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