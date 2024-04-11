""" apis """
from flask import Blueprint, request, make_response, jsonify
from levelUP.config import DNA_BASE_URL, DNA_API_KEY, DNA_API_SECRET
import urllib.request
import base64
import json

api = Blueprint('api', __name__)


def _sendDNA(user_id, pattern):
    authstring = f"{DNA_API_KEY}:{DNA_API_SECRET}"
    base64string = base64.encodestring(
        authstring.encode()).decode().replace('\n', '')
    data = urllib.parse.urlencode({'tp': pattern})
    url = f'{DNA_BASE_URL}/auto/{user_id}'

    req = urllib.request.Request(url, data.encode('utf-8'), method='POST')
    req.add_header("Authorization", f"Basic {base64string}")
    req.add_header("Content-type", "application/x-www-form-urlencoded")

    res = urllib.request.urlopen(request)
    res_body = res.read()
    return json.loads(res_body.decode('utf-8'))


@api.post('/send/dna')
def sendDNA():
    data = request.get_json()
    pattern = data.get('pattern')
    user_id = data.get('userID')
    typingdna_response = _sendDNA(user_id, pattern)
    return make_response(jsonify(typingdna_response), 200)
