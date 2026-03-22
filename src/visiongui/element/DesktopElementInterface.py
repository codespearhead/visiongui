from abc import ABC, abstractmethod

from visiongui.element.ActionClickOptions import (
    ActionClickOptions,
)
from visiongui.element.ActionTypeOptions import (
    ActionTypeOptions,
)
from visiongui.element.ClickOverlayOptions import (
    ClickOverlayOptions,
)


class DesktopElementInterface(ABC):
    @property
    @abstractmethod
    def top_left(self) -> tuple[int, int]: ...

    @property
    @abstractmethod
    def bottom_right(self) -> tuple[int, int]: ...

    @abstractmethod
    def get_center_coordinates(self) -> tuple[int, int]: ...

    @abstractmethod
    def click(
        self,
        *,
        log_image_name: str,
        options: ActionClickOptions,
        overlay: ClickOverlayOptions,
    ) -> None: ...

    @abstractmethod
    def action_type(
        self,
        *,
        log_image_name: str,
        text_to_type: str,
        options: ActionTypeOptions,
    ) -> None: ...
