from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ----------------- User Table -----------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# ----------------- Feedback Table -----------------
class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())


# ----------------- Student Registration Table -----------------
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    # Student Personal Details
    hostel_name = db.Column(db.String(100), nullable=False)
    Surname = db.Column(db.String(50), nullable=False)
    Firstname = db.Column(db.String(50), nullable=False)
    Middlename = db.Column(db.String(50))
    Email = db.Column(db.String(120), nullable=False)
    Phone = db.Column(db.String(15), nullable=False)
    Gender = db.Column(db.String(10), nullable=False)
    DOB = db.Column(db.String(20), nullable=False)
    Address = db.Column(db.Text, nullable=False)

    # Parent Details
    parent_surname = db.Column(db.String(50), nullable=False)
    parent_firstname = db.Column(db.String(50), nullable=False)
    parent_middlename = db.Column(db.String(50))
    parent_phone = db.Column(db.String(15), nullable=False)
    parent_email = db.Column(db.String(120), nullable=False)

    # Academic Details
    Education = db.Column(db.String(120), nullable=False)
    College_name = db.Column(db.String(200), nullable=False)
    Aadhar = db.Column(db.String(12), nullable=False)
    College_id_photo = db.Column(db.String(200), nullable=True)

    # Hostel Preferences
    Room = db.Column(db.String(50), nullable=False)
    Ac_room = db.Column(db.String(20), nullable=False)
    Gym = db.Column(db.String(10), nullable=True)
