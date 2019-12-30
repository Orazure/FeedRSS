from flask_wtf import FlaskForm
from wtforms import SelectField,PasswordField,BooleanField,SubmitField,StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Length
from wtfpeewee.orm import model_form
import wtforms
from test.models import User

SimpleUserForm=model_form(User)

class UserForm(FlaskForm):
    user_username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    user_password =PasswordField('Password', validators=[DataRequired(),Length(min=3, max=20)])



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')