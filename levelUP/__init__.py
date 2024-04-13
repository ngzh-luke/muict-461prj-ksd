""" Root file of the system """
import threading
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask, flash, session
from flask_migrate import Migrate
from werkzeug import exceptions
from decouple import config as en_var  # import the environment var
from levelUP.config import DB_NAME, TIMEOUT
from levelUP.helpers.errors import errHandl
from levelUP.helpers.logger import log
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers import SchedulerNotRunningError

db = SQLAlchemy()
migrate = Migrate()


scheduler = BackgroundScheduler()


def init_scheduler(app: Flask):
    from levelUP.helpers.automated import deleteAfterCreatedOneDay

    def run_scheduler():
        log(title="Automated job", msg='`deleteAfterCreatedOneDay` job is starting.')
        scheduler.start()
        log(title="Automated job", msg='`deleteAfterCreatedOneDay` job is started.')

        with app.app_context():
            try:
                scheduler.add_job(
                    id='deleteAfterCreatedOneDay',
                    func=deleteAfterCreatedOneDay,
                    args=(app,),
                    trigger='interval',
                    minutes=1,
                    replace_existing=True
                )
                log(title="Automated job",
                    msg='`deleteAfterCreatedOneDay` job is added.')
            except Exception as e:
                log(title="Automated job",
                    msg=f'`deleteAfterCreatedOneDay` job is unable to start. Details:{e}')

        @app.teardown_appcontext
        def shutdown_scheduler(exception=None):
            try:
                log(title="Automated job",
                    msg='`deleteAfterCreatedOneDay` job is shutting down.')
                scheduler.shutdown()
                log(title="Automated job",
                    msg='`deleteAfterCreatedOneDay` job is successfully shut down.')
            except SchedulerNotRunningError:
                log(title="Automated job",
                    msg=f'`deleteAfterCreatedOneDay` job is unable to shutdown. Details:{e}')

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()


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
    levelUP.config['PREFERRED_URL_SCHEME'] = 'https'  # force https

    f_bcrypt.init_app(levelUP)
    db.init_app(levelUP)
    migrate.init_app(levelUP, db)

    for c in exceptions.default_exceptions.keys():
        """ errors handling """
        levelUP.register_error_handler(c, errHandl)

    from levelUP.levelUP import application as a
    from levelUP.apis import api
    from levelUP.authen import iden
    from levelUP.account import acc
    from levelUP.tools import tools
    levelUP.register_blueprint(acc, url_prefix='/account')
    levelUP.register_blueprint(api, url_prefix='/api')
    levelUP.register_blueprint(a, url_prefix='/')
    levelUP.register_blueprint(iden, url_prefix='/')
    levelUP.register_blueprint(tools, url_prefix='/tools')

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

    # init_scheduler(levelUP) # now is not yet work, current error: raise RuntimeError('cannot schedule new futures after shutdown') RuntimeError: cannot schedule new futures after shutdown

    return levelUP
