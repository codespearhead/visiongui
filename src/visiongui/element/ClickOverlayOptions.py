from dataclasses import dataclass


@dataclass
class ClickOverlayOptions:
    enabled: bool = True
    size: int = 30
    duration: float = 1.5
    border_color: str = "red"
    fill_color: str = "red"
    alpha: float = 0.5
    border_width: int = 2
    highlight_thickness: int = 0
    arrow_y_axis_offset: int = 15
