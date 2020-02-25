from os import environ, path


# Base Config class
class Config(object):

    # SQLite database created in project root dir
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///' \
        + path.join(path.abspath(path.dirname(__file__)), 'court_cases.db')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'zebra-unicorn-elephant-some-long-string-of-animals'


class TestConfig(Config):

    TESTING = True
    DEBUG = True
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
