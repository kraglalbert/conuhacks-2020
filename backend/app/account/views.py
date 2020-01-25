import datetime
from flask import Flask, jsonify, request, abort, make_response
from flask_login import current_user, login_required, login_user, logout_user
from . import account
from .. import db
from app.models import User

# log in an existing user
@account.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if (
        user is not None
        and user.password_hash is not None
        and user.verify_password(password)
    ):
        login_user(user)
        token = user.generate_auth_token()
        return jsonify({"user": user.serialize, "token": token.decode("ascii")})
    return "Wrong email or password!", 400


# check if token is valid and return user
@account.route("/token", methods=["POST"])
def verify_token():
    data = request.get_json(force=True)
    token = data.get("token")

    user = User.verify_auth_token(token)
    if user is None:
        abort(404, "Token does not match any user")

    return jsonify(user.serialize)


# register a new user
@account.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    company = data.get("company")
    location = data.get("location")

    if name == "" or email == "" or password == "":
        abort(400, "Cannot have empty fields for user")

    user = User.query.filter_by(email=email).first()
    if user is not None:
        abort(400, "Account already exists with this email")

    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize)


# log out an existing user
@account.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out successfully!", 200
