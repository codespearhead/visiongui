import logging

logger = logging.getLogger(__name__)


def get_center_coordinates(
    top_left: tuple[int, int],
    bottom_right: tuple[int, int],
) -> tuple[int, int]:
    x1, y1 = top_left
    x2, y2 = bottom_right
    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
    logger.debug(
        f"[CENTER] Absolute center: ({center_x}, {center_y}) from top-left {top_left} and bottom-right {bottom_right}",
    )
    return (center_x, center_y)
