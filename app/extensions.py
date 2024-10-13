# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask import current_app
from flask_apscheduler import APScheduler
from flask_apscheduler.scheduler import BackgroundScheduler # WORKS-kinda


# jobstores = {
#     'default': SQLAlchemyJobStore(url='sqlite:///job_scheduler.db')
# }

###################################################
#### Initialize APScheduler
###################################################
scheduler = APScheduler(BackgroundScheduler()) # WORKS-kinda

# scheduler = APScheduler(scheduler=BackgroundScheduler(daemon=False)) # another example of passing parameters
# scheduler = APScheduler(BackgroundScheduler(jobstores=current_app.config['JOBSTORES']))

