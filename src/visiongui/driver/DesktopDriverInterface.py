import re
import subprocess
from abc import ABC, abstractmethod

import pywinctl

from visiongui.element.DesktopElementInterface import (
    DesktopElementInterface,
)


class DesktopDriverInterface(ABC):
    @property
    @abstractmethod
    def process(self) -> subprocess.Popen[bytes] | None: ...

    @process.setter
    @abstractmethod
    def process(self, value: subprocess.Popen[bytes] | None) -> None: ...

    @property
    @abstractmethod
    def window(self) -> pywinctl.Window | None: ...

    @window.setter
    @abstractmethod
    def window(self, value: pywinctl.Window | None) -> None: ...

    @abstractmethod
    def launch_process(self, *, cmd: list[str]) -> subprocess.Popen[bytes]: ...

    @abstractmethod
    def find_window(
        self,
        *,
        title: re.Pattern[str],
        timeout: int,
    ) -> pywinctl.Window: ...

    @abstractmethod
    def wait_for_window_to_disappear(
        self,
        *,
        title: re.Pattern[str],
        timeout: int,
    ) -> None: ...

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
        timeout: int,
        log_image_name: str,
        margin_of_error: int,
        time_held_stable_on_screen: int,
        debug_output_base_path: str,
        match_with_color: bool = False,
    ) -> DesktopElementInterface: ...
