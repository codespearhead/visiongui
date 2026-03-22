from dataclasses import dataclass

from pynput.mouse import Button


@dataclass
class ActionClickOptions:
    button: Button = Button.left
    count: int = 1
    delay_between_clicks: float = 0.1
