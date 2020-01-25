import json
import base64
import enum
from . import db, login_manager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash


class EventCategory(enum.Enum):
    food_drink_alc = "Food/Drink"
    food_drink = "Food/Drink Non-Alcoholic"
    fitness = "Fitness"
    learn = "Learn"
    field_trip = "Field Trip"

association_table = db.Table('association', db.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
)


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.Enum(EventCategory), nullable=False)
    host = db.Column(db.Integer, db.ForeignKey("users.id"))
    attendees = db.relationship(
        "User",
        secondary=association_table)

    @staticmethod
    def generate_test_event():
        event = Event(
            name="Ultimate Frisbee 101", date_time="", category=EventCategory.fitness
        )
        db.session.add(event)
        db.session.commit()
        return event

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "date_time": self.date_time,
            "category": self.category,
        }

    @staticmethod
    def serialize_list(events):
        json_events = []
        for event in events:
            json_events.append(event.serialize)
        return json_events


class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64), nullable=False)
    employees = db.relationship("User", backref="companies", lazy="dynamic")

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {"id": self.id, "name": self.name, "location": self.location, "employees": self.employees}

    @staticmethod
    def serialize_list(companies):
        json_companies = []
        for company in companies:
            json_companies.append(company.serialize)
        return json_companies

    @staticmethod
    def generate_test_company():
        company = Company(name="Really Good Company", location="Montreal")
        db.session.add(company)
        db.session.commit()
        return company

    @staticmethod
    def validate_company(name, city):
        company = Company.query.filter_by(name=name).first()
        if company is None:
            company = Company(name=name, location=city)
            db.session.add(company)
            db.session.commit()
            return company
        else:
            return company



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    coffee_dates = db.Column(db.Boolean, nullable=False)
    hosted_events = db.relationship("Event", backref="users", lazy="dynamic")
    company = db.Column(db.Integer, db.ForeignKey("companies.id"))
    attended_events = db.relationship(
        "Event", secondary=association_table, back_populates="users"
    )

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=604800):
        s = Serializer(current_app.config["SECRET_KEY"], expiration)
        return s.dumps({"token": self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data["token"])
        return user

    @staticmethod
    def generate_test_user():
        user = User(name="Albert Kragl", email="akragl@gmail.com", password="password")
        db.session.add(user)
        db.session.commit()
        return user

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "coffee": self.coffee_dates,
            "password_hash": self.password_hash,
        }

    @staticmethod
    def serialize_list(users):
        json_users = []
        for user in users:
            json_users.append(user.serialize)
        return json_users

    def __repr__(self):
        return "<User %r>" % self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    # first, try to login using the token URL arg
    token = request.args.get("token")
    if token:
        user = User.verify_auth_token(token)
        if user:
            return user

    # next, try to login using Basic Auth
    token = request.headers.get("Authorization")
    if token:
        user = User.verify_auth_token(token)
        if user:
            return user

    # finally, return None if both methods did not login the user
    return None

