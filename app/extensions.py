from flask_apscheduler import APScheduler
from flask_apscheduler.scheduler import BackgroundScheduler


###################################################
#### Initialize APScheduler
###################################################
scheduler = APScheduler(BackgroundScheduler())

# scheduler = APScheduler(scheduler=BackgroundScheduler(daemon=False)) # another example of passing parameters
# scheduler = APScheduler(BackgroundScheduler(jobstores=current_app.config['JOBSTORES']))

