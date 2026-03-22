import os
from pathlib import Path

TEST_INPUT_DIR = os.path.join(
    Path(__file__).parent,
    "assets",
)

os.environ.setdefault("OS_PROCESS_KILL_TIMEOUT", "5")
os.environ.setdefault("TEST_INPUT_DIR", TEST_INPUT_DIR)
os.environ.setdefault("TEST_OUTPUT_DIR", "./tests__output")


os.environ.setdefault(
    "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_CIRCLE_RED",
    os.path.join(
        TEST_INPUT_DIR,
        "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_CIRCLE_RED.png",
    ),
)
os.environ.setdefault(
    "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_CIRCLE_BLUE",
    os.path.join(
        TEST_INPUT_DIR,
        "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_CIRCLE_BLUE.png",
    ),
)
os.environ.setdefault(
    "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO",
    os.path.join(
        TEST_INPUT_DIR,
        "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_BUTTON_LABEL_TEXT_WE_RE_NO.png",
    ),
)
os.environ.setdefault(
    "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_TWO_BUTTONS_LABEL_TEXT_ABRIR",
    os.path.join(
        TEST_INPUT_DIR,
        "TEST_DESKTOPDRIVER_FIND_ELEMENT_BY_IMAGE_PATH_GUI_WITH_TWO_BUTTONS_LABEL_TEXT_ABRIR.png",
    ),
)
os.environ.setdefault(
    "TEST_DESKTOPDRIVER_TYPE_ACTION_IMAGE_PATH_GUI_LABEL_DUMMY_TEXT_BOX",
    os.path.join(
        TEST_INPUT_DIR,
        "TEST_DESKTOPDRIVER_TYPE_ACTION_IMAGE_PATH_GUI_LABEL_DUMMY_TEXT_BOX.png",
    ),
)
