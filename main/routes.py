from flask import Blueprint, redirect, url_for, flash, render_template, jsonify
from flask_login import current_user, login_required
from webapp.models import User, Group, Deadline_status, Level, Deadline
from webapp import db
from main.forms import create_deadline
from datetime import datetime
main = Blueprint('main', __name__, url_prefix='/main', template_folder='templates')


@main.route('/index', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def main_route():
    form = create_deadline()
    groups = current_user.groups
    values = {item.value for item in Level.query.all()}
    if form.validate_on_submit():
        group_name = form.group_name.data
        group = Group.query.filter_by(name=group_name).first()
        value = form.value.data
        value = Level.query.filter_by(value=value)
        deadline = Deadline(title=form.title.data, group=group)
        value.deadlines.append(deadline)
        users = group.members.all()
        db.session.add(deadline)
        db.session.commit()
        for user in users:
            d_s = Deadline_status(user_id=user.id, deadline_id=deadline.id)
            db.session.add(d_s)
            db.session.commit()

    return render_template('main/kalendar.html', form=form, value=values, groups=groups)


@login_required
@main.route('/test/')
def test():
    return jsonify(data='123')


@login_required
@main.route('/data/<int:Data_start>/<int:Data_end>')
def get_deadlines(Data_start, Data_end):
    deadlines = Deadline_status.query.filter_by(user_id=current_user.id) \
        .join(Deadline, Deadline.id == Deadline_status.deadline_id) \
        .add_column(Deadline.title) \
        .add_column(Deadline.id) \
        .join(Level) \
        .add_column(Level.value) \
        .filter(Deadline.expiration_date > Data_start, Deadline.expiration_date < Data_end).all()
    print(deadlines)
    d2 = Deadline.query.filter_by(expiration_date=datetime.utcnow().day).first()
    for item in Deadline.query.all():
        print(item.expiration_date)

    return str(deadlines)
