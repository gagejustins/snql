from flask import render_template, flash, redirect, url_for, request, Response 
from app import app
from app.forms import SneakerEventForm, SneakerAddForm, SneakerRemoveForm, ManufacturerAddForm
from app.data_scripts import data_hooks, data_api 
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Justin'}
    return render_template('index.html', title='Home', user=user)

@app.route('/sneakers', methods=['GET', 'POST'])
def log_sneaker_event():
    form = SneakerEventForm()
    if form.validate_on_submit():
        conn = data_hooks.db_connect()
        event = data_hooks.sneaker_event_insert(conn, form.sneaker_id.data, form.event_type.data, config=data_hooks.readConfigs())
        flash(event)
        conn.close()
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
    return render_template('sneaker_add.html', title='Event logged', form=form)

@app.route('/add-manufacturer', methods=['GET', 'POST'])
def add_manufacturer():
    form = ManufacturerAddForm()
    if form.validate_on_submit():
        conn = data_hooks.db_connect()
        inserted_id = data_hooks.manufacturer_insert(conn, form.manufacturer_name.data, form.collaborator_name.data)
        flash(inserted_id)
        conn.close()
        return redirect(url_for('index'))
    return render_template('manufacturer_add.html', title='Event logged', form=form) 

@app.route('/remove-sneakers', methods=['GET', 'POST'])
def remove_sneakers():
    form = SneakerRemoveForm()
    if form.validate_on_submit():
        conn = data_hooks.db_connect()
        event = data_hooks.sneaker_event_insert(conn, form.sneaker_to_remove.data, form.removal_type.data, config=None)
        remove_update = data_hooks.sneaker_remove(conn, form.sneaker_to_remove.data, form.removal_type.data)
        flash(event, remove_update)
        conn.close()
        return redirect(url_for('index'))
    return render_template('sneaker_remove.html', title='Event logged', form=form)

@app.route('/pairs_owned_over_time', methods=['GET'])
def pairs_owned_over_time():
    conn = data_hooks.db_connect()
    pairs_owned_over_time = data_api.generate_pairs_owned_over_time_df(conn)
    response = Response(pairs_owned_over_time.to_csv(index=False))
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/pairs_per_brand', methods=['GET'])
def pairs_per_brand():
    conn = data_hooks.db_connect()
    pairs_per_brand = data_api.generate_pairs_per_brand_df(conn)
    response = Response(pairs_per_brand.to_csv(index=False))
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
