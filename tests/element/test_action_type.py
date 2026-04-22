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
from src.visiongui.element.ActionTypeOptions import (
    ActionTypeOptions,
)
from src.visiongui.element.ClickOverlayOptions import (
    ClickOverlayOptions,
)

logger = logging.getLogger(__name__)

TEST_INPUT_DIR = os.environ["TEST_INPUT_DIR"]
TEST_OUTPUT_DIR = os.environ["TEST_OUTPUT_DIR"]
TEST_IMAGE_ENTRY_LABEL = os.environ[
    "TEST_DESKTOPDRIVER_TYPE_ACTION_IMAGE_PATH_GUI_LABEL_DUMMY_TEXT_BOX"
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


class TestTypeIntoEntry:
    desktop_driver: DesktopDriverInterface
    test_case_name: str
    test_suite_output_dir: str

    def test_type_text_into_entry(self) -> None:
        gui_code_snippet = f"""
import tkinter as tk

root = tk.Tk()
root.title('{self.test_case_name}')
root.lift()
root.attributes("-topmost", True)
root.after_idle(root.attributes, "-topmost", False)

container = tk.Frame(root)
container.pack(padx=40, pady=40)

label = tk.Label(container, text="Dummy text box")
label.pack(anchor="w")

entry = tk.Entry(container, name="entry")
entry.pack(fill="x")
entry.focus_set()

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
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        image_path = os.path.join(TEST_INPUT_DIR, TEST_IMAGE_ENTRY_LABEL)
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

        desktop_element.action_type(
            log_image_name=self.test_case_name,
            text_to_type="hello world",
            options=ActionTypeOptions(),
        )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)
