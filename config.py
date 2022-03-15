from os import environ, path
from distutils.util import strtobool

app_dir = path.abspath(path.dirname(__file__))

class Config:
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ##### Flask-Mail configurations #####
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USE_TLS = bool(strtobool(environ.get('MAIL_USE_TLS', 'False')))
    MAIL_USE_SSL = bool(strtobool(environ.get('MAIL_USE_SSL', 'False')))
    MAIL_USERNAME = environ.get('EMAIL_USER')
    MAIL_PASSWORD = environ.get('EMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    
    MAX_CONTENT_LENGTH = 20 * 1000 * 1000


class Development(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEVELOPMENT_DATABASE_URI') 

class Testing(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('TESTING_DATABASE_URI')

class Production(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('PRODUCTION_DATABASE_URI') 
