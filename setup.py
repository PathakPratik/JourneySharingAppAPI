from operator import imod
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail
from flask_session import Session



db = SQLAlchemy()
migrate_db = Migrate()
mail = Mail()
session_ = Session()
url_safe_timed_serializer = URLSafeTimedSerializer('Thisisasecret!')