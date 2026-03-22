import os
import time
from enum import Enum

from visiongui.save_file import save_file
from visiongui.driver.take_screenshot import take_screenshot


class FileNamePrefix(Enum):
    PASS = "PASS"
    FAIL = "FAIL"


def save_debug_screenshot(
    image_file_name_prefix: FileNamePrefix,
    log_image_name: str,
    debug_output_base_path: str,
):
    file_binary = take_screenshot()
    file_name = f"{image_file_name_prefix.value}_{int(time.time())}_{os.path.basename(log_image_name)}.png"
    save_file(
        file_content=file_binary,
        base_path=debug_output_base_path,
        file_name=file_name,
    )
