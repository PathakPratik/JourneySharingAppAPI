from setup import db

# this class is for creating tables in db

class Users(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, email, gender, password):
        self.username = username
        self.email = email
        self.gender = gender
        self.password = password
    

        