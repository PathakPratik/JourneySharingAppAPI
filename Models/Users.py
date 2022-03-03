from setup import db
import datetime
# this class is for creating tables in db

class Users(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, username, email, gender, password, admin, confirmed, confirmed_on):
        self.username = username
        self.email = email
        self.gender = gender
        self.password = password
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on

        