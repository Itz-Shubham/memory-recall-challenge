from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
#   id = db.Column(db.String(), primary_key=True, default=lambda: str(uuid.uuid4()))
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(60))
    email = db.Column('email', db.String(100), unique=True)
    password = db.Column('password', db.String(256))
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'
    token = db.Column('token', db.String(32), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    date = db.Column(db.DateTime, default=datetime.now())