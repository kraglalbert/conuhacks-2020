from flask import Flask, jsonify, request, abort, make_response
from flask_login import login_required
from . import users
from .. import db
from app.models import Event, Company, User


@users.route("", methods=["GET"])
def get_all_users():
    users = User.query.all()
    return jsonify(User.serialize_list(users))


@users.route("/<int:id>", methods=["GET"])
def get_user_by_id(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(400, "User does not exist")

    return jsonify(user.serialize)

