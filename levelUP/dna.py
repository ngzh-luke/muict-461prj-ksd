""" Send DNA data to TypingDNA """

import base64
import json
import requests
from flask import session
from levelUP.config import DNA_BASE_URL, DNA_API_KEY, DNA_API_SECRET
from levelUP.models import User


def _getUserID():

    try:
        username = session['username']
        user = User.query.filter_by(uname=username).first()
        if user:
            session['userID'] = user.userID
            return session['userID']
    except:
        return None


def _sendDNA(user_id, pattern, delete=None):
    """ Send DNA pattern to TypingDNA server """
    if user_id == None:
        if _getUserID() == None:
            return
        else:
            user_id = _getUserID()
    authstring = f"{DNA_API_KEY}:{DNA_API_SECRET}"
    base64string = base64.b64encode(authstring.encode()).decode()

    headers = {
        "Authorization": f"Basic {base64string}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    if delete != None:
        url = f"{DNA_BASE_URL}/user/{user_id}"
        res = requests.delete(url, headers=headers)
        return
    else:
        url = f"{DNA_BASE_URL}/auto/{user_id}"
        data = {"tp": pattern}

        res = requests.post(url, headers=headers, data=data)
        res_body = res.content

    # return json.loads(res_body.decode("utf-8"))
    session.clear()
    return json.loads(res_body)
