from dataclasses import dataclass


@dataclass
class ActionTypeOptions:
    delay_between_keys: float = 0.05
    delay_after_click: float = 0.1
