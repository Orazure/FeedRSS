from flask_wtf import FlaskForm
from wtforms import SelectField,PasswordField,BooleanField,SubmitField,StringField,DateField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Length,EqualTo
from wtfpeewee.orm import model_form
import wtforms
from test.models import User,feed

SimpleUserForm=model_form(User)
SimpleFeedForm=model_form(feed)

class UserForm(FlaskForm):
    user_username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    user_password = PasswordField(' Password', validators=[DataRequired(),EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField(' Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class FeedForm(FlaskForm):
    feed_nom = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)])
    feed_url = StringField('Url', validators=[DataRequired()])
    feed_date=DateField('Date ', validators=[DataRequired()])
