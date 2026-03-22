import time

import pytest

from visiongui.driver.exception import ExceptionTimeout
from visiongui.driver.wait import WebDriverWait


class TestWebDriverWait:
    def test_condition_succeeds_before_timeout(self) -> None:
        start_time = time.time()
        wait = WebDriverWait(timeout=2)

        result = wait.until(condition=lambda: True)
        duration = time.time() - start_time

        assert result is True
        assert duration < 2.0

    def test_condition_eventually_succeeds(self) -> None:
        attempts = [0]

        def sometimes_true() -> bool:
            attempts[0] += 1
            return attempts[0] > 3

        wait = WebDriverWait(timeout=2)
        result = wait.until(condition=sometimes_true)

        assert result is True
        assert attempts[0] > 3

    def test_condition_never_succeeds_raises(self) -> None:
        wait = WebDriverWait(timeout=1)

        with pytest.raises(ExceptionTimeout):
            wait.until(condition=lambda: False)
