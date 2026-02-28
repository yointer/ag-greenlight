# ag-greenlight

A PyAutoGUI script that scans your screen for a button image and clicks it automatically.

## Requirements

- Python 3.7+
- pyautogui
- opencv-python (required for the `confidence` parameter)

```bash
pip install -r requirements.txt
```

## Usage

1. Take a screenshot of the button you want to click and save it as `run_button.jpg` in the same directory as the script.
2. Run the script:

```bash
python click_run_button.py
```

The script will scan the screen every second, click the button as soon as it's found, then exit.

## Configuration

Edit the constants at the top of `click_run_button.py`:

| Variable | Default | Description |
|---|---|---|
| `IMAGE_PATH` | `"run_button.jpg"` | Path to the reference image |
| `CONFIDENCE` | `0.8` | Match sensitivity (0.0–1.0). Lower = fuzzier |
| `SCAN_INTERVAL` | `1.0` | Seconds between scans |
| `TIMEOUT` | `30` | Seconds before giving up (`None` = wait forever) |

## Tips

- If the button isn't detected, try lowering `CONFIDENCE` to `0.7`.
- Crop the screenshot tightly around the button for better accuracy.
