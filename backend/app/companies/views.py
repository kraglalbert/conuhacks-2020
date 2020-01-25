from flask import Flask, jsonify, request, abort, make_response
from flask_login import login_required
from . import companies
from .. import db
from app.models import Event, Company, User


@companies.route("/", methods=["GET"])
def get_all_companies():
    companies = Company.query.all()
    return jsonify(Company.serialize_list(companies))

