from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

DATABASE = 'timepal.db'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + DATABASE
db = SQLAlchemy(app)

class Tasks(db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.text)
    task_type_id = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String, primary_key=True)  # TEXT PRIMARY KEY
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    failed_login_attempts = db.Column(db.Integer, nullable=False, default=0)

    last_failed_login = db.Column(db.DateTime, default=None, nullable=True)
    last_login = db.Column(db.DateTime, default=None, nullable=True)

    password_reset_token = db.Column(db.String, default=None, nullable=True)
    password_reset_expiry = db.Column(db.DateTime, default=None, nullable=True)

