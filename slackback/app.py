# encoding: utf-8
"""
Application factory
"""

import logging.config
from views import SlackFeedback
from flask import Flask
from flask.ext.restful import Api

def create_app():
    """
    Create the application and return it to the user

    :return: flask.Flask application
    """
    app = Flask(__name__, static_folder=None)
    app.url_map.strict_slashes = False

    # Load config and logging
    load_config(app)
    logging.config.dictConfig(
        app.config['SLACKBACK_LOGGING']
    )

    # Register extensions
    api = Api(app)

    # Add end points
    api.add_resource(SlackFeedback, '/feedback/slack')

    return app


def load_config(app):
    """
    Loads configuration in the following order:
        1. config.py
        2. local_config.py (ignore failures)
        3. consul (ignore failures)
    :param app: flask.Flask application instance
    :return: None
    """

    app.config.from_pyfile('config.py')

    try:
        app.config.from_pyfile('local_config.py')
    except IOError:
        app.logger.warning('Could not load local_config.py')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, use_reloader=False)
