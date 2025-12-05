import os
import sqlite3
import calendar
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_

from models import db, Users, Tasks, Events


# ======================================================
#  INIT APP
# ======================================================

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "timepal.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


# ======================================================
#  LOGIN MANAGER
# ======================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)



# ======================================================
#  CREATE DB IF MISSING (bootstrap)
# ======================================================

def init_db():
    if not os.path.exists(DATABASE):
        with app.app_context():
            db.create_all()
            print("✔ Database created!")


with app.app_context():
    init_db()


# ======================================================
#  AUTH ROUTES
# ======================================================

@app.route("/")
def home():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password_input = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password_input):
            login_user(user)
            return redirect(url_for("monthly"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password_input = request.form.get("password")

        hashed = generate_password_hash(password_input, method="pbkdf2:sha256")

        new_user = Users(username=username, password_hash=hashed)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ======================================================
#  MONTHLY PAGE
# ======================================================

@app.route("/monthly")
@login_required
def monthly():
    today = datetime.now()

    # ------ TASKS ------
    tasks = Tasks.query.filter_by(user_id=current_user.user_id).all()
    monthly_tasks = [
        t.to_dict()
        for t in tasks
        if t.due_date and t.due_date.year == today.year and t.due_date.month == today.month
    ]

    # ------ EVENTS ------
    events = Events.query.filter_by(user_id=current_user.user_id).all()
    monthly_events = [
        e.to_dict()
        for e in events
        if e.event_date.year == today.year and e.event_date.month == today.month
    ]

    return render_template(
        "monthly.html",
        month_tasks=monthly_tasks,
        month_events=monthly_events
    )



# ======================================================
#  TASKS PAGE
# ======================================================

@app.route("/tasks")
@login_required
def tasks_page():
    return render_template("tasks.html")


# ======================================================
#  TASK API ROUTES
# ======================================================

@app.route("/api/tasks")
@login_required
def api_get_tasks():
    tasks = Tasks.query.filter_by(user_id=current_user.user_id).all()
    return jsonify([t.to_dict() for t in tasks])


@app.route("/api/tasks/add", methods=["POST"])
@login_required
def api_add_task():
    data = request.json

    new_task = Tasks(
        user_id=current_user.user_id,
        title=data.get("title"),
        description=data.get("description"),
        subject=data.get("subject"),
        due_date=datetime.strptime(data["due_date"], "%Y-%m-%d").date() if data.get("due_date") else None,
        status="todo"
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict())


@app.route("/api/tasks/edit", methods=["POST"])
@login_required
def api_edit_task():
    data = request.json
    task = Tasks.query.get(data.get("task_id"))

    if not task:
        return {"error": "Task not found"}, 404

    task.title = data.get("title")
    task.description = data.get("description")
    task.subject = data.get("subject")
    task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date() if data.get("due_date") else None

    db.session.commit()
    return jsonify(task.to_dict())


@app.route("/api/tasks/delete", methods=["POST"])
@login_required
def api_delete_task():
    task_id = request.json.get("task_id")
    task = Tasks.query.get(task_id)

    if not task:
        return {"error": "Task not found"}, 404

    db.session.delete(task)
    db.session.commit()
    return {"success": True}


@app.route("/api/tasks/update_status", methods=["POST"])
@login_required
def api_update_task_status():
    data = request.json
    task = Tasks.query.get(data.get("task_id"))

    if not task:
        return {"error": "Task not found"}, 404

    task.status = data.get("status")
    db.session.commit()
    return {"success": True}


# ======================================================
#  EVENT API ROUTES
# ======================================================

@app.route("/api/events/add", methods=["POST"])
@login_required
def api_add_event():
    data = request.json

    new_event = Events(
        user_id=current_user.user_id,
        title=data.get("title"),
        description=data.get("description"),
        event_date=datetime.strptime(data["event_date"], "%Y-%m-%d").date(),
        start_time=data.get("start_time"),
        end_time=data.get("end_time")
    )

    db.session.add(new_event)
    db.session.commit()
    return jsonify(new_event.to_dict())


@app.route("/api/events/edit", methods=["POST"])
@login_required
def api_edit_event():
    data = request.json
    event = Events.query.get(data.get("event_id"))

    if not event:
        return {"error": "Event not found"}, 404

    event.title = data.get("title")
    event.description = data.get("description")
    event.event_date = datetime.strptime(data["event_date"], "%Y-%m-%d").date()
    event.start_time = data.get("start_time")
    event.end_time = data.get("end_time")

    db.session.commit()
    return jsonify(event.to_dict())


@app.route("/api/events/delete", methods=["POST"])
@login_required
def api_delete_event():
    event_id = request.json.get("event_id")
    event = Events.query.get(event_id)

    if not event:
        return {"error": "Event not found"}, 404

    db.session.delete(event)
    db.session.commit()
    return {"success": True}


@app.route("/about")
def about():
    return render_template("about.html")


# ======================================================
#  RUN APP
# ======================================================

if __name__ == "__main__":
    app.run(debug=True)
