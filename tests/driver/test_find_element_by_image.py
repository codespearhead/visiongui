import os
import re
from collections.abc import Generator

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Node
from pynput.mouse import Button


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
from visiongui.driver.exception import (
    ExceptionElementNotFound,
    ExceptionElementNotStableLongEnough,
)
from visiongui.element.ActionClickOptions import (
    ActionClickOptions,
)
from visiongui.element.ClickOverlayOptions import (
    ClickOverlayOptions,
)

TEST_IMAGE_RED = os.environ["TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_CIRCLE_RED"]
TEST_IMAGE_BLUE = os.environ["TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_CIRCLE_BLUE"]
TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO = os.environ[
    "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO"
]
TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_TWO_BUTTONS_LABEL_TEXT_ABRIR = os.environ[
    "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_TWO_BUTTONS_LABEL_TEXT_ABRIR"
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


class TestFindElementByImage:
    desktop_driver: DesktopDriverInterface
    test_case_name: str
    test_suite_output_dir: str

    def test_match_with_color_param(self):
        gui_code_snippet = f"""
import tkinter as tk
root = tk.Tk()
root.title('{self.test_case_name}')
img = tk.PhotoImage(file=r"{TEST_IMAGE_RED}")
label = tk.Label(root, image=img)
label.image = img
label.pack()
root.mainloop()
"""
        script_path_str = save_file(
            file_content=gui_code_snippet.encode("utf-8"),
            base_path=str(self.test_suite_output_dir),
            file_name=f"{self.test_case_name}.py",
            mode="wb",
        )
        self.desktop_driver.launch_process(cmd=["python", script_path_str])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        element = self.desktop_driver.find_element_by_image(
            image_path=TEST_IMAGE_BLUE,
            log_image_name="blue_no_color",
            timeout=5,
            margin_of_error=0.01,
            time_held_stable_on_screen=1.0,
            debug_output_base_path=self.test_suite_output_dir,
            match_with_color=False,
        )
        assert element is not None

        with pytest.raises(ExceptionElementNotFound):
            self.desktop_driver.find_element_by_image(
                image_path=TEST_IMAGE_BLUE,
                log_image_name="blue_with_color",
                timeout=5,
                margin_of_error=0.01,
                time_held_stable_on_screen=1.0,
                debug_output_base_path=self.test_suite_output_dir,
                match_with_color=True,
            )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

    def test_image_detected_by_template_matching(self):
        gui_code_snippet = f"""
import tkinter as tk
root = tk.Tk()
root.title('{self.test_case_name}')
tk.Button(root, text="We're No Strangers To Love").pack()
root.mainloop()
    """
        path = save_file(
            gui_code_snippet.encode("utf-8"),
            str(self.test_suite_output_dir),
            f"{self.test_case_name}.py",
        )
        self.desktop_driver.launch_process(cmd=["python", path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        with pytest.raises(ExceptionElementNotFound):
            self.desktop_driver.find_element_by_image(
                image_path=TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO,
                log_image_name="template_matching",
                timeout=5,
                margin_of_error=0.01,
                time_held_stable_on_screen=1.0,
                debug_output_base_path=self.test_suite_output_dir,
            )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

    def test_image_detected_with_altered_colors(self):
        gui_code_snippet = f"""
import tkinter as tk
root = tk.Tk()
root.title('{self.test_case_name}')
tk.Button(root, text="We're No Strangers To Love").pack()
root.mainloop()
"""
        path = save_file(
            gui_code_snippet.encode("utf-8"),
            str(self.test_suite_output_dir),
            f"{self.test_case_name}.py",
        )
        self.desktop_driver.launch_process(cmd=["python", path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        with pytest.raises(ExceptionElementNotFound):
            self.desktop_driver.find_element_by_image(
                image_path=TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO,
                log_image_name="altered_colors",
                timeout=5,
                margin_of_error=0.01,
                time_held_stable_on_screen=1.0,
                debug_output_base_path=self.test_suite_output_dir,
            )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

    def test_element_detected_after_motion_stops(self):
        gui_code_snippet = f"""
import tkinter as tk, time, threading
root = tk.Tk()
root.title('{self.test_case_name}')
tk.Button(root, text="A").pack()

def move():
    for i in range(30):
        root.geometry(f"+{{100 + i * 10}}+100")
        root.update()
        time.sleep(0.1)
    root.geometry("+200+100")

threading.Thread(target=move, daemon=True).start()
root.mainloop()
"""
        path = save_file(
            gui_code_snippet.encode("utf-8"),
            str(self.test_suite_output_dir),
            f"{self.test_case_name}.py",
        )
        self.desktop_driver.launch_process(cmd=["python", path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        element = self.desktop_driver.find_element_by_image(
            image_path=TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO,
            log_image_name="motion_stops",
            timeout=6,
            margin_of_error=0.1,
            time_held_stable_on_screen=1.0,
            debug_output_base_path=self.test_suite_output_dir,
        )
        assert element is not None

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

    def test_element_detected_despite_background_motion(self):
        gui_code_snippet = f"""
import tkinter as tk, threading, time
root = tk.Tk()
root.title('{self.test_case_name}')
tk.Button(root, text="We're No Strangers To Love").pack()

def wiggle():
    offset = 0
    while True:
        root.geometry(f"+{{100 + (offset % 40)}}+100")
        offset += 10
        root.update()
        time.sleep(0.1)

threading.Thread(target=wiggle, daemon=True).start()
root.mainloop()
    """
        path = save_file(
            gui_code_snippet.encode("utf-8"),
            str(self.test_suite_output_dir),
            f"{self.test_case_name}.py",
        )
        self.desktop_driver.launch_process(cmd=["python", path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        with pytest.raises(ExceptionElementNotFound):
            self.desktop_driver.find_element_by_image(
                image_path=TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO,
                log_image_name="background_motion",
                timeout=10,
                margin_of_error=0.01,
                time_held_stable_on_screen=1.0,
                debug_output_base_path=self.test_suite_output_dir,
            )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

    def test_element_detected_but_not_stable(self):
        gui_code_snippet = f"""
import tkinter as tk, threading, time
root = tk.Tk()
root.title('{self.test_case_name}')
tk.Button(root, text="We're No Strangers To Love").pack()

def wiggle():
    offset = 0
    while True:
        root.geometry(f"+{{100 + (offset % 40)}}+100")
        offset += 10
        root.update()
        time.sleep(0.1)

threading.Thread(target=wiggle, daemon=True).start()
root.mainloop()
    """
        path = save_file(
            gui_code_snippet.encode("utf-8"),
            str(self.test_suite_output_dir),
            f"{self.test_case_name}.py",
        )
        self.desktop_driver.launch_process(cmd=["python", path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        with pytest.raises(ExceptionElementNotStableLongEnough):
            self.desktop_driver.find_element_by_image(
                image_path=TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO,
                log_image_name="unstable_element",
                timeout=5,
                margin_of_error=0.1,
                time_held_stable_on_screen=1.5,
                debug_output_base_path=self.test_suite_output_dir,
            )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

    def test_element_not_found(self):
        gui_code_snippet = f"""
import tkinter as tk
root = tk.Tk()
root.title('{self.test_case_name}')
tk.Button(root, text="NotMatching").pack()
root.mainloop()
    """
        path = save_file(
            gui_code_snippet.encode("utf-8"),
            str(self.test_suite_output_dir),
            f"{self.test_case_name}.py",
        )
        self.desktop_driver.launch_process(cmd=["python", path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        with pytest.raises(ExceptionElementNotFound):
            self.desktop_driver.find_element_by_image(
                image_path=TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO,
                log_image_name="not_present",
                timeout=5,
                margin_of_error=0.001,
                time_held_stable_on_screen=0.1,
                debug_output_base_path=self.test_suite_output_dir,
            )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)

    def test_click_on_abrir_button_with_alpha_centered_image(self):
        gui_code_snippet = f"""
import tkinter as tk
root = tk.Tk()
root.title('{self.test_case_name}')

def on_target_click():
    print("[TEST] Clicked button 'Abrir' inside Tkinter window '{self.test_case_name}'")

def on_secondary_click():
    raise RuntimeError("Wrong button clicked!")

tk.Button(root, text="Abrir", command=on_target_click).pack(pady=(10, 5))
tk.Button(root, text="Cancelar", command=on_secondary_click).pack(pady=(5, 10))
root.mainloop()
    """
        path = save_file(
            gui_code_snippet.encode("utf-8"),
            str(self.test_suite_output_dir),
            f"{self.test_case_name}.py",
        )
        self.desktop_driver.launch_process(cmd=["python", path])

        desktop_window = self.desktop_driver.find_window(
            title=re.compile(f"^{re.escape(self.test_case_name)}$"),
            timeout=5,
            should_exist=True,
        )
        self.desktop_driver.switch_to(target_window=desktop_window)

        log_image_name = "abrir_with_alpha"
        desktop_element = self.desktop_driver.find_element_by_image(
            image_path=TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_TWO_BUTTONS_LABEL_TEXT_ABRIR,
            log_image_name=log_image_name,
            timeout=5,
            margin_of_error=0.01,
            time_held_stable_on_screen=1.0,
            debug_output_base_path=self.test_suite_output_dir,
        )

        desktop_element.click(
            log_image_name=log_image_name,
            options=ActionClickOptions(button=Button.left, count=1),
            overlay=ClickOverlayOptions(),
        )

        self.desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)
