""" apis """
from flask import Blueprint, request, make_response, jsonify, session
from levelUP import redis_client
from levelUP.helpers.logger import log

api = Blueprint('api', __name__)


@api.post('/get/dna')
def getDNA():
    """ get DNA pattern from frontend to our server """
    data = request.get_json()
    pattern = data.get('pattern')
    session['dna'] = pattern
    username = data.get('username')
    session['username'] = username
    # Save the pattern and username in Redis with an expiration time of 3 minutes
    red = redis_client.set(name=username, ex=180,
                           value=pattern.encode('utf-8'))
    log(title='redis.set', msg=red)
    tobeReturned = jsonify(msg='DNA pattern has been submitted to our server.')
    return make_response(tobeReturned, 200)
