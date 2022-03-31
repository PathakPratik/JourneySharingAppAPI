from setup import db
import datetime
# this class is for creating tables in db

class Users(db.Model):
    
    __tablename__ = 'scheduled_jorney'

    id = db.Column(db.Integer, primary_key=True)
    source_longitude = db.Column(db.String(80), unique=True, nullable=False)
    source_latitude = db.Column(db.String(80), unique=True, nullable=False)
    destination_longitude = db.Column(db.String(80), unique=True, nullable=False)
    destination_latitude = db.Column(db.String(80), unique=True, nullable=False)
    weekday = db.Column(db.String(80), unique=True, nullable=False)
    hour = db.Column(db.String(80), unique=True, nullable=False)
    gender_preference =  db.Column(db.String(80), unique=True, nullable=False)
    required_rating = db.Column(db.String(80), unique=True, nullable=False)


    def __init__(self, source_longitude, source_latitude, \
                        destination_longitude, destination_latitude,
                             gender, password, admin, confirmed, confirmed_on):
        self.source_longitude = db.Column(db.String(80), unique=True, nullable=False)
        self.source_latitude = db.Column(db.String(80), unique=True, nullable=False)
        self.destination_longitude = db.Column(db.String(80), unique=True, nullable=False)
        self.destination_latitude = db.Column(db.String(80), unique=True, nullable=False)
        self.weekday = db.Column(db.String(80), unique=True, nullable=False)
        self.hour = db.Column(db.String(80), unique=True, nullable=False)
        self.gender_preference =  db.Column(db.String(80), unique=True, nullable=False)
        self.required_rating = db.Column(db.String(80), unique=True, nullable=False)

        