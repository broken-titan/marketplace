from pathlib import Path

CODE = Path(__file__).resolve().parents[1]


def test_expected_dag_files_exist():
    dags = CODE / "dags"
    assert (dags / "source_ingest.py").exists()
    assert (dags / "warehouse_transform.py").exists()
    assert (dags / "app_publish.py").exists()
    assert (dags / "dbt" / "warehouse" / "dbt_project.yml").exists()
