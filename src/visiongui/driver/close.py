import logging

import psutil
import win32process

from visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)

logger = logging.getLogger(__name__)


def close(
    driver: DesktopDriverInterface,
    OS_PROCESS_KILL_TIMEOUT: float,
) -> None:
    if not isinstance(driver, DesktopDriverInterface):
        raise TypeError("Expected driver to be an instance of DesktopDriver")

    window = driver.window
    pid = None
    if window is not None:
        # Obtain the process ID directly from the window handle via the Win32 API. In some cases, window.getPID() returned invalid process IDs (e.g. negative or nonexistent values), causing psutil.Process(pid) to fail even though the window was still present. GetWindowThreadProcessId() reliably returns the process that owns the window.
        _, pid = win32process.GetWindowThreadProcessId(window._hWnd)

    logger.debug(f"Forcefully killing process owning the window: {pid}")
    proc = psutil.Process(pid)
    proc.terminate()
    try:
        proc.wait(timeout=OS_PROCESS_KILL_TIMEOUT)
    except psutil.NoSuchProcess:
        logger.debug(f"Process {pid} already terminated before wait.")

    # Clean up the subprocess properly to avoid resource leak
    if driver.process:
        try:
            driver.process.wait(timeout=1)
        except Exception:
            pass

    driver.process = None
    driver.window = None
