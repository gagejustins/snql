from flask import render_template, flash, redirect
from app import app
from app.forms import SneakerEventForm, LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Justin'}
    return render_template('index.html', title='Home', user=user)

@app.route('/sneakers')
def log_event():
    form = SneakerEventForm()
    if form.validate_on_submit():
        flash('Sneaker event requested for user {}').format(form.username.data)
        return redirect(url_for('index'))
    return render_template('sneakers.html', title='Event logged', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
