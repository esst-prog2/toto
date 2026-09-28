import os
from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_root_app_bootstraps_src_layout_without_editable_import_path() -> None:
    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('app.py', run_name='__main__')",
        ],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    assert "No module named 'toto_estimator'" not in process.stderr

