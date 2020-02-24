from os import environ, path


class Config(object):

    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') or 'sqlite:///' \
        + path.join(path.abspath(path.dirname(__file__)), 'court_cases.db')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
