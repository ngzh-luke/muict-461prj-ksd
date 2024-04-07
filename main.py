""" The application is developed by the members of the group, 
please refer to readme file for more information
Created on April 7, 2024
Run file of the application """
from levelUP import createApp
from decouple import config as en_var  # import the environment var
from levelUP.config import VERSION, DEFAULTS
from levelUP.helpers.logger import log

log(title='levelUP APP', msg='started')
log(title='system version', msg=VERSION)

runningDebugMode = en_var('DEBUG', DEFAULTS['DEBUG'])


def runDev():
    """ for running in dev """
    if __name__ == '__main__':
        app = createApp()
        app.run(port=int(en_var("PORT", 5500)),
                debug=en_var("DEBUG", True))


def runProd():
    """ for running gunicorn (in production) """
    app = createApp()


match runningDebugMode:
    case "True":
        log(title='running mode', msg='dev')
        runDev()

    case "False":
        log(title='running mode', msg='prod')
        runProd()
    case _:
        runningDebugMode = bool("False")
        log(title='running mode',
            msg=f"def (prod)")
        runProd()
