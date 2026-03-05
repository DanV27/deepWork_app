import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date

app = Flask(__name__)

# Ensure instance folder exists (so SQLite file can be created)
os.makedirs(app.instance_path, exist_ok=True)

db_path = os.path.join(app.instance_path, "deepwork.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    focus = db.Column(db.Integer, nullable=False)
    journal = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

def load_sessions():
    return Session.query.order_by(Session.created_at.desc()).all()

def compute_stats(sessions):
    total_sessions = len(sessions)
    total_minutes = sum(s.duration for s in sessions)
    avg_focus = round(sum(s.focus for s in sessions) / total_sessions, 2) if total_sessions else 0
    longest_session = max((s.duration for s in sessions), default=0)
    return total_sessions, total_minutes, avg_focus, longest_session

@app.route("/log", methods=["GET"])
def log():
    sessions = load_sessions()
    total_sessions, total_minutes, avg_focus, longest_session = compute_stats(sessions)

    today = date.today()
    days = [today - timedelta(days=i) for i in range(27, -1, -1)]
    minutes_by_day = {d: 0 for d in days}
    is_today = {d: d == today for d in days}

    for s in sessions:
        d = s.created_at.date()
        if d in minutes_by_day:
            minutes_by_day[d] += int(s.duration)

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
            "level": level,
            "is_today": (d == today)
        })

    current_streak = 0
    for d in reversed(days):
        if minutes_by_day[d] > 0:
            current_streak += 1
        else:
            break

    return render_template(
        "log.html",
        total_sessions=total_sessions,
        total_minutes=total_minutes,
        avg_focus=avg_focus,
        longest_session=longest_session,
        heatmap_tiles=heatmap_tiles,
        current_streak=current_streak,
        is_today=is_today,
    )

@app.route("/log", methods=["POST"])
def log_post():
    task = (request.form.get("task") or "").strip()
    duration = request.form.get("duration")
    focus_level = request.form.get("focus")
    journal = request.form.get("journal", "").strip()

    if not task:
        return redirect(url_for("log"))

    try:
        duration_int = int(duration)
        focus_int = int(focus_level)
    except (TypeError, ValueError):
        return redirect(url_for("log"))

    if duration_int <= 0 or focus_int < 1 or focus_int > 10:
        return redirect(url_for("log"))

    new_session = Session(
        task=task,
        duration=duration_int,
        focus=focus_int,
        journal=journal
    )
    db.session.add(new_session)
    db.session.commit()

    return redirect(url_for("log"))

@app.route("/sessions")
def sessions():
    sessions = load_sessions()
    return render_template("sessions.html", sessions=sessions)

if __name__ == "__main__":
    app.run(debug=True)