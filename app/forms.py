from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired
from app.data_scripts import data_hooks

class SneakerEventForm(FlaskForm):
    event_type = SelectField('Event Name', validators=[DataRequired()], choices=[('clean', 'Clean'), ('wear', 'Wear'), ('walk', 'Walk')])
    #owner_id = SelectField('OwnerId', coerce=int, validators=[DataRequired()], choices= [(0,0)])
    sneaker_id = SelectField('Sneaker Name', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Log Event')    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sneaker_id.choices = data_hooks.list_available_sneakers(data_hooks.db_connect())

class SneakerAddForm(FlaskForm):
    sneaker_name = StringField(validators=[DataRequired()]) 
    color = StringField(validators=[DataRequired()])
    purchase_price = FloatField(validators=[DataRequired()]) 
    manufacturer_id = SelectField('Manufacturer Name', coerce=int, validators=[DataRequired()]) 
    submit = SubmitField('Add Sneakers') 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.manufacturer_id.choices = data_hooks.list_available_manufacturers(data_hooks.db_connect())

class ManufacturerAddForm(FlaskForm):
    manufacturer_name = StringField(validators=[DataRequired()])
    collaborator_name = StringField(default=None)
    submit = SubmitField('Add Brand')

class SneakerRemoveForm(FlaskForm):
    removal_type = SelectField('Removal Type', validators=[DataRequired()], choices=[('sell', 'Sell'), ('trash', 'Trash'), ('give', 'Give')])
    sneaker_to_remove = SelectField('Sneaker Name', coerce=int, validators=[DataRequired()]) 
    submit = SubmitField('Remove Sneakers')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sneaker_to_remove.choices = data_hooks.list_available_sneakers(data_hooks.db_connect())

