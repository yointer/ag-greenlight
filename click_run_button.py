import pyautogui
import sys
import time
from pathlib import Path
from PIL import ImageGrab

# Configuration
SCRIPT_DIR = Path(__file__).parent
IMAGE_PATH = str(SCRIPT_DIR / "run_button.jpg")
CONFIDENCE = 0.8       # How closely it must match (0.0–1.0)
SCAN_INTERVAL = 5.0    # Seconds between scans
# Expected background colour: blue button (white text on blue bg)
# Tweak these HSV-style RGB thresholds if needed
COLOR_MIN = (0,   80,  130)   # min (R, G, B)
COLOR_MAX = (150, 180, 255)   # max (R, G, B)


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
    print(f"[✓] Clicked '{image_path}' at {centre}")
    return True


def main():
    print(f"[*] Scanning for '{IMAGE_PATH}' (blue background only) …")
    print("[*] Running forever. Press Ctrl+C to stop.")

    while True:
        try:
            clicked = find_and_click(IMAGE_PATH)
        except pyautogui.ImageNotFoundException:
            clicked = False
        except KeyboardInterrupt:
            print("\n[*] Stopped by user.")
            sys.exit(0)
        except Exception as exc:
            print(f"[!] Error during scan: {exc}", file=sys.stderr)
            clicked = False

        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
