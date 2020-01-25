import unittest
from flask import current_app, request, jsonify
from app.models import User
from app import create_app, db


class UsersIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_not_found(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/account/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.get("/users/jdoe")
            self.assertEqual(resp.status_code, 404)

    def test_unauthorized_user(self):
        with self.app.test_client() as c:
            resp = c.get("/users/jdoe")
            self.assertEqual(resp.status_code, 401)

    def test_update_user_settings(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/account/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.put(
                "/users/{}/settings".format(user.id),
                json={"monthly_budget": 10000, "default_currency": "CAD"},
            )
            self.assertEquals(resp.status_code, 200)

            resp = c.get("/users/{}".format(user.id))
            json_data = resp.get_json()
            self.assertEquals(json_data["monthly_budget"], 10000)
            self.assertEquals(json_data["default_currency"], "CAD")

    def test_update_user_settings_invalid(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/account/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            # negative monthly budget
            resp = c.put(
                "/users/{}/settings".format(user.id),
                json={"monthly_budget": -100, "default_currency": "CAD"},
            )
            self.assertEquals(resp.status_code, 400)

            # invalid currency code
            resp = c.put(
                "/users/{}/settings".format(user.id),
                json={"monthly_budget": 10000, "default_currency": "AAAAA"},
            )
            self.assertEquals(resp.status_code, 400)

            # invalid currency code 2
            resp = c.put(
                "/users/{}/settings".format(user.id),
                json={"monthly_budget": 10000, "default_currency": "123"},
            )
            self.assertEquals(resp.status_code, 400)

            # null values
            resp = c.put(
                "/users/{}/settings".format(user.id),
                json={"monthly_budget": None, "default_currency": ""},
            )
            self.assertEquals(resp.status_code, 400)

