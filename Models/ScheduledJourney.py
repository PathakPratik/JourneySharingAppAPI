from enum import unique
from venv import create
from setup import db
import datetime
# this class is for creating tables in db

class ScheduledJourney(db.Model):
    
    __tablename__ = 'scheduled_jorney'

    id = db.Column(db.Integer, primary_key=True)
    journey_name = db.Column(db.String(80), unique= True, nullable=False)
    creator_id = db.Column(db.String(80), nullable=False)
    source_longitude = db.Column(db.String(200), nullable=False)
    source_latitude = db.Column(db.String(200), nullable=False)
    destination_longitude = db.Column(db.String(200), nullable=False)
    destination_latitude = db.Column(db.String(200), nullable=False)
    weekday = db.Column(db.String(80), nullable=False)
    hour = db.Column(db.String(80), nullable=False)
    gender_preference =  db.Column(db.String(80), nullable=True)
    required_rating = db.Column(db.String(80), nullable=True)
    quota = db.Column(db.String(80), nullable=True)
    members = db.Column(db.String(100), nullable=False)


    def __init__(self,
                creator_id,
                journey_name,
                source_longitude,
                source_latitude, 
                destination_longitude,
                destination_latitude, 
                weekday,
                hour, 
                gender_preference,
                required_rating,
                quota):

        self.creator_id = creator_id  
        self.journey_name = journey_name          
        self.source_longitude = source_longitude
        self.source_latitude = source_latitude
        self.destination_longitude = destination_longitude 
        self.destination_latitude = destination_latitude
        self.weekday = weekday
        self.hour = hour
        self.gender_preference =  gender_preference
        self.required_rating = required_rating
        self.quota = quota
        self.members = str(creator_id) + "/"

        