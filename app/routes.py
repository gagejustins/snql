from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import SneakerEventForm 

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Justin'}
    return render_template('index.html', title='Home', user=user)

@app.route('/sneakers', methods=['GET', 'POST'])
def log_sneaker_event():
    form = SneakerEventForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('sneaker_event.html', title='Event logged', form=form)
