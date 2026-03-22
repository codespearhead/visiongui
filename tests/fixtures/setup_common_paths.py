import logging
import os
from pathlib import Path

from _pytest.fixtures import FixtureRequest

from .HasTestContextDesktopDriver import HasTestContextDesktopDriver

logger = logging.getLogger(__name__)

TEST_OUTPUT_DIR = os.environ["TEST_OUTPUT_DIR"]


def setup_common_paths(request: FixtureRequest) -> None:
    if request.instance is None:
        raise RuntimeError("setup_common_paths must be used within a class-based test")

    self: HasTestContextDesktopDriver = request.instance

    module_name = (
        ".".join(self.__module__.split(".")[1:-1])
        if len(self.__module__.split(".")) > 2
        else (_ for _ in ()).throw(ValueError("Invalid module path"))
    )
    logger.info(f"module_name: {module_name}")
    module_parts = module_name.split(".")
    self.module_output_dir = os.path.join(TEST_OUTPUT_DIR, *module_parts)
    Path(self.module_output_dir).mkdir(parents=True, exist_ok=True)

    test_suite_class_name = self.__class__.__name__
    logger.info(f"test_suite_class_name: {test_suite_class_name}")
    self.test_suite_output_dir = os.path.join(
        self.module_output_dir,
        test_suite_class_name,
    )
    Path(self.test_suite_output_dir).mkdir(parents=True, exist_ok=True)
    logger.info(f"test_suite_output_dir: {self.test_suite_output_dir}")
