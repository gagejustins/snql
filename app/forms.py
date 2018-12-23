from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SneakerEventForm(FlaskForm):
    event_type = SelectField('EventName', validators=[DataRequired()])
    sneaker_id = SelectField('SneakerId', validators=[DataRequired()])
    submit = SubmitField('Log Event')    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
