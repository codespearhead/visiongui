import os
import re
import subprocess
import time
from collections.abc import Generator
from pathlib import Path

import pytest
import pywinctl
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Node

from tests.fixtures.HasTestContextDesktopDriver import (
    HasTestContextDesktopDriver,
)
from visiongui.driver.DesktopDriverWindowsImplementation import (
    DesktopDriverWindowsImplementation,
)
from visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)
from visiongui.driver.exception import (
    ExceptionUnexpectedWindowFound,
)

TEST_OUTPUT_DIR = os.environ["TEST_OUTPUT_DIR"]
OS_PROCESS_KILL_TIMEOUT = int(os.environ["OS_PROCESS_KILL_TIMEOUT"])


@pytest.fixture(scope="function", autouse=True)
def setup(request: FixtureRequest) -> Generator[None]:
    self: HasTestContextDesktopDriver = request.instance
    self.desktop_driver = DesktopDriverWindowsImplementation()
    node: Node = request.node
    self.test_case_name = node.name
    return


@pytest.fixture(scope="function")
def dummy_app_path(request: FixtureRequest, tmp_path: Path) -> Path:
    self: HasTestContextDesktopDriver = request.instance
    test_case_name = self.test_case_name
    script = f"""
import tkinter as tk
root = tk.Tk()
root.title('{test_case_name}')
root.mainloop()
"""
    file_path = os.path.join(str(tmp_path), f"{test_case_name}.py")
    path = Path(file_path)
    path.write_text(script, encoding="utf-8")
    return path


def launch_gui_subprocess(script_path: Path) -> subprocess.Popen:
    proc = subprocess.Popen(["python", str(script_path)])
    for _ in range(30):
        if any(script_path.stem == w.title for w in pywinctl.getAllWindows()):
            break
        time.sleep(0.1)
    return proc


class TestWaitForWindowToDisappear:
    desktop_driver: DesktopDriverInterface
    test_case_name: str

    def test_window_should_disappear_and_does(self, dummy_app_path: Path) -> None:
        self.desktop_driver.launch_process(cmd=["python", str(dummy_app_path)])

        self.desktop_driver.window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=3,
        )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

        self.desktop_driver.wait_for_window_to_disappear(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
        )

    def test_window_should_not_exist_but_does(self, dummy_app_path: Path) -> None:
        self.desktop_driver.launch_process(cmd=["python", str(dummy_app_path)])

        self.desktop_driver.window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=3,
        )
        with pytest.raises(ExceptionUnexpectedWindowFound):
            self.desktop_driver.wait_for_window_to_disappear(
                title=re.compile(f"^{re.escape(self.test_case_name)}$"),
                timeout=3,
            )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)
