import logging
import os

logger = logging.getLogger(__name__)


def save_file(
    file_content: bytes,
    base_path: str,
    file_name: str,
    mode: str = "wb",
) -> str:
    if not isinstance(file_content, bytes):
        raise TypeError("Expected file_content to be bytes")
    if not isinstance(file_name, str):
        raise TypeError("Expected file_name to be a str")
    if not isinstance(mode, str):
        raise TypeError("Expected mode to be a str")
    if not isinstance(base_path, str):
        raise TypeError("Expected base_path to be a str")

    base_path = os.path.normpath(base_path)

    if not os.path.isdir(base_path):
        raise FileNotFoundError(f"Directory does not exist: {base_path}")
    if not os.access(base_path, os.W_OK):
        raise PermissionError(f"Directory is not writable: {base_path}")

    full_path = os.path.join(base_path, file_name)

    try:
        with open(full_path, mode) as f:
            f.write(file_content)
        logger.debug(f"save_file: wrote to {full_path}")
        return full_path
    except OSError as e:
        logger.exception(f"save_file: I/O error while saving '{full_path}': {e}")
        raise
