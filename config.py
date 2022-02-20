from os import environ
from datetime import timedelta
import redis


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = str(environ.get('SECRET_KEY'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = str(environ.get('SQLALCHEMY_DATABASE_URI'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Session
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.from_url('redis://redis:6379')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=30)

    #Flask-Mail
    MAIL_SERVER = str(environ.get('MAIL_SERVER'))
    MAIL_PORT = (environ.get('MAIL_PORT'))
    MAIL_USERNAME = str(environ.get('MAIL_USERNAME'))
    MAIL_PASSWORD = str(environ.get('MAIL_PASSWORD'))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
