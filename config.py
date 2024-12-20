from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from dotenv import load_dotenv
import os


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SCHEDULER_API_ENABLED = True
    SCHEDULER_JOBSTORES = {'default': SQLAlchemyJobStore(url=f"sqlite:///{os.getenv('SCHEDULER_JOBSTORE_FILE', 'job_scheduler.sqlite')}")}


class TestConfig(Config):
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    DEBUG = True
    SW_REVIEW_API_URL = os.getenv('SW_RV_API_URL')
    SW_CONFIRM_API_URL = os.getenv('SW_CM_API_URL')


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SW_REVIEW_API_URL = os.getenv('SW_RV_API_URL', 'https://www.southwest.com/api/air-checkin/v1/air-checkin/page/air/check-in/review')
    SW_CONFIRM_API_URL = os.getenv('SW_CM_API_URL', 'https://www.southwest.com/api/air-checkin/v1/air-checkin/page/air/check-in/confirmation')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': ProductionConfig,
}
