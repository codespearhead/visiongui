import logging
import re
from visiongui.driver.exception import (
    ExceptionTimeout,
    ExceptionUnexpectedWindowFound,
)
from visiongui.driver.find_window import _get_matching_window
from visiongui.driver.wait import WebDriverWait

logger = logging.getLogger(__name__)


def wait_for_window_to_disappear(
    title: re.Pattern,
    timeout: float,
) -> None:
    def _window_check() -> bool:
        return _get_matching_window(title) is None

    try:
        WebDriverWait(timeout).until(_window_check)
    except ExceptionTimeout:
        raise ExceptionUnexpectedWindowFound(window_title=title.pattern)
