import time
from collections.abc import Callable

from visiongui.driver.exception import ExceptionTimeout


class WebDriverWait:
    def __init__(self, timeout: float, poll_frequency: float = 0.1):
        self.timeout = timeout
        self.poll_frequency = poll_frequency

    def until(
        self,
        condition: Callable[[], object],
    ):
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
