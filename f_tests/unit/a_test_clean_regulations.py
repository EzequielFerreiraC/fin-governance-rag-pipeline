import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from d_src.pipeline.a_bronze_to_silver.clean_regulations import get_project_data_paths


def test_get_project_data_paths_uses_repo_root():
    project_root = Path(__file__).resolve().parents[2]

    bronze_dir, silver_dir = get_project_data_paths()

    assert bronze_dir == project_root / "c_data" / "a_raw" / "a_bronze"
    assert silver_dir == project_root / "c_data" / "b_processed" / "b_silver"
