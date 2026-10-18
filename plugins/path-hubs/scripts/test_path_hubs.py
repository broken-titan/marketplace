#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "path_hubs.py"


class PathHubsTest(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp())
        self.home = self.work / "home"
        self.state = self.work / "state"
        self.home.mkdir()
        self.state.mkdir()
        self.env = os.environ.copy()
        self.env["HOME"] = str(self.home)
        self.env["PATH_HUBS_HOME"] = str(self.state)
        self.env["PATH_HUBS_SCAN_ROOT"] = str(self.home)
        self.env.pop("PATH_HUBS_SESSION_ID", None)
        self.env.pop("PATH_HUBS_CWD", None)

    def run_cli(self, *args: str, stdin: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=self.work,
            env=self.env,
            text=True,
            input=stdin,
            capture_output=True,
            check=False,
        )

    def write_repo(self, rel: str, remote: str) -> Path:
        root = self.work / rel
        root.mkdir(parents=True)
        subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True)
        subprocess.run(
            ["git", "remote", "add", "origin", remote],
            cwd=root,
            check=True,
            capture_output=True,
        )
        return root

    def write_session(self, cwd: Path, sid: str, title: str, files: list[str] | None = None) -> None:
        encoded = "-" + str(cwd).lstrip("/").replace("/", "-")
        dest = self.home / ".claude" / "projects" / encoded
        dest.mkdir(parents=True, exist_ok=True)
        rows = [
            {
                "type": "user",
                "cwd": str(cwd),
                "message": {"role": "user", "content": title},
            },
        ]
        for path in files or []:
            rows.append(
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "tool_use", "name": "Write", "input": {"file_path": path}}
                        ]
                    },
                }
            )
        (dest / f"{sid}.jsonl").write_text(
            "\n".join(json.dumps(row) for row in rows) + "\n",
            encoding="utf-8",
        )

    def state_json(self) -> dict:
        return json.loads((self.state / "state.json").read_text(encoding="utf-8"))

    def test_auto_link_groups_chats_and_code(self):
        web = self.write_repo("acme/webapp", "git@github.com:acme/webapp.git")
        mobile = self.write_repo("acme/mobile", "https://github.com/acme/mobile.git")
        notes = self.work / "scratch"
        notes.mkdir()
        self.write_session(
            web,
            "auth",
            "User auth flow",
            [str(web / "lib" / "auth.ts")],
        )
        self.write_session(
            mobile,
            "onboard",
            "Onboarding improvements",
            [str(mobile / "store" / "userStore.ts")],
        )
        self.write_session(notes, "idea", "Idea cache strategy")
        result = self.run_cli("view", "--format", "text")
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        self.assertIn("acme/webapp", out)
        self.assertIn("acme/mobile", out)
        self.assertIn("User auth flow", out)
        self.assertIn("auth.ts", out)
        self.assertIn("UNLINKED", out)
        self.assertIn("Idea cache strategy", out)
        self.assertIn("Auto-link new repos: on", out)
        state = self.state_json()
        self.assertTrue(state["autoLink"])
        self.assertIn("acme/webapp", state["hubs"])
        self.assertEqual(state["items"]["chat:auth"]["hubId"], "acme/webapp")
        self.assertEqual(state["items"][f"code:{web / 'lib' / 'auth.ts'}"]["kind"], "code")
        self.assertNotIn("brokentitan/dotfiles", state["hubs"])
        self.assertTrue(state["items"]["chat:idea"]["unlinked"] or not state["items"]["chat:idea"].get("hubId"))

    def test_manual_unlink_and_toggle_persist(self):
        web = self.write_repo("acme/webapp", "git@github.com:acme/webapp.git")
        self.write_session(web, "auth", "User auth flow")
        self.run_cli("view", "--format", "text")
        off = self.run_cli("auto-off")
        self.assertEqual(off.returncode, 0, off.stderr)
        self.assertIn("off", off.stdout)
        unlink = self.run_cli("unlink", "--id", "chat:auth")
        self.assertEqual(unlink.returncode, 0, unlink.stderr)
        self.run_cli("view", "--format", "text")
        state = self.state_json()
        self.assertFalse(state["autoLink"])
        self.assertTrue(state["items"]["chat:auth"]["unlinked"])
        self.assertEqual(state["items"]["chat:auth"]["hubId"], "")
        text = self.run_cli("view", "--format", "text").stdout
        self.assertIn("Auto-link new repos: off", text)
        self.assertIn("User auth flow", text)

    def test_manual_link_wins_after_discover(self):
        web = self.write_repo("acme/webapp", "git@github.com:acme/webapp.git")
        other = self.write_repo("acme/infra", "git@github.com:acme/infra.git")
        self.write_session(other, "notes", "General notes")
        linked = self.run_cli(
            "link",
            "--id",
            "chat:notes",
            "--hub",
            "acme/webapp",
            "--cwd",
            str(web),
            "--title",
            "General notes",
        )
        self.assertEqual(linked.returncode, 0, linked.stderr)
        self.run_cli("view", "--format", "text")
        state = self.state_json()
        self.assertEqual(state["items"]["chat:notes"]["hubId"], "acme/webapp")
        self.assertTrue(state["items"]["chat:notes"]["manual"])

    def test_session_start_and_statusline(self):
        web = self.write_repo("acme/webapp", "git@github.com:acme/webapp.git")
        payload = json.dumps({"session_id": "s1", "cwd": str(web), "session_name": "User auth flow"})
        start = self.run_cli("session-start", stdin=payload)
        self.assertEqual(start.returncode, 0, start.stderr)
        data = json.loads(start.stdout)
        self.assertIn("acme/webapp", data["hookSpecificOutput"]["additionalContext"])
        line = self.run_cli("statusline", stdin=payload)
        self.assertEqual(line.returncode, 0, line.stderr)
        self.assertIn("2a · acme/webapp", line.stdout)
        self.assertIn("auto-link on", line.stdout)

    def test_html_view_has_mock_regions(self):
        web = self.write_repo("acme/webapp", "git@github.com:acme/webapp.git")
        self.write_session(web, "auth", "User auth flow", [str(web / "auth.ts")])
        dest = self.work / "view.html"
        result = self.run_cli("view", "--format", "html", "--out", str(dest))
        self.assertEqual(result.returncode, 0, result.stderr)
        html = dest.read_text(encoding="utf-8")
        for needle in (
            "2a · Path hubs",
            "Path hubs",
            "Chat context",
            "Code context",
            "Unlinked",
            "Auto-link new repos",
            "User auth flow",
            "auth.ts",
            "#e07a5f",
            "#14110f",
        ):
            self.assertIn(needle, html)

    def test_cowork_nests_under_chats(self):
        web = self.write_repo("acme/webapp", "git@github.com:acme/webapp.git")
        self.write_session(web, "cowork-1", "Cowork review")
        text = self.run_cli("view", "--format", "text").stdout
        self.assertIn("Cowork review · cowork", text)
        self.assertIn("Chats (", text)


if __name__ == "__main__":
    unittest.main()
