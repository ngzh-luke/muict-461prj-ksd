""" tools """
from flask import Blueprint, request, render_template, jsonify, session
from flask_login import current_user
from levelUP.dna import _sendDNA

tools = Blueprint('tools', __name__)


@tools.route('/typing-patterns', methods=['GET', 'POST'])
def typing_patterns():
    if request.method == 'POST':
        _sendDNA(user_id=current_user.userID, pattern=session['dna'])
    return render_template("typing_patterns.html", user=current_user)
