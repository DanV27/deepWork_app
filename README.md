# DeepWork App

A lightweight Flask web application for tracking "deep work" sessions. Users can log tasks, duration, and focus level; the app stores entries in a simple JSON file and displays basic statistics.

## Features

- Log deep work sessions with task description, duration (in minutes), and focus level (1–10).
- View aggregate statistics: total sessions, total focus time, average focus, and longest session.
- Browse all previously logged sessions.
- No database required — data is persisted in `data.json`.

## Prerequisites

- Python 3.7 or newer
- [Flask](https://pypi.org/project/Flask/)

## Installation

```bash
cd /Users/daniel/Desktop/deepWork_app
# optional virtual environment
python -m venv venv
source venv/bin/activate   # on macOS/Linux

# install dependencies
pip install flask
# (or: pip install -r requirements.txt if you add one)
```

## Running the Application

```bash
python main.py
```

By default the server listens on `http://127.0.0.1:5000` (or `localhost:5000`).

- Go to `/log` to submit a new session.
- Use the "View Sessions" link to jump to `/sessions` and see all entries.

## Project Structure

```
deepWork_app/
├── data.json          # persistent store for logged sessions (created automatically)
├── main.py            # the Flask application
├── templates/         # HTML templates used by the app
│   ├── log.html       # form + stats page
│   ├── sessions.html  # list of logged sessions
│   └── index.html     # currently unused placeholder
├── static/            # static assets (CSS, etc.)
│   └── styles.css     # currently empty
└── README.md          # this file
```

## Usage Notes

- The app performs basic validation: tasks cannot be blank, duration must be positive, and focus must be between 1 and 10.
- Refreshing the `/log` page after submitting a session will not trigger a duplicate entry thanks to the post/redirect/get pattern.
- Debug mode is enabled in `main.py` for development; remove `debug=True` for production.

## Extending the App

You can add features such as:

- Persistent storage using SQLite or another database.
- User authentication to separate sessions.
- Visualization of statistics with charts.
- CSS styling and front‑end enhancements.

## Contributing

Feel free to fork the repository, issue bug reports, or submit pull requests.

## License

This project is released under the MIT License. See `LICENSE` for details.

