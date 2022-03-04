import os
from os import environ
from datetime import timedelta
import redis


class Config:
    """Set Flask configuration vars from .env file."""

    # General Config
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
