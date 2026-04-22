import threading
import tkinter as tk
from typing import cast

from visiongui.element.ClickOverlayOptions import (
    ClickOverlayOptions,
)


def click_overlay(x: int, y: int, options: ClickOverlayOptions) -> None:
    def _show() -> None:
        overlay = tk.Tk()
        overlay.overrideredirect(True)
        overlay.attributes("-topmost", True)

        arrow_width = options.size
        arrow_height = options.size
        overlay_x = x - arrow_width // 2
        overlay_y = y + options.arrow_y_axis_offset

        overlay.geometry(f"{arrow_width}x{arrow_height}+{overlay_x}+{overlay_y}")

        canvas = tk.Canvas(
            overlay,
            width=arrow_width,
            height=arrow_height,
            highlightthickness=options.highlight_thickness,
            bd=0,
        )
        canvas.pack()

        mid_x = arrow_width // 2
        arrowhead_height = arrow_height // 3
        arrowhead_tip = (mid_x, 0)
        arrowhead_left = (mid_x - arrowhead_height // 2, arrowhead_height)
        arrowhead_right = (mid_x + arrowhead_height // 2, arrowhead_height)
        shaft_width = arrow_width // 8
        shaft_half_width = shaft_width / 2
        shaft_top_left = (mid_x - shaft_half_width, arrowhead_height)
        shaft_top_right = (mid_x + shaft_half_width, arrowhead_height)
        shaft_bottom_right = (mid_x + shaft_half_width, arrow_height)
        shaft_bottom_left = (mid_x - shaft_half_width, arrow_height)

        points: list[tuple[float, float]] = [
            arrowhead_tip,
            arrowhead_left,
            shaft_top_left,
            shaft_bottom_left,
            shaft_bottom_right,
            shaft_top_right,
            arrowhead_right,
        ]

        canvas.create_polygon(
            cast(
                list[tuple[int, int]],
                [tuple(round(coord) for coord in point) for point in points],
            ),
            fill=options.fill_color,
            outline=options.border_color,
            width=options.border_width,
        )

        overlay.attributes("-alpha", options.alpha)

        overlay.after(int(options.duration * 1000), overlay.destroy)
        overlay.mainloop()

    threading.Thread(target=_show, daemon=True).start()
