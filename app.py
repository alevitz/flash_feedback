"""Flask app for Flash Feedback"""
from flask import Flask, render_template, redirect, request, jsonify, session, flash
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "DHFGUSRGHUISHGUISHG"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)
connect_db(app)
db.create_all()

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name) 

        db.session.add(user)
        db.session.commit()

        session['username'] = username

        return redirect('/secret')

    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.get(username)

        if user and user.password == password:
            session['username'] = username
            return redirect('/secret')

        else:
            form.username.errors = ['Bad name/password']

    return render_template('login.html', form=form)


@app.route("/secret")
def secret():

    if 'username' not in session:
        flash("You have to be logged in to view!")
        return redirect('/')
    else:
        return ("You made it here!")