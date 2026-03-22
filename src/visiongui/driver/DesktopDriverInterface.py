import subprocess
from abc import ABC, abstractmethod

import pywinctl

from visiongui.element.DesktopElementInterface import (
    DesktopElementInterface,
)


class DesktopDriverInterface(ABC):
    @property
    @abstractmethod
    def process(self) -> subprocess.Popen | None: ...

    @process.setter
    @abstractmethod
    def process(self, value: subprocess.Popen | None) -> None: ...

    @property
    @abstractmethod
    def window(self) -> pywinctl.Window | None: ...

    @window.setter
    @abstractmethod
    def window(self, value: pywinctl.Window | None) -> None: ...

    @staticmethod
    @abstractmethod
    def launch_process(*, cmd: list[str]) -> subprocess.Popen: ...

    @abstractmethod
    def find_window(
        self,
        *,
        title,
        timeout: float,
        should_exist: bool,
    ) -> pywinctl.Window: ...

    @abstractmethod
    def switch_to(self, *, target_window: pywinctl.Window) -> None: ...

    @abstractmethod
    def close(
        self,
        *,
        OS_PROCESS_KILL_TIMEOUT: int,
    ) -> None: ...

    @abstractmethod
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
    ) -> DesktopElementInterface: ...
