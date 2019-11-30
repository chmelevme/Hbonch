import unittest
from webapp import create_app, db
from config import config
from webapp.models import User, Deadline, Level, Group, Deadline_status
from datetime import datetime, timedelta


class Testingconfig(config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class tests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app(Testingconfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_deadline_value(self):
        now = datetime.utcnow()
        now2 = now + timedelta(minutes=10)
        d = Deadline(expiration_date=now, title='first')
        d2 = Deadline(expiration_date=now2, title='second')
        level = Level(value=10)
        db.session.add_all([d, d2, level])
        db.session.commit()
        level.deadlines.append(d)
        level.deadlines.append(d2)
        db.session.commit()
        self.assertEqual('[<Deadline 1>, <Deadline 2>]', str(level.deadlines.all()))
        self.assertEqual(10, d.level.value)
        self.assertEqual(10, d2.level.value)
        self.assertNotEqual(1100, d2.level.value)

    def test_deadline_group(self):
        now = datetime.utcnow()
        now2 = now + timedelta(minutes=10)
        d = Deadline(expiration_date=now, title='first')
        d2 = Deadline(expiration_date=now2, title='second')
        group = Group(name='Test_group')
        group.deadlines.append(d)
        group.deadlines.append(d2)
        db.session.add_all([d, d2, group])
        db.session.commit()
        self.assertEqual(d.group.name, 'Test_group')
        self.assertNotEqual(d.group.name, 'Test_group2')
        self.assertEqual(d2.group.name, 'Test_group')

    def test_user_deadline_status(self):
        now = datetime.utcnow()
        now2 = now + timedelta(minutes=10)
        d = Deadline(expiration_date=now, title='first')
        d2 = Deadline(expiration_date=now2, title='second')
        level = Level(value=10)
        level.deadlines.append(d)
        level.deadlines.append(d2)
        u = User(name='Test_user', email='Test_user_email')
        u.set_password('123')
        db.session.add_all([d, level, u])
        db.session.commit()
        d_s = Deadline_status(user_id=u.id, deadline_id=d.id)
        d_s2 = Deadline_status(user_id=u.id, deadline_id=d2.id)
        db.session.add_all([d_s, d_s2])
        d_s2.status = 3
        db.session.commit()
        self.assertEqual(2, Deadline_status.query.filter_by(user_id=u.id, deadline_id=d.id).first().status)
        self.assertEqual(3, Deadline_status.query.filter_by(user_id=u.id, deadline_id=d2.id).first().status)
        self.assertNotEqual(2, Deadline_status.query.filter_by(user_id=u.id, deadline_id=d2.id).first().status)

    def test_self_group(self):
        u = User(name='Test_user', email='Test_user_email')
        group = Group(name='Test_group')
        now = datetime.utcnow()
        d = Deadline(expiration_date=now, title='first')
        group.deadlines.append(d)
        u.self_group = group
        level = Level(value=10)
        level.deadlines.append(d)
        self.assertEqual('Test_group', u.self_group.name)
        self.assertEqual(10, u.self_group.deadlines.first().level.value)
        self.assertNotEqual(120, u.self_group.deadlines.first().level.value)
        db.session.add_all([u, group, d])
        db.session.commit()
        user = User.query.filter_by(name='Test_user').first()


if __name__ == '__main__':
    unittest.main(verbosity=2)
