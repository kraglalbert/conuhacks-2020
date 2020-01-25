from flask import Flask, jsonify, request, abort, make_response
from flask_login import login_required
from . import main
from .. import db
from app.models import Event, Company, User


@main.route("/", methods=["GET"])
def index():
    return "Welcome to ConUHacks 2020!"

