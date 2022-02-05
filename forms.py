from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Passwrod')
    email = StringField('Email ID')
    first_name = StringField('First_Name')
    last_name = StringField('Last_Name')

 

class LoginForm(FlaskForm):

    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class FeedbackForm(FlaskForm):

    title = StringField('Feedback Title', validators=[InputRequired()])
    content = StringField('Feedback Content', validators=[InputRequired()])