from typing import Protocol, runtime_checkable

from .HasTestContext import HasTestContext
from visiongui.driver.DesktopDriverInterface import (
    DesktopDriverInterface,
)


@runtime_checkable
class HasTestContextDesktopDriver(HasTestContext, Protocol):
    desktop_driver: DesktopDriverInterface
