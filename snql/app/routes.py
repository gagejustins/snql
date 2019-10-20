from flask import render_template, flash, redirect, url_for, request, Response 
from app import app
from app.forms import SneakerEventForm, SneakerAddForm, SneakerRemoveForm, ManufacturerAddForm
from app.data_scripts import data_hooks, data_api 
import pandas as pd
from twilio.twiml.messaging_response import MessagingResponse

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

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    user_term = request.values.get('Body', None)
    resp = MessagingResponse()
    conn = data_hooks.db_connect()

    if user_term.isnumeric() == False:
        #List sneakers if user sends a string
        sneakers_dict = dict(data_hooks.available_sneakers_search(conn, user_term.lower()))
        formatted_sneakers_list = '\n'.join(['%s - %s' % (key, value) for (key, value) in sorted(sneakers_dict.items())])

        if len(formatted_sneakers_list) > 0:
            resp.message("Which pair exactly?\n {}".format(formatted_sneakers_list))
        else:
            resp.message("That search didn't return any results. Try again. Or don't, life is meaningless.")

    else:
        #Update database if user sends a sneaker ID
        #validate given sneaker ID is in the database
        available_ids = data_hooks.list_available_sneaker_ids(conn)
        if int(user_term) in available_ids:
            data_hooks.sneaker_event_insert(conn=conn, 
                                            sneaker_id=user_term, 
                                            event_type='wear', 
                                            config=None)
            resp.message("Wear recorded for sneaker_id {}".format(user_term))
        else:
            resp.message("That sneaker_id doesn't exist in the SNQL database or isn't owned (yet). Try searching again or entering a sneaker_id directly. Or don't, life is meaningless.")

    return str(resp)
