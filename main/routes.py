from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from webapp.models import User, Group, Deadline_status, Level, Deadline
from webapp import db
from main.forms import create_deadline

main = Blueprint('main', __name__, url_prefix='/main', template_folder='templates')


@main.route('/index', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def main_route():
    form = create_deadline()
    values = {'первый', 'второй', 'третий'}
    groups = {'1', '2', '3'}
    if form.validate_on_submit():
        group_name = form.group_name.data
        value = form.value.data
        value = Level.query.filter_by(value=value)
    return render_template('kalendar.html', form=form, value=values, groups=groups)
