from flask import Flask, jsonify, request, abort, make_response
from flask_login import login_required
from . import events
from .. import db
from app.models import Event, Company, User


@events.route("/", methods=["GET"])
def get_all_events():
    events = Event.query.all()
    return jsonify(Event.serialize_list(events))
