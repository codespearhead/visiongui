class ExceptionTimeout(Exception):
    def __init__(
        self,
        *,
        timeout: float,
    ):
        super().__init__(f"Element was not found within the {timeout}-second timeout")


class ExceptionElementNotStableLongEnough(Exception):
    def __init__(
        self,
        *,
        time_held_stable_on_screen: float,
        timeout: float,
    ):
        super().__init__(
            f"Element was not stable on screen for {time_held_stable_on_screen} seconds within the {timeout}-second timeout",
        )


class ExceptionElementNotFound(ExceptionTimeout):
    def __init__(
        self,
        *,
        timeout: float,
    ):
        super().__init__(timeout=timeout)


class ExceptionWindowNotFound(Exception):
    def __init__(
        self,
        *,
        window_title: str,
        timeout: float,
    ):
        super().__init__(
            f"Window '{window_title}' not found within the {timeout}-second timeout",
        )


class ExceptionUnexpectedWindowFound(Exception):
    def __init__(
        self,
        *,
        window_title: str,
    ):
        super().__init__(
            f"Window '{window_title}' was found, but it should not be present.",
        )
