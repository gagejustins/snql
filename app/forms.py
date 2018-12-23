from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired

class SneakerEventForm(FlaskForm):
    event_type = SelectField('Event Name', validators=[DataRequired()], choices=[('Add', 'add'), ('Remove', 'remove'), ('Clean', 'clean'), ('Wear', 'wear')])
    owner_id = SelectField('OwnerId', validators=[DataRequired()], choices= [('0',0)])
    sneaker_id = SelectField('SneakerId', validators=[DataRequired()], choices = [('1',1)])
    submit = SubmitField('Log Event')    

class SneakerCatalogForm(FlaskForm):
    sneaker_name = StringField(validators=[DataRequired()]) 
    color = StringField(validators=[DataRequired()])
    purchase_price = FloatField(validators=[DataRequired()]) 
    manufacturer_id = IntegerField(validators=[DataRequired()]) 
    submit = SubmitField('Add Sneaker') 
