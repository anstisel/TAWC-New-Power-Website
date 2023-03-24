# Note: secret key should not be in this file for production config

import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Set up config options for the application


class Config(object):
    # SQL Alchemy config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pagination settings
    POST_PER_PAGE = 50

    # Secret key for API
    SECRET_KEY = "adsflajkldsfioewi12389908&*&*(_*(&*@"
