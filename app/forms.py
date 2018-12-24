from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.data_scripts import data_hooks

class SneakerEventForm(FlaskForm):
    event_type = SelectField('Event Name', validators=[DataRequired()], choices=[('add', 'Add'), ('remove', 'Remove'), ('clean', 'Clean'), ('wear', 'Wear')])
    owner_id = SelectField('OwnerId', validators=[DataRequired()], choices= [(0,0)])
    sneaker_id = SelectField('SneakerId', validators=[DataRequired()], choices = [(1,1)])
    submit = SubmitField('Log Event')    

class SneakerAddForm(FlaskForm):
    sneaker_name = StringField(validators=[DataRequired()]) 
    color = StringField(validators=[DataRequired()])
    purchase_price = FloatField(validators=[DataRequired()]) 
    manufacturer_id = IntegerField(validators=[DataRequired()]) 
    submit = SubmitField('Add Sneaker') 

class SneakerRemoveForm(FlaskForm):
    removal_type = SelectField('Removal Type', validators=[DataRequired()], choices=[('sell', 'Sell'), ('trash', 'Trash'), ('give', 'Give')])
    sneaker_to_remove = SelectField('Sneaker Name', coerce=int, validators=[DataRequired()], choices=[result for result in data_hooks.list_available_sneakers(data_hooks.db_connect())])
    submit = SubmitField('Remove Sneaker')
