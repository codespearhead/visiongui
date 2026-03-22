from typing import Protocol, runtime_checkable

from .HasTestContextDesktopDriver import HasTestContextDesktopDriver


@runtime_checkable
class HasTestContextDesktopDriverWithDummyGuiAppWithButtonLabelTextWereNo(
    HasTestContextDesktopDriver,
    Protocol,
):
    image_dummy_gui_with_button_label_text_we_re_no: str
