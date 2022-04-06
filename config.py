from os import environ
from dotenv import dotenv_values

ENV = dotenv_values(".env")

class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = str(environ.get('SECRET_KEY'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = str(environ.get('SQLALCHEMY_DATABASE_URI'))
    #SQLALCHEMY_DATABASE_URI = str(ENV['SQLALCHEMY_DATABASE_URI'])
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #Flask-Mail
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=465
    #To use pytest, uncomment line 21 and comment out line 20
    # MAIL_USERNAME = str(ENV['MAIL_USERNAME'])
    MAIL_USERNAME = str(environ.get('MAIL_USERNAME'))

    #To use pytest, uncomment line 25 and comment out line 24
    # MAIL_PASSWORD = str(ENV['MAIL_PASSWORD'])
    MAIL_PASSWORD = str(environ.get('MAIL_PASSWORD'))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True