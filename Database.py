from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    


    
class saidarbar(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    hostel_name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    media_file = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Deccan(db.Model):  # Model name matches your table
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    hostel_name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    media_file = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class sunrise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    hostel_name = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    media_file = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    hostel_name = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    media_file = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class FeedbackRboys(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    hostel_name = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    media_file = db.Column(db.String(250))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostel_name = db.Column(db.String(150), nullable=False)
    surname = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    middlename = db.Column(db.String(100))
    email = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    dob = db.Column(db.String(20))
    address = db.Column(db.Text)
    parent_surname = db.Column(db.String(100))
    parent_firstname = db.Column(db.String(100))
    parent_middlename = db.Column(db.String(100))
    parent_phone = db.Column(db.String(20))
    parent_email = db.Column(db.String(150))
    education = db.Column(db.String(100))
    college_name = db.Column(db.String(150))
    aadhar = db.Column(db.String(20))
    college_id_photo = db.Column(db.String(250))
    room = db.Column(db.String(50))
    ac_room = db.Column(db.String(50))
    gym = db.Column(db.String(50))
