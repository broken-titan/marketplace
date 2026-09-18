# Respond

For each comment, in order:

1. Open the file and line. Read the surrounding code and any test that covers it.
2. Decide:

| Pick | When |
|---|---|
| **fix** | The finding is right. Make the smallest change. Say what you changed. |
| **reject** | The finding is wrong or out of scope. Say why, using the code, a test, or the API contract. Do not hedge. |
| **ask** | The finding is unclear, or two readings are both plausible. Ask if one reading is the one they meant. Do not guess-edit. |

3. Do not mix picks in one reply without saying which comment each pick is for.

A thread that asks for a rewrite you already rejected stays rejected until something new in the code, a test, or the contract shows otherwise. Do not silently comply on the next pass.
