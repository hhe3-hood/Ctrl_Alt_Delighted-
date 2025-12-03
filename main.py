import sqlite3
import calendar
import datetime
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_


# Info Found Here: https://www.geeksforgeeks.org/python/how-to-add-authentication-to-your-app-with-flask-login/
# https://www.geeksforgeeks.org/python/connect-flask-to-a-database-with-flask-sqlalchemy/

DATABASE = 'timepal.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Flask Route Listings -- Move to routes.py later
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/monthly")
def monthly():

    today = datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)
    start_of_month = today.replace(day=1)
    end_of_month = today.replace(day=days_in_month)

    month_tasks = (
        Tasks.query
        .filter(
            or_(
                and_(  # start_date between range_start and range_end
                    Tasks.start_date >= start_of_month,
                    Tasks.start_date <= end_of_month,
                ),
                and_(  # end_date between (or equal to) range_start and range_end
                    Tasks.end_date >= start_of_month,
                    Tasks.end_date <= end_of_month,
                ),
            )
        )
        .all()
    )

    return render_template("monthly.html", Tasks=month_tasks)

@app.route("/")
def home():
    return render_template("login.html")

if __name__ == "__main__":

    app.run()

