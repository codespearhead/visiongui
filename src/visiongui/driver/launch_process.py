import os
import subprocess


def launch_process(cmd: list[str]) -> subprocess.Popen[bytes]:
    if not cmd:
        raise ValueError("Command list must not be empty")

    for part in cmd:
        if os.path.isfile(part):
            break
    else:
        raise FileNotFoundError(
            "No valid executable or script found in the command list",
        )

    return subprocess.Popen(cmd)
