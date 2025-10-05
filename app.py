import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from Database import db, User, Feedback, Student

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ----------------- DB Config -----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:shubham123@localhost/hostel_finder"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# File Upload Config
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"png","jpg","jpeg","gif","mp4","mov","webm"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

db.init_app(app)
with app.app_context():
    db.create_all()

# ----------------- Routes -----------------
@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/first")
def first():
    return render_template("first.html")

@app.route("/vritteGirlshostel", methods=["GET","POST"])
def vritteGirlshostel():
    if request.method == "POST":
        if "user" not in session:
            flash("Please login to submit feedback", "warning")
            return redirect(url_for("login", next_hostel="VRIITEE Girls hostel"))

        feedback_text = request.form.get("feedback_text", "").strip()
        rating_str = request.form.get("rating", "").strip()
        email = session["user"]

        try:
            rating = int(rating_str) if rating_str else 0
        except ValueError:
            rating = 0

        media_file = None
        file = request.files.get("media_file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            media_file = filename

        if feedback_text and rating > 0:
            fb = Feedback(
                email=email,
                hostel_name="VRIITEE Girls hostel",
                rating=rating,
                feedback_text=feedback_text,
                media_file=media_file
            )
            db.session.add(fb)
            db.session.commit()
            # flash("Feedback submitted successfully!", "success")
            return redirect(url_for("vritteGirlshostel"))
        else:
            flash("Please enter feedback text and select a rating.", "error")

    feedbacks = Feedback.query.filter_by(hostel_name="VRIITEE Girls hostel").order_by(Feedback.timestamp.desc()).all()
    return render_template("vritteGirlshostel.html", feedbacks=feedbacks)



@app.route("/registration/<hostel_name>", methods=["GET", "POST"])
def registration(hostel_name):
    display_name = hostel_name.replace("_", " ").title()
    if "user" not in session:
        flash("You must login before registration", "warning")
        return redirect(url_for("login", next_hostel=hostel_name))

    if request.method == "POST":
        try:
            file = request.files.get("college_id_photo")
            filename = None
            if file and file.filename.strip() != "":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            student = Student(
                hostel_name = request.form.get("hostelName"),
                surname = request.form.get("surname"),
                firstname = request.form.get("firstname"),
                middlename = request.form.get("middlename"),
                email = request.form.get("email"),
                phone = request.form.get("phone"),
                gender = request.form.get("gender"),
                dob = request.form.get("dob"),
                address = request.form.get("address"),
                parent_surname = request.form.get("parent_surname"),
                parent_firstname = request.form.get("parent_firstname"),
                parent_middlename = request.form.get("parent_middlename"),
                parent_phone = request.form.get("parent_phone"),
                parent_email = request.form.get("parent_email"),
                education = request.form.get("education"),
                college_name = request.form.get("college_name"),
                aadhar = request.form.get("aadhar"),
                college_id_photo = filename,
                room = request.form.get("room"),
                ac_room = request.form.get("ac_room"),
                gym = request.form.get("gym")
            )

            db.session.add(student)
            db.session.commit()
            flash(f"Registered successfully in {display_name}", "success")
            return redirect(url_for("vritteGirlshostel"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("registration", hostel_name=hostel_name))

    return render_template("registration.html", display_name=display_name, hostel_name=hostel_name)



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        cpassword = request.form["cpassword"]

        if password != cpassword:
            flash("Passwords do not match", "error")
            return redirect(url_for("signup"))

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for("signup"))

        new_user = User(fullname=fullname, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup Successful! Please Login", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    next_hostel = request.form.get("next_hostel") or request.args.get("next_hostel")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("⚠️ Email not registered! Please signup first.", "error")
            return render_template("login.html", next_hostel=next_hostel)

        if user.check_password(password):
            session["user"] = user.email

            if next_hostel:
                return redirect(url_for("registration", hostel_name=next_hostel))
            else:
                return redirect(url_for("first")) 
        else:
            flash("Incorrect Password. Try again.", "error")
            return render_template("login.html", next_hostel=next_hostel)

    return render_template("login.html", next_hostel=next_hostel)

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
