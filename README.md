# ag-greenlight

A PyAutoGUI script that scans your screen for UI buttons and clicks them automatically. Includes scroll-to-reveal for hidden buttons and colour verification for precise matching.

## Project Structure

```
ag-greenlight/
├── click_run_button.py      # Main script
├── images/                  # Reference button screenshots
│   ├── run_button.jpg
│   ├── allow_this_conversation_button.jpg
│   ├── allow_once_button.jpg
│   ├── text_box.jpg
│   └── prompt_done.jpg
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7+

```bash
pip install -r requirements.txt
```

## Usage

1. Place tightly-cropped screenshots of buttons you want to auto-click into the `images/` folder.
2. Update the `BUTTONS` list in `click_run_button.py` if adding new targets.
3. Run:

```bash
python click_run_button.py
```

The script runs forever (Ctrl+C to stop). Each cycle it:
- Scrolls down near the text box to reveal hidden buttons
- Scans for each button in the `BUTTONS` list
- Clicks any match that passes the blue colour check

## Configuration

Edit the constants at the top of `click_run_button.py`:

| Variable | Default | Description |
|---|---|---|
| `CONFIDENCE` | `0.8` | Match sensitivity (0.0–1.0). Lower = fuzzier |
| `SCAN_INTERVAL` | `5.0` | Seconds between scans |
| `SCROLL_CLICKS` | `-5` | Scroll amount (negative = down) |
| `COLOR_MIN` | `(0, 80, 130)` | Min RGB for blue colour check |
| `COLOR_MAX` | `(150, 180, 255)` | Max RGB for blue colour check |
