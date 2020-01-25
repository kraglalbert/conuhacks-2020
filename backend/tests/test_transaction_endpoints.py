import unittest
import datetime
from flask import current_app, request, jsonify
from app.models import User
from app import create_app, db

TITLE = "Groceries"
SOURCE = "Safeway"
AMOUNT = -10045
YEAR = 2019
MONTH = 11
DAY = 1


class TransactionsIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_and_get_transaction(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/account/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.post(
                "/transactions/create",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": AMOUNT,
                    "email": user.email,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            t_id = json_data["id"]

            # get all transactions
            resp = c.get("/transactions")
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transaction by ID
            resp = c.get("/transactions/{}".format(t_id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(json_data["amount"], AMOUNT)
            self.assertEqual(json_data["source"], SOURCE)

            # get all transactions for user ID
            resp = c.get("/transactions/user/{}".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, valid
            resp = c.get("/transactions/user/{}?year=2019&month=11".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, year only
            resp = c.get("/transactions/user/{}?year=2019".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(json_data), 1)
            self.assertEqual(json_data[0]["amount"], AMOUNT)
            self.assertEqual(json_data[0]["source"], SOURCE)

            # get transactions for user by date, wrong date
            resp = c.get("/transactions/user/{}?year=2019&month=10".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(json_data, [])

            # get transactions for user by date, bad format
            resp = c.get("/transactions/user/{}?month=10".format(user.id))
            json_data = resp.get_json()
            self.assertEqual(resp.status_code, 400)

    def test_create_transaction_invalid(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/account/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            # create with invalid date
            resp = c.post(
                "/transactions/create",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": 1000,
                    "email": user.email,
                    "year": 0,
                    "month": 0,
                    "day": 0,
                },
            )
            self.assertEqual(resp.status_code, 400)

            # create with empty fields
            resp = c.post(
                "/transactions/create",
                json={
                    "title": "",
                    "source": "",
                    "amount": 0,
                    "email": "",
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 400)

    def test_update_transaction(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/account/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.post(
                "/transactions/create",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": AMOUNT,
                    "email": user.email,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            t_id = json_data["id"]
            json_data["title"] = "New Car"
            json_data["source"] = "Tesla"
            json_data["amount"] = -5000000
            json_data["year"] = 2020
            json_data["month"] = 1
            json_data["day"] = 31

            resp = c.put("/transactions/update/{}".format(t_id), json=json_data)
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            self.assertEqual(json_data["title"], "New Car")
            self.assertEqual(json_data["source"], "Tesla")
            self.assertEqual(json_data["amount"], -5000000)
            self.assertEqual(json_data["year"], 2020)
            self.assertEqual(json_data["month"], 1)
            self.assertEqual(json_data["day"], 31)

    def test_delete_transaction(self):
        user = User.generate_test_user()

        with self.app.test_client() as c:
            resp = c.post(
                "/account/login", json={"email": user.email, "password": "password"},
            )
            self.assertEqual(resp.status_code, 200)

            resp = c.post(
                "/transactions/create",
                json={
                    "title": TITLE,
                    "source": SOURCE,
                    "amount": AMOUNT,
                    "email": user.email,
                    "year": YEAR,
                    "month": MONTH,
                    "day": DAY,
                },
            )
            self.assertEqual(resp.status_code, 200)
            json_data = resp.get_json()
            t_id = json_data["id"]

            # delete existing transaction
            resp = c.delete("/transactions/delete/{}".format(t_id))
            self.assertEqual(resp.status_code, 200)

            # try deleting non-existent transaction
            resp = c.delete("/transactions/delete/{}".format(t_id))
            self.assertEqual(resp.status_code, 404)
