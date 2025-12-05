# TimePal Models.py for SQLAlchemy
# Rewritten for clean structure + tasks with due dates + events table

import uuid
from flask_login import UserMixin
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ------------------------------------------------------------
# USERS TABLE
# ------------------------------------------------------------
class Users(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    tasks = db.relationship("Tasks", backref="user", lazy=True, cascade="all, delete-orphan")
    events = db.relationship("Events", backref="user", lazy=True, cascade="all, delete-orphan")

    # For Flask-Login compatibility
    @property
    def id(self):
        return self.user_id


# ------------------------------------------------------------
# TASKS TABLE (Kanban + Calendar tasks)
# ------------------------------------------------------------
class Tasks(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # NEW FIELDS ✨
    subject = db.Column(db.String(100))
    due_date = db.Column(db.Date)  # for monthly calendar display

    # "todo", "inprogress", or "done"
    status = db.Column(db.String(20), default="todo")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Used for AJAX, JSON, and calendar rendering"""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "subject": self.subject,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status,
        }


# ------------------------------------------------------------
# EVENTS TABLE (For Add Event modal + Calendar entries)
# ------------------------------------------------------------
class Events(db.Model):
    __tablename__ = "events"

    event_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.user_id"), nullable=False)

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # required for calendar
    event_date = db.Column(db.Date, nullable=False)

    start_time = db.Column(db.String(10))  # optional
    end_time = db.Column(db.String(10))    # optional

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Used for frontend calendar rendering"""
        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "event_date": self.event_date.isoformat(),
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
