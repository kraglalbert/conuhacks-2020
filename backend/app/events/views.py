from flask import Flask, jsonify, request, abort, make_response
from flask_login import login_required
from datetime import datetime
from . import events
from .. import db
from app.models import Event, Company, User, EventCategory


@events.route("", methods=["GET"])
def get_all_events():
    events = Event.query.all()
    return jsonify(Event.serialize_list(events))


# filter events by various criteria
@events.route("/filter", methods=["GET"])
def get_events_by_filter():
    category = request.args.get("category")

    if category is not None:
        events = Event.query.filter_by(category=EventCategory(category)).all()
        return jsonify(Event.serialize_list(events))


# create a new event
@events.route("", methods=["POST"])
def create_event():
    data = request.get_json(force=True)
    event_name = data.get("name")
    description = data.get("description")
    location = data.get("location")
    category = data.get("category")
    tags = data.get("tags")
    datetime_str = data.get("date_time")
    host_email = data.get("host_email")

    if (
        event_name == ""
        or description == ""
        or location == ""
        or host_email == ""
        or category == ""
        or tags is None
    ):
        abort(400, "Cannot have empty fields for new event")

    host = User.query.filter_by(email=host_email).first()
    if host is None:
        abort(400, "Event host does not exist")

    datetime_obj = datetime.strptime(datetime_str, "%D-%M-%Y %I:%M%p")
    new_event = Event(
        name=event_name,
        date_time=datetime_obj,
        category=category,
        tags=tags,
        host=host.id,
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.serialize)
