import logging
import time

from pynput.keyboard import Controller

from visiongui.driver.wait import WebDriverWait
from visiongui.element.ActionTypeOptions import (
    ActionTypeOptions,
)
from visiongui.element.DesktopElementInterface import (
    DesktopElementInterface,
)

logger = logging.getLogger(__name__)


def action_type(
    web_element: DesktopElementInterface,
    text_to_type: str,
    log_image_name: str,
    options: ActionTypeOptions,
) -> None:
    x, y = web_element.get_center_coordinates()

    time.sleep(options.delay_after_click)

    keyboard = Controller()
    for char in text_to_type:
        keyboard.type(char)
        logger.debug(f"[TYPE] Typed '{char}' at ({x}, {y}) on image: {log_image_name}")
        time.sleep(options.delay_between_keys)

    if hasattr(web_element, "get_text") and callable(web_element.get_text):
        wait = WebDriverWait(timeout=2)
        wait.until(
            condition=lambda: web_element.get_text() == text_to_type,
        )
