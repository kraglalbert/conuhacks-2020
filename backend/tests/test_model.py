import unittest
import datetime
from flask import current_app
from app import create_app, db
from app.models import User, Transaction, TransactionMonth


class ModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # def create_test_transactions(self):
    #     # create 10 sample transactions

    # prefix all test cases with "test_"
    def test_create_user(self):
        user = User(
            name="John Doe",
            email="jdoe@gmail.com",
            password="goodpass",
            monthly_budget=50000,
        )
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email="jdoe@gmail.com").first()
        self.assertTrue(user is not None)
        self.assertTrue(user.monthly_budget == 50000)

    def test_delete_user(self):
        user = User(
            name="John Doe",
            email="jdoe@gmail.com",
            password="goodpass",
            monthly_budget=50000,
        )
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email="jdoe@gmail.com").first()
        self.assertTrue(user is not None)

        db.session.delete(user)
        db.session.commit()

        user = User.query.filter_by(email="jdoe@gmail.com").first()
        self.assertTrue(user is None)

    def test_user_default_currency(self):
        user = User(
            name="John Doe",
            email="jdoe@gmail.com",
            password="goodpass",
            default_currency="CAD",
            monthly_budget=50000,
        )
        db.session.add(user)
        db.session.commit()

        user = User.query.filter_by(email="jdoe@gmail.com").first()
        self.assertTrue(user.default_currency == "CAD")

        # attempt to set invalid currency
        try:
            user.default_currency = "AAAAA"
            db.session.add(user)
            db.session.commit()
        except:
            return

        self.fail()

    def test_create_transaction_month(self):
        # create test user
        user = User(
            name="John Doe",
            email="jdoe@gmail.com",
            password="goodpass",
            monthly_budget=50000,
        )
        db.session.add(user)
        db.session.commit()

        t_month = TransactionMonth(date=datetime.date(2019, 11, 1), user_id=user.id)
        db.session.add(t_month)
        db.session.commit()

        t_months = TransactionMonth.query.all()
        self.assertTrue(t_months[0] is not None)
        self.assertEqual(t_months[0].date, datetime.date(2019, 11, 1))

    def test_create_transaction(self):
        # create test users
        user = User(
            name="John Doe",
            email="jdoe@gmail.com",
            password="goodpass",
            monthly_budget=50000,
        )
        db.session.add(user)
        db.session.commit()

        # create TransactionMonth
        t_month = TransactionMonth(date=datetime.date(2019, 11, 1), user_id=user.id)
        db.session.add(t_month)
        db.session.commit()

        date = datetime.datetime(2019, 11, 3)
        t = Transaction(
            title="Groceries",
            source="Safeway",
            amount=10145,
            date=date,
            user_id=user.id,
            transaction_month_id=t_month.id,
        )

        db.session.add(t)
        db.session.commit()

        user = User.query.filter_by(email="jdoe@gmail.com").first()
        t = user.transactions[0]
        self.assertTrue(t is not None)
        self.assertEqual(t.amount, 10145)
        self.assertEqual(t.source, "Safeway")
        self.assertEqual(t.title, "Groceries")
