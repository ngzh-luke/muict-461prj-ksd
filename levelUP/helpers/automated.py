""" automated executable functions """
from datetime import datetime, timedelta, timezone
from levelUP.models import User
from levelUP import db
from levelUP.helpers.logger import log
from flask import Flask, current_app
import logging

logger = logging.getLogger(__name__)


def deleteAfterCreatedOneDay(app: Flask):
    """ user account deletion after creation for a day """
    # app = current_app
    with app.app_context():
        try:
            users_to_delete = User.query.filter(
                User.createdAt <= datetime.now(
                    timezone.utc) - timedelta(days=1)
            ).all()

            for user in users_to_delete:
                user.delete()
            db.session.commit()

            log(title="Automated job",
                msg='`deleteAfterCreatedOneDay` successfully executed.')
        except Exception as e:
            # db.session.rollback()
            log(title="Automated job",
                msg=f'`deleteAfterCreatedOneDay` encountered error: {e}')

    # try:
    #     # Your logic to delete records after one day
    #     logger.info("Executing deleteAfterCreatedOneDay job")
    #     # ... (your code here)
    # except Exception as e:
    #     logger.error(f"Error executing deleteAfterCreatedOneDay job: {e}")
