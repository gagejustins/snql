from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import SneakerEventForm, SneakerAddForm, SneakerRemoveForm
from app.data_scripts import data_hooks 

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

@app.route('/add-sneakers', methods=['GET', 'POST'])
def add_sneakers():
    form = SneakerAddForm()
    if form.validate_on_submit():
        conn = data_hooks.db_connect()
        inserted_id = data_hooks.sneaker_insert(conn, form.sneaker_name.data, form.color.data, form.purchase_price.data, form.manufacturer_id.data)
        if inserted_id:
            event = data_hooks.sneaker_event_insert(conn, inserted_id, 'add', config=None) 
        flash('Inserted ID: ' + str(inserted_id))
        conn.close()
        return redirect(url_for('index'))
    return render_template('sneaker_catalog.html', title='Event logged', form=form)

@app.route('/remove-sneakers', methods=['GET', 'POST'])
def remove_sneakers():
    form = SneakerRemoveForm()
    if form.validate_on_submit():
        conn = data_hooks.db_connect()
        event = data_hooks.sneaker_event_insert(conn, form.sneaker_to_remove.data, form.removal_type.data, config=None)
        flash(event)
        conn.close()
        return redirect(url_for('index'))
    return render_template('sneaker_remove.html', title='Event logged', form=form)
