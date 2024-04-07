""" Root file of the system """
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask, flash, session
from flask_migrate import Migrate
from werkzeug import exceptions
from decouple import config as en_var  # import the environment var
from levelUP.config import DB_NAME, TIMEOUT
from levelUP.helpers.errors import errHandl

db = SQLAlchemy()
migrate = Migrate()


def createApp():
    levelUP = Flask(__name__)
    f_bcrypt = Bcrypt()
    levelUP.config['SECRET_KEY'] = en_var('levelUP', 'levelUP_secret')
    levelUP.config['DATABASE_NAME'] = DB_NAME
    levelUP.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_NAME}'
    levelUP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    levelUP.config['REMEMBER_COOKIE_SECURE'] = True
    levelUP.config['TIMEZONE'] = 'Asia/Bangkok'
    levelUP.config['SESSION_COOKIE_SECURE'] = True
    levelUP.config['SESSION_COOKIE_HTTPONLY'] = True
    levelUP.config['SESSION_COOKIE_NAME'] = 'levelUP'
    levelUP.config['PERMANENT_SESSION_LIFETIME'] = TIMEOUT

    f_bcrypt.init_app(levelUP)
    db.init_app(levelUP)
    migrate.init_app(levelUP, db)

    for c in exceptions.default_exceptions.keys():
        """ errors handling """
        levelUP.register_error_handler(c, errHandl)

    from levelUP.levelUP import application as a
    from levelUP.authen import iden
    from levelUP.account import acc
    levelUP.register_blueprint(acc, url_prefix='/account')
    levelUP.register_blueprint(a, url_prefix='/')
    levelUP.register_blueprint(iden, url_prefix='/')

    # with app.app_context(): # Drop all of the tables
    #     db.drop_all()

    try:
        with levelUP.app_context():
            db.create_all()
    except Exception as e:
        db.session.rollback()
        flash(f'{e}', category='error')
        print(f"Error: {e}")

    from .models import User

    # config the user session
    @levelUP.before_request
    def before_request():
        session.permanent = True
        # session.modified = True # default set to true. Consult the lib to confirm

    login_manager = LoginManager()
    login_manager.login_view = 'auth.getLogin'
    login_manager.refresh_view = 'auth.getLogin'
    login_manager.login_message_category = 'info'
    login_manager.needs_refresh_message_category = "info"
    login_manager.login_message = 'Please login before perform the operation!'
    login_manager.needs_refresh_message = "You have to login again to confirm your identity!"
    login_manager.init_app(levelUP)

    @login_manager.user_loader
    def load_user(userID):
        return User.query.get(str(userID))

    return levelUP
