from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, DataRequired, Length


class RegisterForm(FlaskForm):
    '''Form for registering users.'''

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[InputRequired()])
    # can do email field later
    first_name = StringField("First Name", validators=[InputRequired(),
                             Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(),
                            Length(max=30)])


class LoginForm(FlaskForm):
    '''Form for users to login.'''

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class FeedbackForm(FlaskForm):
    '''Form for adding user feedback.'''

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])
