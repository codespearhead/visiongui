import subprocess

import pywinctl

from visiongui.driver.close import close
from visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)
from visiongui.driver.find_element_by_image import (
    find_element_by_image,
)
from visiongui.driver.find_window import find_window
from visiongui.driver.launch_process import launch_process
from visiongui.driver.switch_to import switch_to
from visiongui.element.DesktopElementInterface import (
    DesktopElementInterface,
)


class DesktopDriverImplementation(DesktopDriverInterface):
    def __init__(self):
        self._process: subprocess.Popen | None = None
        self._window: pywinctl.Window | None = None

    @property
    def process(self) -> subprocess.Popen | None:
        return self._process

    @process.setter
    def process(self, value: subprocess.Popen | None) -> None:
        self._process = value

    @property
    def window(self) -> pywinctl.Window | None:
        return self._window

    @window.setter
    def window(self, value: pywinctl.Window | None) -> None:
        self._window = value

    def launch_process(self, *, cmd: list[str]) -> subprocess.Popen:
        self.process = launch_process(cmd=cmd)
        return self.process

    def find_window(
        self,
        *,
        title,
        timeout: float,
        should_exist: bool,
    ) -> pywinctl.Window:
        return find_window(
            title=title,
            timeout=timeout,
            should_exist=should_exist,
        )

    def find_element_by_image(
        self,
        *,
        image_path: str,
        timeout: float,
        log_image_name: str,
        margin_of_error: float,
        time_held_stable_on_screen: float,
        debug_output_base_path: str,
        match_with_color: bool = False,
    ) -> DesktopElementInterface:
        return find_element_by_image(
            image_path=image_path,
            timeout=timeout,
            log_image_name=log_image_name,
            margin_of_error=margin_of_error,
            time_held_stable_on_screen=time_held_stable_on_screen,
            debug_output_base_path=debug_output_base_path,
            match_with_color=match_with_color,
        )

    def switch_to(
        self,
        *,
        target_window: pywinctl.Window,
    ) -> None:
        switch_to(target_window=target_window)
        self.window = target_window

    def close(
        self,
        *,
        OS_PROCESS_KILL_TIMEOUT: int,
    ) -> None:
        close(
            self,
            OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT,
        )
