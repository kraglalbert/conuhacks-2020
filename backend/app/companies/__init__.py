from flask import Blueprint

companies = Blueprint("companies", __name__)

from . import views
