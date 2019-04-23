from flask import Flask, redirect, render_template, session
from models import User, db, connect_db, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm, FeedbackForm


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


@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()

    print(form.data)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email,
                                 first_name, last_name)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f'/users/{session["username"]}')

        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def username(username):
    if User.check_invalid_login(session, username):
        return redirect('/login')

    user = User.query.get(username)

    return render_template("user.html", user=user)


@app.route('/logout')
def logout():
    if "username" in session:
        session.pop("username")
    return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback(username):
    """ renders feedback form if user is logged in"""

    if User.check_invalid_login(session, username):
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content,
                                username=session["username"])
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{session["username"]}')
    else:
        return render_template("feedback.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def show_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if User.check_invalid_login(session, username):
        return redirect('/login')

    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        return redirect(f'/users/{session["username"]}')
    else:
        return render_template("edit_feedback.html", form=form,
                               feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if User.check_invalid_login(session, username):
        return redirect('/login')

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{session["username"]}')


@app.route('/users/<username>/delete')
def delete_user(username):
    user = User.query.get_or_404(username)

    if "username" not in session or user.username != session["username"]:
        return redirect('/login')

    session.pop("username")
    db.session.delete(user)
    db.session.commit()

    return redirect('/')
