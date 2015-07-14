# Slackback
A small web service that allows you to embed a web form within your web application, which forwards the content of the web form to a slack chat room of your dev team.

# Prerequesites
### Slack chat room
First go over to [slack](www.slack.com) and set up a chat room for your team if you already do not have one. Then setup a room called, e.g. '#feedback'. Then, you will want to set up 'Incoming WebHooks', such that you get a URL end point for the room '#feedback'.

### Google recaptcha
Second, you will need to get a secret key for the Google recaptcha to work. Go over to [Google](https://www.google.com/recaptcha/intro/index.html) and get one.

### Config file
Create a `local_config.py` file for which you should add the following configuration values:
  * FEEDBACK_SLACK_END_POINT = 'Enter your slack WebHook Integration end point'
  * GOOGLE_RECAPTCHA_PRIVATE_KEY = 'Enter your recaptcha key'

**Note** you should not add this to your git repo, and only if you ignore the git-ignore, will you do so.

# Usage

You can start the application in the following way:
```
python wsgi.py
```
Visit the web page `index.html` and fill out the feedback form:

Press submit, and you will see the following message arrive within your slack chat room:

# Customisation










