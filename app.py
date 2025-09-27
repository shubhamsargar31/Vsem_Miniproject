import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from Database import db, User, Feedback, Student

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ----------------- DB Config -----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:shubham123@localhost/hostel_finder"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# File Upload Config
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

# ----------------- Create Tables -----------------
with app.app_context():
    db.create_all()

# ----------------- Routes -----------------
@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/first")
def first():
    return render_template("first.html")

@app.route("/Deccan")
def deccan():
    return render_template("deccanspace.html")

@app.route("/sbphule")
def sbphule():
    return render_template("sbphule.html")

# ----------------- Hostel Pages -----------------
@app.route("/sunrisehostel", methods=["GET", "POST"])
def sunrisehostel():
    if request.method == "POST":
        feedback_text = request.form.get("feedback")
        rating = request.form.get("rating")

        if "user" not in session:
            flash(" Please login to give feedback", "warning")
            return redirect(url_for("login", next_hostel="sunrisehostel"))

        if not feedback_text or not rating:
            flash(" Feedback and rating required!", "error")
            return redirect(url_for("sunrisehostel"))

        fb = Feedback(rating=int(rating), feedback_text=feedback_text)
        db.session.add(fb)
        db.session.commit()

        flash(" Feedback submitted successfully!", "success")
        return redirect(url_for("sunrisehostel"))

    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    return render_template("sunrisehostel.html", feedbacks=feedbacks)


@app.route("/vritteGirlshostel")
def vritteGirlshostel():
    return render_template("vritteGirlshostel.html")

@app.route("/saiDarbar")
def saidarbar():
    return render_template("SaiDarbar.html")
@app.route("/RBoyshostel")
def RBoyshostel():
    return render_template("RBoyshostel.html")

# ----------------- Student Registration -----------------
@app.route("/registration/<hostel_name>", methods=["GET", "POST"])
def registration(hostel_name):
    display_name = hostel_name.replace("_", " ").title()  

    if request.method == "POST":
        try:
            file = request.files.get("college_id_photo")
            filename = None
            if file and file.filename.strip() != "":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            student = Student(
                surname=request.form.get("surname"),
                firstname=request.form.get("firstname"),
                middlename=request.form.get("middlename"),
                email=request.form.get("email"),
                phone=request.form.get("phone"),
                gender=request.form.get("gender"),
                dob=request.form.get("dob"),
                education=request.form.get("education"),
                college_name=request.form.get("college_name"),
                aadhar=request.form.get("aadhar"),
                room=request.form.get("room"),
                ac_room=request.form.get("ac_room"),
                gym=request.form.get("gym"),
                address=request.form.get("address"),
                hostel_name=display_name,
                college_id_photo=filename,
            )
            db.session.add(student)
            db.session.commit()

            flash(f" Registered successfully in {display_name}", "success")
            return redirect(url_for("home"))

        except Exception as e:
            db.session.rollback()
            flash(f"⚠️ Error: {str(e)}", "error")
            return redirect(url_for("registration", hostel_name=hostel_name))

    return render_template("registration.html", hostel_name=hostel_name, display_name=display_name)
# ----------------- Login -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    next_hostel = request.args.get("next_hostel")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("⚠️ Email not registered! Please signup first.", "error")
            return redirect(url_for("signup"))

        if user.check_password(password):
            session["user"] = user.email

            if next_hostel:
                return redirect(url_for("registration", hostel_name=next_hostel))
            else:
                return redirect(url_for("first"))  
        else:
            flash("Incorrect Password. Try again.", "error")
            return redirect(url_for("login"))

    return render_template("login.html", next_hostel=next_hostel)

# ----------------- Logout -----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash(" Logged out successfully", "info")
    return redirect(url_for("login"))

# ----------------- Main -----------------
if __name__ == "__main__":
    app.run(debug=True)
