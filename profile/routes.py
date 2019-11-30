from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from webapp.models import User, Group
from webapp import db
from profile.forms import change_mail, change_name, change_pass

profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='/templates')


@login_required
@profile.route('/', methods=['POST', 'GET'])
def profile():
    change_mail_form = change_mail()
    change_name_form = change_name()
    change_pass_form = change_pass()
    if change_mail_form.validate_on_submit():
        return 'change_mail done'
    if change_pass_form.validate_on_submit():
        return 'change_pass done'
    if change_name_form.validate_on_submit():
        return 'change_name done'
    return render_template('account/profile', change_mail_form=change_mail_form, change_pass_form=change_pass_form,
                           change_name_form=change_name_form)
