""" tools """
from flask import Blueprint, request, render_template, jsonify
from flask_login import current_user

tools = Blueprint('tools', __name__)


@tools.route('/typing-patterns')
def typing_patterns():
    return render_template("typing_patterns.html", user=current_user)
