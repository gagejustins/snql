from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import SneakerEventForm, SneakerCatalogForm
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

@app.route('/sneakers-catalog', methods=['GET', 'POST'])
def add_sneaker():
    form = SneakerCatalogForm()
    if form.validate_on_submit():
        conn = data_hooks.db_connect()
        results = data_hooks.sneaker_insert(conn, form.sneaker_name.data, form.color.data, form.purchase_price.data, form.manufacturer_id.data)
        flash(results)
        return redirect(url_for('index'))
    return render_template('sneaker_catalog.html', title='Event logged', form=form)
