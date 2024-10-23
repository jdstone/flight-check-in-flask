from app.extensions import scheduler
from config import config
from flask import Flask
import logging
import os


def create_app(config_class=os.getenv('FLASK_ENV') or 'default'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config[config_class])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ###################################################
    #### Initialize Extensions
    ###################################################
    scheduler.init_app(app)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

    ###################################################
    #### Register Blueprints
    ###################################################
    from . import southwest
    app.register_blueprint(southwest.bp)
    
    from . import checkin
    app.register_blueprint(checkin.bp)

    ###################################################
    #### Error Logging to File - For Production
    ###################################################
    logger = logging.getLogger(__name__)
    if not app.debug and not app.testing:
        logger.setLevel(logging.INFO)
    elif app.debug or app.testing:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.DEBUG)

    return app

