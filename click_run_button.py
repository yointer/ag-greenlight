import pyautogui
import sys
import time

# Configuration
IMAGE_PATH = "run_button.jpg"
CONFIDENCE = 0.8       # How closely it must match (0.0–1.0)
SCAN_INTERVAL = 5.0    # Seconds between scans when looping
TIMEOUT = None           # Max seconds to wait before giving up (None = wait forever)


def find_and_click(image_path: str, confidence: float = CONFIDENCE) -> bool:
    """
    Locate image on screen and click its centre.
    Returns True if found and clicked, False otherwise.
    """
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    if location is None:
        return False

    centre = pyautogui.center(location)
    pyautogui.click(centre)
    print(f"[✓] Clicked '{image_path}' at {centre}")
    return True


def main():
    print(f"[*] Scanning for '{IMAGE_PATH}' …")

    start = time.time()
    while True:
        try:
            clicked = find_and_click(IMAGE_PATH)
        except pyautogui.ImageNotFoundException:
            clicked = False
        except Exception as exc:
            print(f"[!] Error during scan: {exc}", file=sys.stderr)
            sys.exit(1)

        if clicked:
            break

        elapsed = time.time() - start
        if TIMEOUT is not None and elapsed >= TIMEOUT:
            print(f"[✗] '{IMAGE_PATH}' not found within {TIMEOUT}s — giving up.")
            sys.exit(1)

        print(f"    Not found yet ({elapsed:.0f}s elapsed). Retrying in {SCAN_INTERVAL}s …")
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
