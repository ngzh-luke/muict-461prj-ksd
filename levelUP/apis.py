""" apis """
from flask import Blueprint, request, make_response, jsonify, session

api = Blueprint('api', __name__)


@api.post('/get/dna')
def getDNA():
    """ get DNA pattern from frontend to our server """
    data = request.get_json()
    pattern = data.get('pattern')
    session['dna'] = pattern
    username = data.get('username')
    session['username'] = username
    tobeReturned = jsonify(msg='DNA pattern has been submitted to our server.')
    return make_response(tobeReturned, 200)
