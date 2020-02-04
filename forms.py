from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional, Email, Length
from global_variables import USERNAME_LENGTH, EMAIL_LENGTH, FIRST_NAME_LENGTH, LAST_NAME_LENGTH


class RegisterForm(FlaskForm):
    """Form for registering new user."""

    username = StringField("Username", validators=[Length(max=USERNAME_LENGTH), InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[Email(), Length(max=EMAIL_LENGTH), InputRequired()])
    first_name = StringField("First Name", validators=[Length(max=FIRST_NAME_LENGTH), InputRequired()])
    last_name = StringField("Last Name", validators=[Length(max=LAST_NAME_LENGTH), InputRequired()])

class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField("Username", validators=[Length(max=USERNAME_LENGTH), InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])







