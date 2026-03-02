import json
import datetime
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta, date

app = Flask(__name__)

DATA_FILE = "data.json"


def load_sessions():
    """Load sessions from JSON file, always return a list."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else [data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_sessions(data):
    """Save list of sessions back to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)


def compute_stats(data):
    """Compute stats from session list."""
    total_sessions = len(data)
    total_minutes = round(sum(int(session.get("duration", 0)) for session in data))
    avg_focus = (
        round(sum(int(session.get("focus_level", 0)) for session in data)) / total_sessions
        if total_sessions > 0 else 0
    )
    longest_session = max((int(session.get("duration", 0)) for session in data), default=0)

    return total_sessions, total_minutes, avg_focus, longest_session


@app.route("/log", methods=["GET"])
def log():
    data = load_sessions()
    total_sessions, total_minutes, avg_focus, longest_session = compute_stats(data)

    # ---- Heatmap (last 28 days) ----
    today = date.today()
    days = [today - timedelta(days=i) for i in range(27, -1, -1)]  # oldest -> newest

    minutes_by_day = {d: 0 for d in days}

    for s in data:
        try:
            d = datetime.strptime(s["date"], "%b-%d-%Y %I:%M").date()
        except Exception:
            continue

        if d in minutes_by_day:
            minutes_by_day[d] += int(s.get("duration", 0))

    heatmap_tiles = []
    for d in days:
        mins = minutes_by_day[d]
        if mins == 0:
            level = 0
        elif mins < 60:
            level = 1
        else:
            level = 2

        heatmap_tiles.append({
            "date_label": d.strftime("%b %d"),
            "minutes": mins,
            "level": level
        })

    return render_template(
        "log.html",
        total_sessions=total_sessions,
        total_minutes=total_minutes,
        avg_focus=avg_focus,
        longest_session=longest_session,
        heatmap_tiles=heatmap_tiles
    )


@app.route("/log", methods=["POST"])
def log_post():
    curr_date = datetime.datetime.now().strftime("%b-%d-%Y %I:%M")

    task = (request.form.get("task") or "").strip()
    duration = request.form.get("duration")
    focus_level = request.form.get("focus")

    # Basic validation (simple + safe)
    if not task:
        return redirect(url_for("log"))

    try:
        duration_int = int(duration)
        focus_int = int(focus_level)
    except (TypeError, ValueError):
        return redirect(url_for("log"))

    if duration_int <= 0 or focus_int < 1 or focus_int > 10:
        return redirect(url_for("log"))

    data = load_sessions()
    data.append({
        "date": curr_date,
        "task": task,
        "duration": duration_int,
        "focus_level": focus_int
    })
    save_sessions(data)

    # Redirect so refresh doesn't re-submit the form
    return redirect(url_for("log"))


@app.route("/sessions")
def sessions():
    data = load_sessions()
    return render_template("sessions.html", sessions=data)


if __name__ == "__main__":
    app.run(debug=True)

