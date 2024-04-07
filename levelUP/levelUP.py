""" app """
from flask import render_template, Blueprint, request, redirect, url_for, session, abort, flash
from flask_login import login_required, current_user

application = Blueprint('app', __name__)


@application.route('/')
@login_required
def home():
    return render_template('home.html', current_user=current_user)
