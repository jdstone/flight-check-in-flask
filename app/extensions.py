from flask_apscheduler import APScheduler
from flask_apscheduler.scheduler import BackgroundScheduler


###################################################
#### Initialize APScheduler
###################################################
scheduler = APScheduler(BackgroundScheduler())

