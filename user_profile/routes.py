from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user, login_required
from webapp.models import User, Group, Deadline_status, Deadline, Level, members
from webapp import db
from user_profile.forms import change_pass, change_name, change_mail, create_group
from flask import jsonify

user_profile = Blueprint('profile', __name__, url_prefix='/profile', template_folder='/templates')


@login_required
@user_profile.route('/groups', methods=['POST', 'GET'])
def group():
    form = create_group()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print('here')
        group = Group(name=form.name.data)
        group.members.append(current_user)
        db.session.add(group)
        db.session.commit()
        group.create_link()
        db.session.commit()
    groups_id = [item.id for item in current_user.groups.filter(Group.id != current_user.self_group.id).all()]
    response = []
    for item in groups_id:
        a = dict()
        a['name'] = Group.query.get(item).name
        a['url'] = Group.query.get(item).invite_link
        a['members'] = get_users_from_group(item)
        response.append(a)
    return render_template('groups/groups.html', groups=response, form=form)


def get_users_from_group(id):
    group_rating = Group.query.get(id).members.join(members, (members.c.user_id == User.id)).add_column(
        members.c.points).add_column(User.name).order_by(members.c.points).all()
    json_d = list()
    for item in group_rating:
        a, b = item[1:3]
        json_d.append({'user': b, 'points': a})
    return json_d


@login_required
@user_profile.route('/invite/<string:url>')
def invite(url):
    group = Group.verify_invite_link(url)

    if group is not None:
        group.members.append(current_user)
        db.session.commit()
        deadlines_ids = [item.id for item in group.deadlines.all()]
        for deadline_id in deadlines_ids:
            d_s = Deadline_status(user_id=current_user.id, deadline_id=deadline_id)
            db.session.add(d_s)
            db.session.commit()
    return redirect(url_for('main.main_route'))


@login_required
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
    points = db.session.query(members).filter_by(user_id=current_user.id,
                                                 group_id=current_user.self_group.id).first().points
    return render_template('account/profile.html', change_mail_form=change_mail_form, change_pass_form=change_pass_form,
                           change_name_form=change_name_form, history=history, points=points,
                           last_digit=str(current_user.id)[-1])
