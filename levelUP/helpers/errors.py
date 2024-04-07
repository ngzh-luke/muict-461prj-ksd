""" HTTP errors handling """
from flask import jsonify


def errHandl(ex):
    """Handle errors as appropriate depending on path."""
    # adapted from Google cftscore: https://github.dev/google/ctfscoreboard/blob/28a8f6c30e401e07031741d5bafea3003e2d100e/scoreboard/main.py#L55%23L55
    try:
        status_code = ex.code
    except AttributeError:
        status_code = 500

    resp = jsonify(error=str(ex))
    resp.status_code = status_code

    return resp
