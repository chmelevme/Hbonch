from flask import Blueprint, redirect, url_for, flash, render_template
from auth.forms import login_form
from flask_login import current_user, login_user
from webapp.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='/templates')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = login_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)
