""" apis """
from flask import Blueprint, request, make_response, jsonify, redirect, url_for, session
from flask_login import current_user

api = Blueprint('api', __name__)


@api.post('/get/dna')
def getDNA():
    data = request.get_json()
    pattern = data.get('pattern')
    session['dna'] = pattern
    # if current_user.is_authenticated:
    #     user_id = current_user.userID
    # else:
    #     print('redirect')
    #     return redirect(url_for('auth.getLogin'))
    # typingdna_response = _sendDNA(user_id, pattern)
    # tobeReturned = jsonify(typingdna_response)
    tobeReturned = jsonify(msg='dna has been submitted to our server')
    # print('json')
    return make_response(tobeReturned, 200)
