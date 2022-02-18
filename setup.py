from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from flask_login import LoginManager

db = SQLAlchemy()
migrate_db = Migrate()
session_ = Session()
login_manager = LoginManager()