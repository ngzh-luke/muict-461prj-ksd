""" Send DNA data to TypingDNA """

import base64
import json
import requests
from levelUP.config import DNA_BASE_URL, DNA_API_KEY, DNA_API_SECRET


def _sendDNA(user_id, pattern, delete=None):
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
    return json.loads(res_body)
