# encoding: utf-8
"""
Views
"""

import json
import requests

from flask import current_app, request, abort
from flask.ext.restful import Resource
from flask.ext.discoverer import advertise
from client import client
from utils import get_post_data, err

from werkzeug.exceptions import BadRequestKeyError

CHECK_CAPTCHA = False
API_DOCS = 'https://github.com/adsabs/adsabs-dev-api'
ERROR_UNVERIFIED_CAPTCHA = dict(
    body='captcha was not verified',
    number=403
)
ERROR_MISSING_KEYWORDS = dict(
    body='Incorrect POST data, see the API docs {0}'
          .format(API_DOCS),
    number=404
)
def verify_recaptcha(request, ep=None):
    """
    Verify a google recaptcha based on the data contained in the request

    :param request: flask.request
    :param ep: google recaptcha endpoint
    :type ep: basestring|None
    :return:True|False
    """
    if ep is None:
        ep = current_app.config['GOOGLE_RECAPTCHA_ENDPOINT']
    data = get_post_data(request)
    payload = {
        'secret': current_app.config['GOOGLE_RECAPTCHA_PRIVATE_KEY'],
        'remoteip': request.remote_addr,
        'response': data['g-recaptcha-response']
    }
    r = requests.post(ep,data=payload)
    r.raise_for_status()
    return True if (r.json()['success'] == True) else False

class SlackFeedback(Resource):
    """
    Forwards a user's feedback to slack chat using a web end
    """
    decorators = [advertise('scopes', 'rate_limit')]
    scopes = []
    rate_limit = [1000, 60*60*24]

    @staticmethod
    def prettify_post(post_data):
        """
        Converts the given input into a prettified version
        :param post_data: the post data to prettify, dictionary expected
        :return: prettified_post data, dictionary
        """
        channel = post_data.get('channel', '#feedback')
        icon_emoji = post_data.get('icon_emoji', ':ghost:')
        username = post_data.get('username', 'TownCrier')

        try:
            name = post_data['name']
            reply_to = post_data['_replyto']
            comments = post_data['comments']
            subject = post_data['_subject']
            feedback_type = post_data['feedback-type']
        except BadRequestKeyError:
            raise

        if feedback_type == 'bug':
            icon_emoji = ':goberserk:'
        elif feedback_type == 'comment':
            icon_emoji = ':neckbeard:'
        else:
            icon_emoji = ':see_no_evil:'

        prettified_data = {
            'text': '```Incoming Feedback```\n'
                    '*Commenter*: {commenter}\n'
                    '*e-mail*: {email}\n'
                    '*Type*: {feedback_type}\n'
                    '*Subject*: {subject}\n'
                    '*Feedback*: {feedback}'.format(
                        commenter=name,
                        email=reply_to,
                        feedback_type=feedback_type,
                        feedback=comments,
                        subject=subject
                    ),
            'username': username,
            'channel': channel,
            'icon_emoji': icon_emoji
        }

        return prettified_data

    def post(self):
        """
        HTTP POST request
        :return: status code from the slack end point
        """

        post_data = get_post_data(request)
        current_app.logger.info('Received feedback: {0}'.format(post_data))

        if CHECK_CAPTCHA:
            if not post_data.get('g-recaptcha-response', False) or \
                    not verify_recaptcha(request):
                current_app.logger.info('The captcha was not verified!')
                return err(ERROR_UNVERIFIED_CAPTCHA)
            else:
                current_app.logger.info('Skipped captcha!')

        try:
            current_app.logger.info('Prettifiying post data: {0}'
                                    .format(post_data))
            formatted_post_data = json.dumps(self.prettify_post(post_data))
            current_app.logger.info('Data prettified: {0}'
                                    .format(formatted_post_data))
        except BadRequestKeyError as error:
            current_app.logger.error('Missing keywords: {0}, {1}'
                                     .format(error, post_data))
            return err(ERROR_MISSING_KEYWORDS)

        slack_response = client().post(
            url=current_app.config['FEEDBACK_SLACK_END_POINT'],
            data=formatted_post_data
        )

        return {}, 200
