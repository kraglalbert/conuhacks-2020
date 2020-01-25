import time
import unittest

from app import create_app, db
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User.generate_test_user()
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User.generate_test_user()
        with self.assertRaises(AttributeError):
            u.password()

    def test_password_verification(self):
        u = User.generate_test_user()
        self.assertTrue(u.verify_password("password"))
        self.assertFalse(u.verify_password("notpassword"))

    def test_password_salts_are_random(self):
        u = User(name="Albert Kragl", email="akragl@gmail.com", password="password")
        u2 = User(name="Kragl Albert", email="kragla@gmail.com", password="password")
        self.assertTrue(u.password_hash != u2.password_hash)
