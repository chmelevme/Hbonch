from flask import Blueprint, redirect, url_for, flash, render_template
from auth.forms import login_form, register_form
from flask_login import current_user, login_user
from webapp.models import User, Group
from webapp import db

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
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('auth.main_route'))
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.main_route'))
    form = register_form()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        self_group = Group(name='group {}'.format(form.name.data))
        user.self_group = self_group
        db.session.add_all([user, self_group])
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
