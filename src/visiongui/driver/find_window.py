import logging
import re
import pywinctl
from visiongui.driver.exception import (
    ExceptionTimeout,
    ExceptionWindowNotFound,
)
from visiongui.driver.wait import WebDriverWait

logger = logging.getLogger(__name__)


def _get_matching_window(title: re.Pattern[str]) -> pywinctl.Window | None:
    all_windows = pywinctl.getAllWindows()  # type: ignore[no-untyped-call]
    titles = [window.title for window in all_windows if window.title.strip()]
    logger.debug(f"Checking all window titles: {titles}")

    matched = next(
        (window for window in all_windows if title.search(window.title.strip())),
        None,
    )
    logger.debug(f"Matched window for pattern {title.pattern}: {matched}")

    return matched


def find_window(
    title: re.Pattern[str],
    timeout: int,
) -> pywinctl.Window:
    def _window_check() -> pywinctl.Window | None:
        return _get_matching_window(title)

    try:
        result = WebDriverWait(timeout).until(_window_check)
    except ExceptionTimeout:
        raise ExceptionWindowNotFound(
            timeout=timeout,
            window_title=title.pattern,
        )

    if not isinstance(result, pywinctl.Window):
        raise ExceptionWindowNotFound(
            timeout=timeout,
            window_title=title.pattern,
        )

    logger.info(f"Window found: {result.title}")
    return result
