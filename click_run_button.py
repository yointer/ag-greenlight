import pyautogui
import sys
import time

# Configuration
IMAGE_PATH = "run_button.jpg"
CONFIDENCE = 0.8       # How closely it must match (0.0–1.0)
SCAN_INTERVAL = 5.0    # Seconds between scans when looping
TIMEOUT = None         # Run forever


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

        if not clicked:
            print(f"    Not found. Retrying in {SCAN_INTERVAL}s …")

        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
