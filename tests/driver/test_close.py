from ..fixtures.HasTestContextDesktopDriver import HasTestContextDesktopDriver

import os
import re
from collections.abc import Generator
from pathlib import Path

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Node

from visiongui.driver.DesktopDriverWindowsImplementation import (
    DesktopDriverWindowsImplementation,
)

from visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)

OS_PROCESS_KILL_TIMEOUT = int(os.environ["OS_PROCESS_KILL_TIMEOUT"])


@pytest.fixture(scope="function", autouse=True)
def setup(request: FixtureRequest) -> Generator[None, None, None]:
    self: HasTestContextDesktopDriver = request.instance
    self.desktop_driver = DesktopDriverWindowsImplementation()
    node: Node = request.node
    self.test_case_name = node.name
    yield


@pytest.fixture(scope="function")
def dummy_app_path(request: FixtureRequest, tmp_path: Path) -> Path:
    self: HasTestContextDesktopDriver = request.instance
    title = self.test_case_name
    script = f"""
import tkinter as tk
root = tk.Tk()
root.title('{title}')
root.mainloop()
"""
    file_path = os.path.join(str(tmp_path), f"{title}.py")
    path = Path(file_path)
    path.write_text(script, encoding="utf-8")
    return path


@pytest.fixture(scope="function")
def stubborn_app_path(request: FixtureRequest, tmp_path: Path) -> Path:
    self: HasTestContextDesktopDriver = request.instance
    title = self.test_case_name
    script = f"""
import tkinter as tk
def on_close():
    pass
root = tk.Tk()
root.title('{title}')
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
"""
    file_path = os.path.join(str(tmp_path), f"{title}_stubborn.py")
    path = Path(file_path)
    path.write_text(script, encoding="utf-8")
    return path


class TestCloseDesktopDriver:
    desktop_driver: DesktopDriverInterface
    test_case_name: str

    def test_process_and_window_cleanup(self, dummy_app_path: Path) -> None:
        self.desktop_driver.launch_process(cmd=["python", str(dummy_app_path)])

        self.desktop_driver.window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
        )

        assert self.desktop_driver.process is not None
        assert self.desktop_driver.window is not None

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

        assert self.desktop_driver.process is None
        assert self.desktop_driver.window is None

    def test_forced_process_termination(self, stubborn_app_path: Path) -> None:
        self.desktop_driver.launch_process(cmd=["python", str(stubborn_app_path)])

        self.desktop_driver.window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
        )

        assert self.desktop_driver.process is not None
        assert self.desktop_driver.window is not None

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

        assert self.desktop_driver.process is None
        assert self.desktop_driver.window is None
