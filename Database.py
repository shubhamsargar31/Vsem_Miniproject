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
        """Password Hashing"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Password Verification"""
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
    surname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50))
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    education = db.Column(db.String(120), nullable=False)
    college_name = db.Column(db.String(200), nullable=False)
    aadhar = db.Column(db.String(12), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    ac_room = db.Column(db.String(20), nullable=False)
    gym = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=False)
    hostel_name = db.Column(db.String(100), nullable=False)
    college_id_photo = db.Column(db.String(200), nullable=True) 