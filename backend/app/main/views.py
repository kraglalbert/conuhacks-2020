from flask import Flask, jsonify, request, abort, make_response
from . import main


@main.route("/", methods=["GET"])
def index():
    return "Welcome to ConUHacks 2020!"


