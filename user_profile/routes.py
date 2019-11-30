from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from webapp.models import User, Group, Deadline_status, Deadline, Level, members
from webapp import db
from user_profile.forms import change_pass, change_name, change_mail

user_profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='/templates')


@user_profile.route('/', methods=['POST', 'GET'])
def profile():
    change_mail_form = change_mail()
    change_name_form = change_name()
    change_pass_form = change_pass()
    if change_mail_form.validate_on_submit() and change_mail_form.mail.data:
        return 'change_mail done'
    if change_pass_form.validate_on_submit() and change_pass_form.pasword.data:
        return 'change_pass done'
    if change_name_form.validate_on_submit() and change_name_form.name.data:
        return 'change_name done'

    history = Deadline_status.query.filter_by(user_id=current_user.id) \
        .join(Deadline) \
        .add_columns(Deadline.title, Deadline_status.status) \
        .filter(Deadline_status.status < 2) \
        .join(Level).add_columns(Level.value).all()

    points = db.session.query(members).filter_by(user_id=current_user.id, group_id=current_user.self_group.id).first().points

    return render_template('account/profile.html', change_mail_form=change_mail_form, change_pass_form=change_pass_form,
                           change_name_form=change_name_form, history=history, points=points)
