from flask import Flask, request, jsonify, redirect, render_template, session
from models import User, db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def index():
    return redirect('/register')


@app.route('/register', methods=["GET","POST"])
def register():

    form = RegisterForm()

    print(form.data)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect('/')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=["GET","POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_id"] = user.username  # keep logged in
            return redirect("/secret")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login.html', form=form)


@app.route('/secret')
def secret():

    if "user_id" not in session:
        return redirect('/')

    return "<body></body>"


