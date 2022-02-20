from operator import imod
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate_db = Migrate()
session_ = Session()
login_manager = LoginManager()
mail = Mail()
url_safe_timed_serializer = URLSafeTimedSerializer('Thisisasecret!')