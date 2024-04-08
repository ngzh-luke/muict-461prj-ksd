from levelUP.helpers.automated import deleteAfterCreatedOneDay
from apscheduler.schedulers.background import BackgroundScheduler
from levelUP.helpers.logger import log


def ok():
    log(title='function', msg='executed')


# Configure the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(ok, 'interval', minutes=1)  # runs every 1 minute

# Start the scheduler
scheduler.start()

try:
    # Keep the main thread alive
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    # Handle the scheduler shutdown
    scheduler.shutdown()
