import unittest
from webapp import create_app,db
from config import config

class Testingconfig(config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'


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

