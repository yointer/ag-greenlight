import pyautogui
import sys
import time
from pathlib import Path
from PIL import ImageGrab

# Configuration
SCRIPT_DIR = Path(__file__).parent
CONFIDENCE = 0.8       # How closely it must match (0.0–1.0)
SCAN_INTERVAL = 5.0    # Seconds between scans
SCROLL_CLICKS = -5     # Negative = scroll down
# Expected background colour: blue button (white text on blue bg)
COLOR_MIN = (0,   80,  130)   # min (R, G, B)
COLOR_MAX = (150, 180, 255)   # max (R, G, B)

# Buttons to watch for — checked every scan cycle
BUTTONS = [
    SCRIPT_DIR / "run_button.jpg",
    SCRIPT_DIR / "allow_this_conversation_button.jpg",
]

TEXT_BOX = SCRIPT_DIR / "text_box.jpg"


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


def find_and_click(image_path: str, confidence: float = CONFIDENCE) -> bool:
    """
    Locate image on screen, verify colour, then click its centre.
    Returns True if found, colour-verified, and clicked. False otherwise.
    """
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location is None:
        return False

    if not is_color_match(location):
        return False

    centre = pyautogui.center(location)
    pyautogui.click(centre)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [✓] Clicked '{Path(image_path).name}' at {centre}")
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


def main():
    print(f"[*] Watching {len(BUTTONS)} button(s). Press Ctrl+C to stop.")

    while True:
        try:
            # Scroll down to reveal hidden buttons
            scroll_to_reveal()
            time.sleep(0.5)

            for btn in BUTTONS:
                try:
                    find_and_click(str(btn))
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
