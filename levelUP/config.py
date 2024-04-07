""" global configurations """
from decouple import config as en_var  # import the environment var
from datetime import timedelta  # , datetime

VERSION = '0.2'
DEFAULTS = {'DEBUG': "False"}
DB_NAME = en_var(
    'DATABASE_URL', "sqlite:///levelUP_db.sqlite")
TIMEOUT = timedelta(hours=1)  # set session timeout here
