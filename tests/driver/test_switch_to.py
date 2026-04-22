import os
import re
from collections.abc import Generator

import pytest
import pywinctl
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Node

from visiongui.save_file import save_file
from tests.fixtures.HasTestContextDesktopDriver import (
    HasTestContextDesktopDriver,
)
from tests.fixtures.setup_common_paths import setup_common_paths
from visiongui.driver.DesktopDriverWindowsImplementation import (
    DesktopDriverWindowsImplementation,
)
from visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)


OS_PROCESS_KILL_TIMEOUT = int(os.environ["OS_PROCESS_KILL_TIMEOUT"])


@pytest.fixture(scope="function", autouse=True)
def setup(request: FixtureRequest) -> Generator[None]:
    self: HasTestContextDesktopDriver = request.instance
    setup_common_paths(request)
    self.desktop_driver = DesktopDriverWindowsImplementation()
    node: Node = request.node
    self.test_case_name = node.name
    return


class TestSwitchTo:
    desktop_driver: DesktopDriverInterface
    test_case_name: str
    test_suite_output_dir: str

    def test_switch_to_raises_on_invalid_type(self) -> None:
        with pytest.raises(TypeError):
            self.desktop_driver.switch_to(target_window="not a window object")

    def test_switch_to_raises_on_none(self) -> None:
        with pytest.raises(TypeError):
            self.desktop_driver.switch_to(target_window=None)

    def test_switch_to_activates_window(self) -> None:
        gui_code_snippet = f"""
import tkinter as tk

root = tk.Tk()
root.title('{self.test_case_name}')
root.mainloop()
"""
        script_path = save_file(
            file_content=gui_code_snippet.encode("utf-8"),
            base_path=str(self.test_suite_output_dir),
            file_name=f"{self.test_case_name}.py",
            mode="wb",
        )

        self.desktop_driver.launch_process(cmd=["python", script_path])

        self.desktop_driver.window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
        )

        assert self.desktop_driver.window is not None
        assert self.desktop_driver.window.title == self.test_case_name

        self.desktop_driver.switch_to(target_window=self.desktop_driver.window)

        active_window = pywinctl.getActiveWindow()
        assert active_window == self.desktop_driver.window

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)
