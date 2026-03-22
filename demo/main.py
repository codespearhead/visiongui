import os
import re
from pathlib import Path
from PIL import Image, ImageDraw
from visiongui.driver.DesktopDriverImplementation import DesktopDriverImplementation


OS_PROCESS_KILL_TIMEOUT = 5

DEMO__OUTPUT__DIR = os.path.join("demo__output", Path(__file__).stem)
Path(DEMO__OUTPUT__DIR).mkdir(parents=True, exist_ok=True)

IMAGE__CIRCLE__RED__NAME = "IMAGE__CIRCLE__RED"
IMAGE__CIRCLE__RED__PATH = os.path.join(
    DEMO__OUTPUT__DIR, f"{IMAGE__CIRCLE__RED__NAME}.png"
)
img_size = (200, 200)
circle_img = Image.new("RGB", img_size, "white")
draw = ImageDraw.Draw(circle_img)
draw.ellipse((50, 50, 150, 150), fill="red")
circle_img.save(IMAGE__CIRCLE__RED__PATH)

dummy_gui_code_snippet = f"""
import tkinter as tk
root = tk.Tk()
root.title('{Path(__file__).stem}')
img = tk.PhotoImage(file=r"{IMAGE__CIRCLE__RED__PATH}")
label = tk.Label(root, image=img)
label.image = img
label.pack()
root.mainloop()
"""
dummy_gui_code_snippet__file_path = os.path.join(DEMO__OUTPUT__DIR, "dummy_gui.py")
with open(dummy_gui_code_snippet__file_path, "wb") as f:
    f.write(dummy_gui_code_snippet.encode("utf-8"))


desktop_driver = DesktopDriverImplementation()

desktop_driver.launch_process(cmd=["python", dummy_gui_code_snippet__file_path])
desktop_window = desktop_driver.find_window(
    title=re.compile(f"^{re.escape(Path(__file__).stem)}$"),
    timeout=5,
    should_exist=True,
)
desktop_driver.switch_to(target_window=desktop_window)

desktop_driver.find_element_by_image(
    image_path=IMAGE__CIRCLE__RED__PATH,
    log_image_name=IMAGE__CIRCLE__RED__NAME,
    timeout=5,
    margin_of_error=0.01,
    time_held_stable_on_screen=1.0,
    debug_output_base_path=DEMO__OUTPUT__DIR,
    match_with_color=True,
)

desktop_driver.close(OS_PROCESS_KILL_TIMEOUT=OS_PROCESS_KILL_TIMEOUT)
