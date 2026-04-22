import re

from visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)


def voltar_ao_vscode(desktop_driver: DesktopDriverInterface) -> None:
    desktop_window = desktop_driver.find_window(
        title=re.compile("Visual Studio Code$"),
        timeout=2,
    )
    assert desktop_window is not None
    desktop_driver.switch_to(target_window=desktop_window)
