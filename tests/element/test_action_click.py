import logging
import os
import re
from collections.abc import Generator

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Node
from pynput.mouse import Button

from src.visiongui.save_file import save_file
from tests.fixtures.HasTestContextDesktopDriver import (
    HasTestContextDesktopDriver,
)
from tests.fixtures.setup_common_paths import setup_common_paths
from src.visiongui.driver.DesktopDriverWindowsImplementation import (
    DesktopDriverWindowsImplementation,
)
from src.visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)
from src.visiongui.element.ActionClickOptions import (
    ActionClickOptions,
)
from src.visiongui.element.ClickOverlayOptions import (
    ClickOverlayOptions,
)

logger = logging.getLogger(__name__)

TEST_INPUT_DIR = os.environ["TEST_INPUT_DIR"]
TEST_OUTPUT_DIR = os.environ["TEST_OUTPUT_DIR"]
TEST_IMAGE_BUTTON_LABEL_TEXT_WE_RE_NO = os.environ[
    "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO"
]
OS_PROCESS_KILL_TIMEOUT = int(os.environ["OS_PROCESS_KILL_TIMEOUT"])


@pytest.fixture(scope="function", autouse=True)
def setup(request: FixtureRequest) -> Generator[None]:
    self: HasTestContextDesktopDriver = request.instance
    setup_common_paths(request)
    self.desktop_driver = DesktopDriverWindowsImplementation()
    node: Node = request.node
    self.test_case_name = node.name
    return


class TestClickElement:
    desktop_driver: DesktopDriverInterface
    test_case_name: str
    test_suite_output_dir: str

    def test_single_left_click(self) -> None:
        gui_code_snippet = f"""
import tkinter as tk

def on_left():
    print("[TEST] left click received")

root = tk.Tk()
root.title('{self.test_case_name}')
root.lift()
root.attributes("-topmost", True)
root.after_idle(root.attributes, "-topmost", False)

btn = tk.Button(root, text="we're no", command=on_left)
btn.pack(expand=True, fill="both", padx=40, pady=40)

root.mainloop()
"""
        script_path = save_file(
            file_content=gui_code_snippet.encode("utf-8"),
            base_path=str(self.test_suite_output_dir),
            file_name=f"{self.test_case_name}.py",
            mode="wb",
        )

        self.desktop_driver.launch_process(cmd=["python", script_path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        image_path = os.path.join(TEST_INPUT_DIR, TEST_IMAGE_BUTTON_LABEL_TEXT_WE_RE_NO)
        desktop_element = self.desktop_driver.find_element_by_image(
            image_path=image_path,
            log_image_name=self.test_case_name,
            timeout=5,
            margin_of_error=0.1,
            time_held_stable_on_screen=1.0,
            debug_output_base_path=self.test_suite_output_dir,
        )

        desktop_element.click(
            log_image_name=self.test_case_name,
            options=ActionClickOptions(button=Button.left, count=1),
            overlay=ClickOverlayOptions(),
        )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)
