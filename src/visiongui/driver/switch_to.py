import pywinctl
import ctypes
import platform


def _set_foreground_hwnd(hwnd: int) -> None:
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    GetForegroundWindow = user32.GetForegroundWindow
    GetWindowThreadProcessId = user32.GetWindowThreadProcessId
    GetCurrentThreadId = kernel32.GetCurrentThreadId
    AttachThreadInput = user32.AttachThreadInput
    SetForegroundWindow = user32.SetForegroundWindow
    BringWindowToTop = user32.BringWindowToTop
    ShowWindow = user32.ShowWindow
    IsIconic = user32.IsIconic
    AllowSetForegroundWindow = user32.AllowSetForegroundWindow

    ASFW_ANY = 0xFFFFFFFF
    SW_RESTORE = 9
    if not hwnd:
        return
    # Let any process take foreground briefly
    AllowSetForegroundWindow(ASFW_ANY)

    # If minimized, restore first
    if IsIconic(hwnd):
        ShowWindow(hwnd, SW_RESTORE)

    # “Attach thread input” trick so SetForegroundWindow is honored
    fg = GetForegroundWindow()
    cur_tid = GetCurrentThreadId()
    fg_tid = GetWindowThreadProcessId(fg, None) if fg else 0

    if fg_tid and fg_tid != cur_tid:
        AttachThreadInput(cur_tid, fg_tid, True)

    try:
        BringWindowToTop(hwnd)
        SetForegroundWindow(hwnd)
    finally:
        if fg_tid and fg_tid != cur_tid:
            AttachThreadInput(cur_tid, fg_tid, False)


def switch_to(target_window: pywinctl.Window) -> None:
    if not isinstance(target_window, pywinctl.Window):
        raise TypeError("Expected a pywinctl.Window instance")
    if not target_window:
        raise RuntimeError("No window has been attached to switch to")

    if target_window.isMinimized is True:
        target_window.restore()

    target_window.activate()

    if platform.system() == "Windows":
        _set_foreground_hwnd(target_window.getHandle())
