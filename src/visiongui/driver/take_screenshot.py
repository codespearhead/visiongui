from io import BytesIO

import mss
from PIL import Image


def take_screenshot() -> bytes:
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        with BytesIO() as buffer:
            img.save(buffer, format="PNG")
            return buffer.getvalue()
