from typing import Protocol, runtime_checkable

from .HasTestContextDesktopDriver import HasTestContextDesktopDriver


@runtime_checkable
class HasTestContextDesktopDriverWithGuiAppFilePath(
    HasTestContextDesktopDriver,
    Protocol,
):
    gui_app_launcher_file_path: str
