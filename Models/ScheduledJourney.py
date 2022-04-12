from setup import db

class ScheduledJourney(db.Model):
    
    __tablename__ = 'schduled_journeys'

    id = db.Column(db.Integer, primary_key=True)
    creatorId = db.Column(db.String(80), unique=True, nullable=False)
    TripStartLocation = db.Column(db.String(120), unique=True, nullable=False)
    TripStopLocation = db.Column(db.String(120), unique=True, nullable=False)
    ScheduleTime = db.Column(db.String(120), nullable=False)
    GenderPreference = db.Column(db.String(120), nullable=True)
    RequiredRating = db.Column(db.String(120), nullable=True)
    ModeOfTransport = db.Column(db.String(120), nullable=True, default=False)
    

    def __init__(self, creatorId, TripStartLocation, TripStopLocation, ScheduleTime, GenderPreference, RequiredRating, ModeOfTransport):
        self.creatorId = creatorId
        self.TripStartLocation = TripStartLocation
        self.TripStopLocation = TripStopLocation
        self.ScheduleTime = ScheduleTime
        self.GenderPreference = GenderPreference
        self.RequiredRating = RequiredRating
        self.ModeOfTransport = ModeOfTransport