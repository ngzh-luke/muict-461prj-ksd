""" The application is developed by the members of the group, 
please refer to readme file for more information
Created on April 14, 2024
Production Run file of the application """
from levelUP import createApp
from decouple import config as en_var  # import the environment var
from levelUP.config import VERSION, DEFAULTS
from levelUP.helpers.logger import log

log(title='levelUP APP', msg='started')
log(title='system version', msg=VERSION)
log(title='running mode',
    msg=f"production")
app = createApp()
