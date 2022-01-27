from flask import Flask,request,jsonify
from constants import FLASK_HOSTNAME, FLASK_PORT, REDIS_HOST, REDIS_PORT
from flask_sqlalchemy import SQLAlchemy
import redis

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:'DB_PASSWORD'@localhost/DB_NAME'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
redisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

# this class is for creating tables in db
class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route("/login",methods=["GET", "POST"])
def login():
    d = {}
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]
        
        login = user.query.filter_by(username=uname, password=passw).first()

        if login is not None:
            # account found
            d["status"] = 11
            return jsonify(d)
        else:
            # account not exist
            d["status"] = 22
            return jsonify(d)
            

@app.route("/register", methods=["GET", "POST"])
def register():
    d = {}
    if request.method == "POST":
        uname = request.form['uname']
        mail = request.form['mail']
        passw = request.form['passw']
        username = user.query.filter_by(username=uname).first()
        if username is None:
            register = user(uname,mail,passw)
            db.session.add(register)
            db.session.commit()
            d["status"] = 11
            return jsonify(d)
        else:
            # already exist
            d["status"] = 22
            return jsonify(d)

# Add MatchUsers Controller
from controllers.MatchUsers import app_match_users
app.register_blueprint(app_match_users)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host=FLASK_HOSTNAME, port=FLASK_PORT)
