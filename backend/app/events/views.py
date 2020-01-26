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


# get hosted events
@events.route("/event-by-host/<int:id>", methods=["GET"])
def get_events_by_host(id):
    events = []

    if id is None:
        abort(400, "Must specify host ID")

    user = User.query.filter_by(id=id).first()

    # get all events hosted by this user
    if user is not None:
        events.extend(user.hosted_events)

    return jsonify(Event.serialize_list(events))

# find a coffee date
@events.route("/find-coffee-date/<int:id>", methods=["GET"])
def find_coffee_date(id):
    if id is None: 
        abort(400, "Must specify host ID")
    
    user = User.query.filter_by(id=id).first()
    date = user.find_coffee_date()

    if date is None:
        return jsonify({'result':False})
    else:
        user.coffee = False
        db.session.add(user)
        db.session.commit()
        date.coffee = False
        db.session.add(date)
        db.session.commit()
        return jsonify(date.serialize)


# update an event
@events.route("/update", methods=["POST"])
def update_event():
    data = request.get_json(force=True)
    event_name = data.get("name")
    description = data.get("description")
    location = data.get("location")
    datetime_str = data.get("date_time")
    host_id = int(data.get("host_id"))
    event_id = int(data.get("event_id"))

    if (
        event_name == ""
        or description == ""
        or location == ""
        or host_id == ""
        or event_id == ""
    ):
        abort(400, "Cannot have empty fields for event")

    event = Event.query.filter_by(id=event_id).first()

    if event is None:
        abort(400, "Event does not exist")

    host = User.query.filter_by(id=host_id).first()
    if host is None:
        abort(400, "Event host does not exist")

    if host_id != event.host:
        abort(400, "Only the event host can edit the event")

    # format: 12-12-2019 1:30PM
    datetime_obj = datetime.strptime(datetime_str, "%d-%m-%Y %I:%M%p")

    event.name = event_name
    event.description = description
    event.location = location
    event.host = host_id
    event.date_time = datetime_obj

    db.session.add(event)
    db.session.commit()

    return jsonify(event.serialize)


# get all event categories
@events.route("/categories", methods=["GET"])
def get_categories():
    enum_list = [category.value for category in EventCategory]

    return jsonify(enum_list)


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


# delete event
@events.route("/delete", methods=["DELETE"])
def delete_event():
    data = request.get_json(force=True)
    event_id = int(data.get("event_id"))
    host_id = int(data.get("host_id"))
    print("hiiiiiiiii")

    event = Event.query.filter_by(id=event_id).first()

    if event.host != host_id:
        abort(400, "Event can only be deleted by the host of the event")

    if Event.query.filter_by(id=event_id).first is None:
        abort(400, "There are no events with this ID.")

    event = Event.query.filter_by(id=event_id)
    Event.query.filter_by(id=event_id).delete()

    return jsonify({"result": True})


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
        description=description,
        location=location,
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
