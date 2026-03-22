import logging
import time

from pynput.mouse import Controller

from visiongui.element.ActionClickOptions import (
    ActionClickOptions,
)
from visiongui.element.click_overlay import click_overlay
from visiongui.element.ClickOverlayOptions import (
    ClickOverlayOptions,
)
from visiongui.element.DesktopElementInterface import (
    DesktopElementInterface,
)

logger = logging.getLogger(__name__)


def action_click(
    web_element: DesktopElementInterface,
    options: ActionClickOptions,
    overlay: ClickOverlayOptions,
    log_image_name: str,
) -> None:
    x, y = web_element.get_center_coordinates()

    if overlay.enabled:
        click_overlay(x=x, y=y, options=overlay)

    mouse = Controller()
    mouse.position = (x, y)

    for i in range(options.count):
        mouse.click(options.button, 1)
        logger.debug(
            f"[CLICK] Clicked ({i + 1}/{options.count}) at {web_element.get_center_coordinates()} "
            f"using {options.button.name} on image: {log_image_name}",
        )
        if i < options.count - 1:
            time.sleep(options.delay_between_clicks)
