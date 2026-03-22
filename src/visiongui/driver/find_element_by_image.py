import logging
import os
import time

import cv2
import numpy as np
from mss import mss

from visiongui.driver.exception import (
    ExceptionElementNotFound,
    ExceptionElementNotStableLongEnough,
    ExceptionTimeout,
)
from visiongui.driver.save_debug_screenshot import (
    FileNamePrefix,
    save_debug_screenshot,
)
from visiongui.driver.wait import WebDriverWait
from visiongui.element.DesktopElementImplementation import (
    DesktopElementImplementation,
)

logger = logging.getLogger(__name__)


def _is_stable(get_current_location, timeout, time_held_stable_on_screen):
    start_time = time.time()
    last_location = None
    stable_start = None
    found_once = False

    while time.time() - start_time < timeout:
        current_location = get_current_location()
        if current_location:
            found_once = True
            if (
                last_location
                and current_location.top_left == last_location.top_left
                and current_location.bottom_right == last_location.bottom_right
            ):
                if stable_start is None:
                    stable_start = time.time()
                elif time.time() - stable_start >= time_held_stable_on_screen:
                    logger.debug("[STABLE MATCH] Element remained stable.")
                    return current_location
            else:
                stable_start = None
            last_location = current_location
        else:
            last_location = None
            stable_start = None

        time.sleep(0.1)

    if found_once:
        raise ExceptionElementNotStableLongEnough(
            time_held_stable_on_screen=time_held_stable_on_screen,
            timeout=timeout,
        )
    raise ExceptionElementNotFound(timeout=timeout)


def _match_template(template, margin_of_error, monitor, screen_image, mask=None):
    # Ensure screen image has same number of channels as template
    if len(template.shape) == 2:
        if len(screen_image.shape) == 3:
            screen_image = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
    elif len(template.shape) == 3:
        if len(screen_image.shape) == 2:
            raise ValueError("Template is color but screen image is grayscale")
        if screen_image.shape[2] == 4:
            screen_image = cv2.cvtColor(screen_image, cv2.COLOR_BGRA2BGR)
        if screen_image.shape[2] != template.shape[2]:
            raise ValueError("Template and screen image have different channel counts")
    else:
        raise ValueError("Unsupported template shape")

    if screen_image.dtype != template.dtype:
        screen_image = screen_image.astype(template.dtype)

    if mask is not None:
        result = cv2.matchTemplate(
            screen_image,
            template,
            cv2.TM_SQDIFF_NORMED,
            mask=mask,
        )
    else:
        result = cv2.matchTemplate(screen_image, template, cv2.TM_SQDIFF_NORMED)

    min_val, _, min_loc, _ = cv2.minMaxLoc(result)

    if min_val <= margin_of_error:
        top_left = (min_loc[0] + monitor["left"], min_loc[1] + monitor["top"])
        bottom_right = (
            top_left[0] + template.shape[1],
            top_left[1] + template.shape[0],
        )
        logger.debug(
            f"[DEBUG] Template match found with confidence {min_val} at {top_left} [adjusted to absolute]",
        )
        return DesktopElementImplementation(
            top_left=top_left,
            bottom_right=bottom_right,
        )

    return False


def find_element_by_image(
    image_path: str,
    timeout: float,
    log_image_name: str,
    debug_output_base_path: str,
    margin_of_error: float,
    time_held_stable_on_screen: float,
    match_with_color: bool = False,
) -> DesktopElementImplementation:
    if not image_path or not os.path.isfile(image_path):
        raise FileNotFoundError(f"Template image not found: {image_path}")

    # [68566fb0-e936-48e3-8c87-c5b8735567df] If the image has an alpha channel, extract it to build a binary mask. This mask ensures that only opaque regions of the template are matched, ignoring transparent padding.
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    mask = None
    template = None
    if len(image.shape) == 3 and image.shape[2] == 4:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]

        if match_with_color:
            template = bgr
        else:
            template = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        # Alpha mask: white (255) where opaque, black (0) where transparent
        mask = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)[1]
    elif len(image.shape) == 3 and image.shape[2] == 3:
        if match_with_color:
            template = image
        else:
            template = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif len(image.shape) == 2:
        if match_with_color:
            template = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:
            template = image
    else:
        raise ValueError(f"Unsupported image shape: {image.shape}")

    if template is None:
        raise ValueError(f"Unable to read image at {image_path}")

    try:
        with mss() as sct:
            monitor = sct.monitors[1]

            def get_current_location():
                screenshot = sct.grab(monitor)
                screen_image = np.array(screenshot)
                return _match_template(
                    template=template,
                    margin_of_error=margin_of_error,
                    monitor=monitor,
                    screen_image=screen_image,
                    mask=mask,
                )

            if time_held_stable_on_screen > 0:
                result = _is_stable(
                    get_current_location,
                    timeout,
                    time_held_stable_on_screen,
                )
                return result
            try:
                result = WebDriverWait(timeout).until(
                    condition=get_current_location,
                )
                return result
            except ExceptionTimeout:
                save_debug_screenshot(
                    image_file_name_prefix=FileNamePrefix.FAIL,
                    log_image_name=log_image_name,
                    debug_output_base_path=debug_output_base_path,
                )
                raise ExceptionElementNotFound(timeout=timeout)

    except ExceptionElementNotStableLongEnough, ExceptionElementNotFound:
        save_debug_screenshot(
            image_file_name_prefix=FileNamePrefix.FAIL,
            log_image_name=log_image_name,
            debug_output_base_path=debug_output_base_path,
        )
        raise
