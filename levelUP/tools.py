""" tools """
from flask import Blueprint, request, render_template, flash, session
from flask_login import current_user
from levelUP.dna import _sendDNA
from levelUP.helpers.logger import log

tools = Blueprint('tools', __name__)


@tools.route('/typing-patterns', methods=['GET', 'POST'])
def typing_patterns():
    if request.method == 'POST':
        dna = _sendDNA(user_id=None, pattern=session['dna'])
        log(msg=dna, title='DNA')
        if dna['message_code'] == 10:
            flash(message='Another DNA pattern has been submitted but probably not enough, you may need to submit again.', category='info')
        elif dna['message_code'] == 1:
            flash(category='info',
                  message='Thank you! You may try to login again now.')
    return render_template("typing_patterns.html", user=current_user)
