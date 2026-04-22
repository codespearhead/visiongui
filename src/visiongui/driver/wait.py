import time
from collections.abc import Callable
from typing import TypeVar

from visiongui.driver.exception import ExceptionTimeout

T = TypeVar("T")


class WebDriverWait:
    def __init__(self, timeout: int, poll_frequency: float = 0.1):
        self.timeout = timeout
        self.poll_frequency = poll_frequency

    def until(
        self,
        condition: Callable[[], T],
    ) -> T:
        end_time = time.time() + self.timeout
        while True:
            try:
                value = condition()
                if value:
                    return value
            except Exception:
                pass
            if time.time() > end_time:
                raise ExceptionTimeout(timeout=self.timeout)
            time.sleep(self.poll_frequency)
