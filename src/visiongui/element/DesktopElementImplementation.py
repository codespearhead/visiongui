import logging

from visiongui.element.action_click import action_click
from visiongui.element.action_type import action_type
from visiongui.element.ActionClickOptions import (
    ActionClickOptions,
)
from visiongui.element.ActionTypeOptions import (
    ActionTypeOptions,
)
from visiongui.element.ClickOverlayOptions import (
    ClickOverlayOptions,
)
from visiongui.element.DesktopElementInterface import (
    DesktopElementInterface,
)
from visiongui.element.get_center_coordinates import (
    get_center_coordinates,
)

logger = logging.getLogger(__name__)


class DesktopElementImplementation(DesktopElementInterface):
    def __init__(
        self,
        top_left: tuple[int, int],
        bottom_right: tuple[int, int],
    ):
        self._top_left = top_left
        self._bottom_right = bottom_right

    @property
    def top_left(self) -> tuple[int, int]:
        return self._top_left

    @property
    def bottom_right(self) -> tuple[int, int]:
        return self._bottom_right

    def get_center_coordinates(self) -> tuple[int, int]:
        return get_center_coordinates(
            top_left=self._top_left,
            bottom_right=self._bottom_right,
        )

    def click(
        self,
        *,
        log_image_name: str,
        options: ActionClickOptions,
        overlay: ClickOverlayOptions,
    ) -> None:
        return action_click(
            web_element=self,
            log_image_name=log_image_name,
            options=options,
            overlay=overlay,
        )

    def action_type(
        self,
        *,
        log_image_name: str,
        text_to_type: str,
        options: ActionTypeOptions,
    ) -> None:
        return action_type(
            web_element=self,
            log_image_name=log_image_name,
            text_to_type=text_to_type,
            options=options,
        )
