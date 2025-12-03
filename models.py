import uuid
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tasks(UserMixin,db.Model):
    __tablename__ = "tasks"
    task_id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),  # UUID stored as TEXT
    )
    user_id = db.Column(db.String(36), nullable=False)
    task_type_id = db.Column(db.Integer)
    color_scheme_id = db.Column(db.Integer)

    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)

    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    reminder_time = db.Column(db.DateTime)

    is_completed = db.Column(db.Integer, default=0)  # 0/1 as in schema

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.title}>"

class Users(UserMixin,db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.String(36), primary_key=True,default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    email_verified = db.Column(db.Integer, default=0)
    failed_login_attempts = db.Column(db.Integer, default=0)

    last_failed_login = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)

    password_reset_token = db.Column(db.String, nullable=True)
    password_reset_expiry = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,)

    @property
    def id(self):
        return self.user_id

    def __repr__(self):
        return f"<User {self.username}>"

