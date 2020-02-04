"""Models for Flash_feedback app."""

from flask_sqlalchemy import SQLAlchemy
from global_variables import USERNAME_LENGTH, EMAIL_LENGTH, FIRST_NAME_LENGTH, LAST_NAME_LENGTH


db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User"""

    __tablename__ = "users"

    username = db.Column(db.String(USERNAME_LENGTH), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(EMAIL_LENGTH), nullable=False, unique=True)
    first_name = db.Column(db.String(FIRST_NAME_LENGTH), nullable=False)
    last_name = db.Column(db.String(LAST_NAME_LENGTH), nullable=False)
