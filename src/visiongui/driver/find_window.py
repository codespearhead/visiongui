import logging
import re

import pywinctl

from visiongui.driver.exception import (
    ExceptionTimeout,
    ExceptionUnexpectedWindowFound,
    ExceptionWindowNotFound,
)
from visiongui.driver.wait import WebDriverWait

logger = logging.getLogger(__name__)


def find_window(
    title: re.Pattern,
    timeout: float,
    should_exist: bool = True,
) -> pywinctl.Window | None:
    def _window_check() -> pywinctl.Window | None:
        all_windows = pywinctl.getAllWindows()
        titles = [w.title for w in all_windows if w.title.strip()]
        logger.debug(f"Checking all window titles: {titles}")

        matched = next((w for w in all_windows if title.search(w.title.strip())), None)
        logger.debug(f"Matched window for pattern {title.pattern}: {matched}")

        if should_exist:
            return matched
        if matched:
            raise ExceptionUnexpectedWindowFound(window_title=title.pattern)
        return True

    try:
        result = WebDriverWait(timeout).until(_window_check)
    except ExceptionTimeout:
        if should_exist is True:
            raise ExceptionWindowNotFound(timeout=timeout, window_title=title.pattern)
        raise ExceptionUnexpectedWindowFound(window_title=title.pattern)

    if should_exist:
        if not isinstance(result, pywinctl.Window):
            raise ExceptionWindowNotFound(timeout=timeout, window_title=title.pattern)
        logger.info(f"Window found: {result.title}")
        return result

    return None
