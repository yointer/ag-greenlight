import pyautogui
import sys
import time
from pathlib import Path
from PIL import ImageGrab

# Configuration
SCRIPT_DIR = Path(__file__).parent
IMAGES_DIR = SCRIPT_DIR / "images"
CONFIDENCE = 0.8       # How closely it must match (0.0–1.0)
SCAN_INTERVAL = 5.0    # Seconds between scans
SCROLL_INTERVAL = 300  # Seconds between scroll-to-reveal (5 minutes)
SCROLL_CLICKS = -5     # Negative = scroll down
# Expected background colour: blue button (white text on blue bg)
COLOR_MIN = (0,   80,  130)   # min (R, G, B)
COLOR_MAX = (150, 180, 255)   # max (R, G, B)

# Buttons to watch for — checked every scan cycle
# Each entry: (image_path, requires_color_check, click_offset, cooldown_sec)
#   click_offset = (x%, y%) offset from centre, as fraction of button size
#   cooldown_sec = minimum seconds between clicks (0 = no cooldown)
BUTTONS = [
    (IMAGES_DIR / "run_button.jpg",                    True,  (0, 0),    0),
    (IMAGES_DIR / "allow_this_conversation_button.jpg", True,  (0, 0),    0),
    (IMAGES_DIR / "request-popup.jpg",                  False, (0, 0),    0),
    (IMAGES_DIR / "expand_button.jpg",                  False, (0, 0),    0),
    (IMAGES_DIR / "bell_button.jpg",                    False, (-1.0, 0), 300),
]

TEXT_BOX = IMAGES_DIR / "text_box.jpg"
RUN_BUTTON_OBSTRUCTED = IMAGES_DIR / "run_button_obstructed.jpg"


def is_color_match(region) -> bool:
    """
    Grab the pixels inside `region` and check whether the average
    colour falls within the expected blue range.
    """
    x, y, w, h = region.left, region.top, region.width, region.height
    screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
    pixels = list(screenshot.getdata()) if not hasattr(screenshot, 'get_flattened_data') else list(screenshot.get_flattened_data())

    avg_r = sum(p[0] for p in pixels) / len(pixels)
    avg_g = sum(p[1] for p in pixels) / len(pixels)
    avg_b = sum(p[2] for p in pixels) / len(pixels)

    r_ok = COLOR_MIN[0] <= avg_r <= COLOR_MAX[0]
    g_ok = COLOR_MIN[1] <= avg_g <= COLOR_MAX[1]
    b_ok = COLOR_MIN[2] <= avg_b <= COLOR_MAX[2]
    return r_ok and g_ok and b_ok


def find_and_click(image_path: str, check_color: bool = True,
                   click_offset: tuple = (0, 0),
                   confidence: float = CONFIDENCE) -> bool:
    """
    Locate image on screen, optionally verify colour, then click.
    click_offset = (x%, y%) shifts the click point from centre,
    as a fraction of the matched region's width/height.
    Returns True if found and clicked. False otherwise.
    """
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location is None:
        return False

    if check_color and not is_color_match(location):
        return False

    centre = pyautogui.center(location)
    click_x = centre.x + int(click_offset[0] * location.width)
    click_y = centre.y + int(click_offset[1] * location.height)
    pyautogui.click(click_x, click_y)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [✓] Clicked '{Path(image_path).name}' at ({click_x}, {click_y})")
    return True


def scroll_to_reveal():
    """
    Find the text box, move the mouse up 1/4 of the screen from there,
    and scroll down to reveal any hidden Run buttons above the text box.
    """
    try:
        location = pyautogui.locateOnScreen(str(TEXT_BOX), confidence=CONFIDENCE)
    except pyautogui.ImageNotFoundException:
        return
    if location is None:
        return

    screen_w, screen_h = pyautogui.size()
    centre = pyautogui.center(location)
    # Move up 1/4 of the screen from the text box
    target_y = max(0, centre.y - screen_h // 4)
    pyautogui.moveTo(centre.x, target_y)
    pyautogui.scroll(SCROLL_CLICKS)


def clear_obstruction():
    """
    If the Run button is obstructed (e.g. by a down-arrow overlay),
    scroll up then back down to dismiss the overlay.
    """
    try:
        location = pyautogui.locateOnScreen(
            str(RUN_BUTTON_OBSTRUCTED), confidence=CONFIDENCE
        )
    except pyautogui.ImageNotFoundException:
        return
    if location is None:
        return

    centre = pyautogui.center(location)
    pyautogui.moveTo(centre.x, centre.y)
    pyautogui.scroll(3)    # scroll up to dismiss overlay
    time.sleep(0.3)
    pyautogui.scroll(-3)   # scroll back down
    time.sleep(0.3)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [↕] Cleared obstructed Run button")


def main():
    print(f"[*] Watching {len(BUTTONS)} button(s). Press Ctrl+C to stop.")

    last_scroll = 0
    last_click = {}  # per-button cooldown tracker

    while True:
        try:
            # Scroll down every SCROLL_INTERVAL seconds
            now = time.time()
            if now - last_scroll >= SCROLL_INTERVAL:
                scroll_to_reveal()
                last_scroll = now
                time.sleep(0.5)

            # Clear any obstructed Run button before scanning
            clear_obstruction()

            for btn_path, check_color, offset, cooldown in BUTTONS:
                # Skip if still in cooldown
                btn_key = str(btn_path)
                if cooldown > 0 and now - last_click.get(btn_key, 0) < cooldown:
                    continue
                try:
                    clicked = find_and_click(btn_key, check_color=check_color,
                                             click_offset=offset)
                    if clicked and cooldown > 0:
                        last_click[btn_key] = time.time()
                except pyautogui.ImageNotFoundException:
                    pass
        except KeyboardInterrupt:
            print("\n[*] Stopped by user.")
            sys.exit(0)
        except Exception as exc:
            print(f"[!] Error: {exc}", file=sys.stderr)

        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
