from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    score_assiduite = db.Column(db.Integer, default=0)

    # Relations
    goals = db.relationship(
        'Goal',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    habits = db.relationship(
        'Habit',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    todos = db.relationship(
        'TodoItem',
        backref='user',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    habits = db.relationship(
        'Habit',
        backref='goal',
        lazy=True,
        cascade="all, delete-orphan"
    )


class Habit(db.Model):
    __tablename__ = 'habits'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)

    title = db.Column(db.String(150), nullable=False)
    why = db.Column(db.String(500), nullable=True)

    expected_result = db.Column(db.String(500), nullable=True)

    schedule_days = db.Column(db.String(100), nullable=True)
    schedule_time = db.Column(db.String(100), nullable=True)

    duration = db.Column(db.Integer, nullable=True)  # en minutes

    max_streak = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)

    logs = db.relationship(
        'HabitLog',
        backref='habit',
        lazy=True,
        cascade="all, delete-orphan"
    )


class HabitLog(db.Model):
    __tablename__ = 'habit_logs'

    id = db.Column(db.Integer, primary_key=True)

    habit_id = db.Column(
        db.Integer,
        db.ForeignKey('habits.id'),
        nullable=False
    )

    date_completed = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class TodoItem(db.Model):
    __tablename__ = 'todo_items'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=True)

    is_completed = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )