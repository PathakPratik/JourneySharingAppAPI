from constants import FLASK_HOSTNAME, FLASK_PORT, REDIS_HOST, REDIS_PORT
from setup import db, migrate_db, mail, session_
from flask import Flask
from flask_migrate import init, migrate, upgrade
import redis

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')


db.init_app(app)
migrate_db.init_app(app, db)
session_.init_app(app)
mail.init_app(app)

redisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Add MatchUsers Controller
from controllers.MatchUsers import app_match_users
app.register_blueprint(app_match_users)

# Add Register Controller
from controllers.Register import app_register
app.register_blueprint(app_register)

# Add Login Controller
from controllers.Login import app_login
app.register_blueprint(app_login)

# Add Logout Controller
from controllers.Logout import app_logout
app.register_blueprint(app_logout)

# Add Email Confirmation Controller
from controllers.EmailConformation import app_confirm_email
app.register_blueprint(app_confirm_email)

# Add Rating Controller
from controllers.Rating import app_ratings
app.register_blueprint(app_ratings)

# Add UserInfo Controller
from controllers.userInfo import user_info
app.register_blueprint(user_info)

if __name__ == "__main__":
    with app.app_context():
        #init_db = init() #Initialize the DB migriation path
        db.create_all()
        #migrate() #DB migration
        #upgrade() #DB Upgrade
    app.run(debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)