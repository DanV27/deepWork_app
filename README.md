# DeepWork App

A local Flask web application for tracking deep work sessions. Log tasks, run a built-in timer, rate your focus, and watch your XP and level grow over time.

## Features

- **Integrated Pomodoro timer** — pick 25, 45, 60 min or a custom duration; the save form only unlocks once the timer completes, so your logged duration always reflects real time spent
- **Session logging** — record the task name, focus score (1–10), and a freeform journal reflection per session
- **XP & levelling system** — earn XP equal to `duration × focus` per session; maintain a daily streak longer than 1 day for a 1,000 XP bonus per streak day; level up from 1 to 100 as you accumulate XP
- **Sticky XP bar** — always-visible bar at the top of every page showing your current level, XP progress, and XP needed for the next level; animates on page load and flashes with a level-up banner when you level up
- **Stats dashboard** — total sessions, total focus time, average focus score, and longest session
- **Focus heatmap** — 28-day rolling heatmap showing daily activity with a current streak counter
- **Flash messages** — success and error feedback on form submission, auto-dismissed after a few seconds
- **Session history** — browse all previously logged sessions at `/sessions`
- **SQLite persistence** — data stored in `instance/deepwork.db` via SQLAlchemy (auto-created on first run)

## Prerequisites

- Python 3.7 or newer
- Flask
- Flask-SQLAlchemy

## Installation

```bash
cd deepWork_app

# optional but recommended: create a virtual environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

# install dependencies
pip install flask flask-sqlalchemy
```

## Running the App

```bash
python main.py
```

The server starts at `http://localhost:5000` and redirects automatically to the log page. No login required — designed for local desktop use.

## Project Structure

```
deepWork_app/
├── main.py              # Flask app, routes, XP logic, DB models
├── instance/
│   └── deepwork.db      # SQLite database (auto-created)
├── templates/
│   ├── base.html        # shared layout: XP bar, nav, flash messages
│   ├── log.html         # timer + session log form + heatmap
│   └── sessions.html    # full session history table
├── static/
│   └── styles.css       # all styles including XP bar and timer
└── README.md
```

## XP & Level System

| Source | XP earned |
|---|---|
| Completing a session | `duration (min) × focus score` |
| Daily streak bonus (streak > 1) | `1,000 XP × (streak − 1)` |

Each level requires `level × 500 XP` to complete. The streak bonus is dynamic — it reflects your current active streak and resets if you miss a day, which keeps the motivation to stay consistent.

## Usage Notes

- The save button is locked until the timer finishes — this enforces honest session tracking
- The level-up banner uses `localStorage` to detect when you've gained a level and shows once per level-up
- `debug=True` is enabled in `main.py` — fine for local use, remove it before any public deployment
- The secret key in `main.py` is a placeholder; change it if you ever expose the app on a network

## License

MIT License.
