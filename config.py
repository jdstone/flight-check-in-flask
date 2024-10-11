from datetime import timedelta
from dotenv import load_dotenv
import os


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    SCHEDULER_API_ENABLED = True


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'   # use an in-memory database for test


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SW_REVIEW_API_URL = os.environ.get('SW_RV_API_URL')
    SW_CONFIRM_API_URL = os.environ.get('SW_CM_API_URL')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SECRET_KEY = os.environ.get('SECRET_KEY')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig,
}

