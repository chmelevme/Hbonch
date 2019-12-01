from flask import Blueprint, redirect, url_for, flash, render_template, jsonify
from flask_login import current_user, login_required
from webapp.models import User, Group, Deadline_status, Level, Deadline, members
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
        value = Level.query.filter_by(value=value).first()
        deadline = Deadline(title=form.title.data, group=group, expiration_date=form.expiration_date.data)
        value.deadlines.append(deadline)
        users = group.members.all()
        db.session.add(deadline)
        db.session.commit()
        for user in users:
            d_s = Deadline_status(user_id=user.id, deadline_id=deadline.id)
            db.session.add(d_s)
            db.session.commit()
    Monday = Deadline_status.query.filter_by(user_id=current_user.id).join(Deadline).add_column(Deadline.id).add_column(
        Deadline.title) \
        .join(Level).add_column(Level.value).filter(Deadline.expiration_date == 1).all()
    Tuesday = Deadline_status.query.filter_by(user_id=current_user.id).join(Deadline).add_column(
        Deadline.id).add_column(
        Deadline.title) \
        .join(Level).add_column(Level.value).filter(Deadline.expiration_date == 2).all()
    Wednesday = Deadline_status.query.filter_by(user_id=current_user.id).join(Deadline).add_column(
        Deadline.id).add_column(
        Deadline.title) \
        .join(Level).add_column(Level.value).filter(Deadline.expiration_date == 3).all()
    Thursday = Deadline_status.query.filter_by(user_id=current_user.id).join(Deadline).add_column(
        Deadline.id).add_column(
        Deadline.title) \
        .join(Level).add_column(Level.value).filter(Deadline.expiration_date == 4).all()
    Friday = Deadline_status.query.filter_by(user_id=current_user.id).join(Deadline).add_column(Deadline.id).add_column(
        Deadline.title) \
        .join(Level).add_column(Level.value).filter(Deadline.expiration_date == 5).all()
    Saturday = Deadline_status.query.filter_by(user_id=current_user.id).join(Deadline).add_column(
        Deadline.id).add_column(
        Deadline.title) \
        .join(Level).add_column(Level.value).filter(Deadline.expiration_date == 6).all()
    Sunday = Deadline_status.query.filter_by(user_id=current_user.id).join(Deadline).add_column(Deadline.id).add_column(
        Deadline.title) \
        .join(Level).add_column(Level.value).filter(Deadline.expiration_date == 7).all()
    print(Monday)

    return render_template('main/kalendar.html', form=form, value=values, groups=groups, monday=Monday,
                           Thursday=Thursday, Wednesday=Wednesday, Friday=Friday, Saturday=Saturday, Sunday=Sunday,
                           Tuesday=Tuesday)


@login_required
@main.route('/done/<int:id>')
def done(id):
    #TODO Доделть
    deadline = Deadline.query.filter_by(id=id).first()
    status = Deadline_status.query.filter_by(deadline_id=deadline.id, user_id=current_user.id).first()
    status.status = 1
    group = deadline.group_id
    member = db.session.query(members).filter(members.c.group_id == group, members.c.user_id == current_user.id).first()
    s = int(member.points) + int(deadline.level.value)
    user_group_id = current_user.self_group.id
    member = db.session.query(members).filter(members.c.group_id == user_group_id, members.c.user_id == current_user.id)
    member.points += deadline.level.value
    db.session.commit()
    return redirect(url_for('main.main_route'))
