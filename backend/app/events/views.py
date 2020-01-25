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
    company_id = request.args.get("company_id")

    events = []

    if company_id is None:
        abort(400, "Must specify company ID")

    # get all events from specified company
    company = Company.query.filter_by(id=company_id).first()
    if company is None:
        abort(400, "Company does not exist")

    for employee in company.employees:
        events.extend(employee.hosted_events)

    if category is not None:
        events = Event.query.filter_by(category=EventCategory(category)).all()
        events = list(
            filter(
                lambda event: User.query.filter_by(id=event.host).first().company
                != company_id,
                events,
            )
        )

    return jsonify(Event.serialize_list(events))


# create a new event
@events.route("", methods=["POST"])
def create_event():
    data = request.get_json(force=True)
    event_name = data.get("event_name")
    description = data.get("description")
    location = data.get("location")
    category = data.get("category")
    datetime_str = data.get("date_time")
    host_email = data.get("host_email")

    if (
        event_name == ""
        or description == ""
        or location == ""
        or host_email == ""
        or category == ""
    ):
        abort(400, "Cannot have empty fields for new event")

    host = User.query.filter_by(email=host_email).first()
    if host is None:
        abort(400, "Event host does not exist")

    # format: 12-12-2019 1:30PM
    datetime_obj = datetime.strptime(datetime_str, "%d-%m-%Y %I:%M%p")
    new_event = Event(
        name=event_name,
        date_time=datetime_obj,
        category=EventCategory(category),
        host=host.id,
    )
    db.session.add(new_event)
    db.session.commit()

    return jsonify(new_event.serialize)


# add a new attendee to an event
@events.route("/<int:event_id>/add-attendee", methods=["PUT"])
def add_attendee_to_event(event_id):
    data = request.get_json(force=True)
    attendee_email = data.get("attendee_email")

    if attendee_email is None or attendee_email == "":
        abort(400, "Attendee email cannot be empty")

    attendee = User.query.filter_by(email=attendee_email).first()
    event = Event.query.filter_by(id=event_id).first()

    event.attendees.append(attendee)
    db.session.add(event)
    db.session.commit()

    return jsonify(event.serialize)


# remove an attendee from an event
@events.route("/<int:event_id>/remove-attendee", methods=["PUT"])
def remove_attendee_from_event(event_id):
    data = request.get_json(force=True)
    attendee_email = data.get("attendee_email")

    if attendee_email is None or attendee_email == "":
        abort(400, "Attendee email cannot be empty")

    attendee = User.query.filter_by(email=attendee_email).first()
    event = Event.query.filter_by(id=event_id).first()

    cur_attendees = event.attendees

    # filter out the attendee that should be removed
    filtered_attendees = list(filter(lambda a: a.id != attendee.id, cur_attendees))

    event.attendees = filtered_attendees
    db.session.add(event)
    db.session.commit()

    return jsonify(event.serialize)
