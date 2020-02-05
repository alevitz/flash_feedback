"""Models for Flash_feedback app."""

from flask_sqlalchemy import SQLAlchemy
from global_variables import USERNAME_LENGTH, EMAIL_LENGTH, FIRST_NAME_LENGTH, LAST_NAME_LENGTH, TITLE_LENGTH
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


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

    feedbacks = db.relationship(
        'Feedback', backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password and return user."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists and password is correct.
            Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


class Feedback(db.Model):
    """ Feedback Entry """

    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(TITLE_LENGTH), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(USERNAME_LENGTH),
                         db.ForeignKey('users.username'))

