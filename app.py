from flask import Flask
from constants import FLASK_HOSTNAME, FLASK_PORT, REDIS_HOST, REDIS_PORT
import redis

app = Flask(__name__)
redisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# Home route
@app.route("/")
def home():
    return "<p>Welcome!</p>"

# Add MatchUsers Controller
from controllers.MatchUsers import app_match_users
app.register_blueprint(app_match_users)

if __name__ == "__main__":
    app.run(debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)