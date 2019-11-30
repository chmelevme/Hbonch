from webapp import db
from webapp import login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


members = db.table('members',
                   db.Column('user_id', db.Integer, db.ForeignKey('User.id'), primary_key=True),
                   db.Column('group_id', db.Integer, db.ForeignKey('Group.id'), primary_key=True),
                   db.Column('points', db.Integer))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)


class Deadline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expiration_date = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String, nullable=False)
    value_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
