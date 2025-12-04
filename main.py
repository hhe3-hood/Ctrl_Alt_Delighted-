# TimePal Main.py with flask paths and logic
# Author: Lindsey Hilditch & Team
# Date: 2025-12-2

import os
import sqlite3
import calendar
from datetime import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_
from models import Users, Tasks
from models import db


# Info Found Here: https://www.geeksforgeeks.org/python/how-to-add-authentication-to-your-app-with-flask-login/
# https://www.geeksforgeeks.org/python/connect-flask-to-a-database-with-flask-sqlalchemy/

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "timepal.db")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

def init_db_from_sql():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        sql_path = os.path.join(BASE_DIR, "tp_database.sql")
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
        conn.commit()
        conn.close()


# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


# Flask Route Listings -- Move to routes.py later
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password_hash = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password_hash):
            login_user(user)
            return redirect(url_for("monthly"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password_hash = request.form["password"]
        password_hash = generate_password_hash(password_hash)
        new_user = Users(username=username, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/monthly")
def monthly():

    # defaults to current month based on date
    today = datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]  # get number of days
    start_of_month = datetime(today.year, today.month, 1, 0, 0, 0)
    end_of_month = datetime(today.year, today.month, days_in_month, 23, 59, 59)

    month_tasks = (
        Tasks.query
        .order_by(Tasks.start_time)
        .filter(
            or_(
                and_(  # start_date between range_start and range_end
                    Tasks.start_time >= start_of_month,
                    Tasks.start_time <= end_of_month,
                ),
                and_(  # end_date between (or equal to) range_start and range_end
                    Tasks.end_time >= start_of_month,
                    Tasks.end_time <= end_of_month,
                ),
            )
        )
    )

    # Converting the model to list to be consumed by javascript/ json
    month_tasks_data = [
        {
            "task_id": t.task_id,
            "title": t.title,
            "description": t.description,
            "start_time": t.start_time.isoformat() if t.start_time else None,
            "end_time": t.end_time.isoformat() if t.end_time else None,
            "is_completed": t.is_completed,
            "day_numb": t.start_time.day,
            "s_time": t.start_time.strftime("%I:%M %p"),
        }
        for t in month_tasks
    ]

    return render_template("monthly.html",month_tasks=month_tasks_data)

@app.route("/")
def home():
    return render_template("login.html")

if __name__ == "__main__":
    init_db_from_sql()
    app.run(debug=True)






