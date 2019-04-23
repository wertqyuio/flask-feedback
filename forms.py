from wtforms import SelectField, StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    '''Form for registering users.'''

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
                            #  EqualTo('confirm', 
                            #                 message='''Passwords
                            #                             must match''')])
    email = StringField("Email", validators=[InputRequired()]) # can do email field later
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)]) # add msg ltr
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    '''Form for users to login.'''

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[DataRequired()])



