import sys
import subprocess
from pathlib import Path


def test_quickstart_runs():
    script = Path("demo/main.py")

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
