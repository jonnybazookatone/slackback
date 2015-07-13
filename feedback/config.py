"""
Configuration file. Please prefix application specific config values with
the application name.
"""

SAMPLE_APPLICATION_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/tmp/app.log',
        },
        'console': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'syslog': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console', 'syslog'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# These values are necessary only if the app needs to be a client of the API
SAMPLE_APPLICATION_ADSWS_API_TOKEN = 'this is a secret api token!'
SAMPLE_APPLICATION_ADSWS_API_URL = 'https://api.adsabs.harvard.edu'
FEEDBACK_SLACK_END_POINT = ''
GOOGLE_RECAPTCHA_ENDPOINT = ''
GOOGLE_RECAPTCHA_PRIVATE_KEY = ''
