from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(60))
    email = db.Column('email', db.String(100), unique=True)
    password = db.Column('password', db.String(256))
    profile_picture = db.Column('profile_picture', db.String(100))
    high_score = db.Column('high_score', db.Integer, default=0)
    attempts = db.Column('attempts', db.Integer, default=0)

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    token = db.Column('token', db.String(32), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    date = db.Column(db.DateTime, default=datetime.now())
