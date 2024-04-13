""" global configurations """
from decouple import config as en_var  # import the environment var
from datetime import timedelta  # , datetime

VERSION = '0.6'
DEFAULTS = {'DEBUG': "False"}
DB_NAME = en_var(
    'DATABASE_URL', "sqlite:///levelUP_db.sqlite")
TIMEOUT = timedelta(hours=1)  # set session timeout here
DNA_API_KEY = en_var('DNA_API_KEY', '0fe67243b0f70a83a1c3fa7fb76ddd3e')
DNA_API_SECRET = en_var('DNA_API_SECRET', '012526c122551650ae0aae249a5bf331')
DNA_BASE_URL = 'https://api.typingdna.com'
