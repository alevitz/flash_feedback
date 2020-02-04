"""Flask app for Flash Feedback"""
from flask import Flask, render_template, redirect, request, jsonify, session, flash
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, FeedbackForm

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
    """ Register User """

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

        return redirect(f'/users/{username}')

    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login User """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.get(username)

        if user and user.password == password:
            session['username'] = username
            return redirect(f'/users/{username}')

        else:
            form.username.errors = ['Bad name/password']

    return render_template('login.html', form=form)


@app.route("/users/<username>")
def show_user_details(username):
    """ User Details page, only accessible by that user """

    if 'username' not in session:
        flash("You have to be logged in to view!")
        return redirect('/')
    elif session['username'] != username:
        flash("You cant access other people's data you sith lord!")
        return redirect('/')
    else:
        user = User.query.get(username)

        return render_template("user_details.html", user=user)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):

    if 'username' not in session:
        flash("You have to be logged in to delete!")
    elif session['username'] != username:
        flash("You cant erase others from existence you sith lord!")
    else:
        user = User.query.get(username)
        db.session.delete(user)
        db.session.commit()
    return redirect('/')

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):

    if 'username' not in session:
        flash("You have to be logged in to add feedback!")
        return redirect("/")
    elif session['username'] != username:
        flash("You cant give feedback for others you sith lowlife!")
        return redirect("/")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{username}")

    return render_template('feedback.html', form=form)

@app.route('/logout')
def logout():
    """ Log currently logged in user out of session"""
    session.pop('username')

    return redirect('/')