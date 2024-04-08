from flask import Blueprint, request, make_response, jsonify

api = Blueprint('api', __name__)


@api.get('')
def dnaLogin():
    pass
