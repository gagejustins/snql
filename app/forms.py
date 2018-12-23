from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SneakerEventForm(FlaskForm):
    event_type = SelectField('Event Name', validators=[DataRequired()], choices=[('Add', 'add'), ('Remove', 'remove'), ('Clean', 'clean'), ('Wear', 'wear')])
    owner_id = SelectField('OwnerId', validators=[DataRequired()], choices= [('0',0)])
    sneaker_id = SelectField('SneakerId', validators=[DataRequired()], choices = [('1',1)])
    submit = SubmitField('Log Event')    
