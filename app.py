from constants import FLASK_HOSTNAME, FLASK_PORT, REDIS_HOST, REDIS_PORT
from db import db
from flask import Flask
import json
from os import environ
import redis
from sqlalchemy.exc import IntegrityError
from time import sleep


app = Flask(__name__)
sleep(10)
app.config.from_file("config.json", load=json.load)

db.init_app(app)

redisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

            
# Add MatchUsers Controller
from controllers.MatchUsers import app_match_users
app.register_blueprint(app_match_users)

# Add Register Controller
from controllers.Register import app_register
app.register_blueprint(app_register)

# Add Register Controller
from controllers.Login import app_login
app.register_blueprint(app_login)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)