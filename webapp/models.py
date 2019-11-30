from webapp import db
from webapp import login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


members = db.Table('members',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                   db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True),
                   db.Column('points', db.Integer, default=0)
                   )


class Deadline_status(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    deadline_id = db.Column(db.Integer, db.ForeignKey('deadline.id'), primary_key=True)
    status = db.Column(db.Integer, nullable=False, default=2)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True)
    deadline_statuses = db.relationship('Deadline_status')
    groups = db.relationship('Group', secondary=members,
                             backref=db.backref('members'))
    self_group = db.relationship('Group', secondary=members, uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    deadlines = db.relationship('Deadline', backref=db.backref('group'), lazy='dynamic')


class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expiration_date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    users_statuses = db.relationship('Deadline_status')


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    deadlines = db.relationship('Deadline', backref='level', lazy='dynamic')
