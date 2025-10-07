import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from werkzeug.routing import BuildError
from Database import db, User, Feedback, Student,FeedbackRboys,sunrise,Deccan,saidarbar, AdminRole
from admin import admin_bp

app = Flask(__name__)
# Generate a new secret key on every server start so old session cookies become invalid
app.secret_key = os.urandom(24)
# Make sessions non-permanent (they expire when the browser is closed)
app.config["SESSION_PERMANENT"] = False

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

# ----------------- Helper Functions -----------------
def is_logged_in_for_hostel(hostel_name):
    """Check if user is logged in specifically for this hostel"""
    return ("user" in session and 
            "logged_hostel" in session and 
            session["logged_hostel"] == hostel_name)

def clear_hostel_session_if_different(current_hostel):
    """Clear hostel session if user is switching to different hostel"""
    if "logged_hostel" in session and session["logged_hostel"] != current_hostel:
        # User is switching from one hostel to another - clear previous session quietly
        session.pop("user", None)
        session.pop("logged_hostel", None)
        # No flash message - just silently clear session

# Make function available in templates
app.jinja_env.globals.update(is_logged_in_for_hostel=is_logged_in_for_hostel)


@app.route("/landing")
def landing():
    # Landing page (used when skipping admin login)
    return render_template("landing.html")

@app.route("/start-admin", methods=["GET", "POST"])
def start_admin():
    if request.method == "POST":
        action = request.form.get("action")
        if action == "skip":
            # Continue as normal user to landing page
            return redirect(url_for("landing"))
        # Attempt admin login
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid credentials", "error")
            return render_template("start_admin.html")
        # Check admin role
        if AdminRole.query.filter_by(email=user.email).first() is None:
            flash("Only Admin can login here", "error")
            return render_template("start_admin.html")
        session["user"] = user.email
        return redirect(url_for("admin.dashboard"))
    return render_template("start_admin.html")
@app.route("/")
def home():
    # Show landing page as default
    return redirect(url_for("landing"))

@app.route("/first")
def first():
    return render_template("first.html")



@app.route("/RBoyshostel", methods=["GET","POST"])
def RBoyshostel():
    # Clear session if user is switching from different hostel
    clear_hostel_session_if_different("R Boys hostel")
    
    if request.method == "POST":
        if not is_logged_in_for_hostel("R Boys hostel"):
            flash("Please login to R Boys Hostel to submit feedback", "warning")
            return redirect(url_for("login", next_page="RBoyshostel"))
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
            fb = FeedbackRboys(
                email=email,
                hostel_name="R Boys hostel",
                rating=rating,
                feedback_text=feedback_text,
                media_file=media_file
            )
            db.session.add(fb)
            db.session.commit()
            flash("Feedback submitted successfully!", "success")
            return redirect(url_for("RBoyshostel"))
        else:
            flash("Please enter feedback text and select a rating.", "error")

    feedbacks = FeedbackRboys.query.filter_by(hostel_name="R Boys hostel").order_by(FeedbackRboys.timestamp.desc()).all()
    return render_template("RBoyshostel.html", feedbacks=feedbacks)



@app.route("/vritteGirlshostel", methods=["GET","POST"])
def vritteGirlshostel():
    # Clear session if user is switching from different hostel
    clear_hostel_session_if_different("VRIITEE Girls hostel")
    
    if request.method == "POST":
        if not is_logged_in_for_hostel("VRIITEE Girls hostel"):
            flash("Please login to VRIITEE Girls Hostel to submit feedback", "warning")
            return redirect(url_for("login", next_page="vritteGirlshostel"))

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
            return redirect(url_for("vritteGirlshostel"))
        else:
            flash("Please enter feedback text and select a rating.", "error")

    feedbacks = Feedback.query.filter_by(hostel_name="VRIITEE Girls hostel").order_by(Feedback.timestamp.desc()).all()
    return render_template("vritteGirlshostel.html", feedbacks=feedbacks)


@app.route("/sunrisehostel", methods=["GET", "POST"])
def sunrisehostel():
    # Clear session if user is switching from different hostel
    clear_hostel_session_if_different("Sunrise Hostel")
    
    if request.method == "POST":
        if not is_logged_in_for_hostel("Sunrise Hostel"):
            flash("Please login to Sunrise Hostel to submit feedback", "warning")
            return redirect(url_for("login", next_page="sunrisehostel"))

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
            fb = sunrise(
                email=email,
                hostel_name="Sunrise Hostel",
                rating=rating,
                feedback_text=feedback_text,
                media_file=media_file
            )
            db.session.add(fb)
            db.session.commit()
            flash("Feedback submitted successfully!", "success")
            return redirect(url_for("sunrisehostel"))
        else:
            flash("Please enter feedback text and select rating!", "error")

    feedbacks = sunrise.query.order_by(sunrise.timestamp.desc()).all()
    return render_template("sunrisehostel.html", feedbacks=feedbacks)



@app.route("/saiDarbar", methods=["GET", "POST"])
def saidarbar_page():
    # Clear session if user is switching from different hostel
    clear_hostel_session_if_different("SaiDarbar Hostel")
    
    if request.method == "POST":
        if not is_logged_in_for_hostel("SaiDarbar Hostel"):
            flash("Please login to SaiDarbar Hostel to submit feedback", "warning")
            return redirect(url_for("login", next_page="saiDarbar"))
        feedback_text = request.form.get("feedback_text", "").strip()
        rating_str = request.form.get("rating", "").strip()
        email = session["user"]

        try:
            rating = int(rating_str)
        except ValueError:
            rating = 0

        media_file = None
        file = request.files.get("media_file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            media_file = filename

        if feedback_text and rating > 0:
            fb = saidarbar(  
                email=email,
                hostel_name="SaiDarbar Hostel",  
                rating=rating,
                feedback_text=feedback_text,
                media_file=media_file
            )
            db.session.add(fb)
            db.session.commit()
            flash("Feedback submitted successfully!", "success")
            return redirect(url_for("saidarbar_page"))
        else:
            flash("Please enter feedback text and select a rating.", "error")

    feedbacks = saidarbar.query.filter_by(hostel_name="SaiDarbar Hostel").order_by(saidarbar.timestamp.desc()).all()
    return render_template("SaiDarbar.html", feedbacks=feedbacks)


@app.route("/deccanspace", methods=["GET", "POST"])
def deccanspace():
    # Clear session if user is switching from different hostel
    clear_hostel_session_if_different("Deccan Space Hostels")
    
    if request.method == "POST":
        if not is_logged_in_for_hostel("Deccan Space Hostels"):
            flash("Please login to Deccan Space Hostels to submit feedback", "warning")
            return redirect(url_for("login", next_page="deccanspace"))
        feedback_text = request.form.get("feedback_text", "").strip()
        rating_str = request.form.get("rating", "").strip()
        email = session["user"]

        try:
            rating = int(rating_str)
        except ValueError:
            rating = 0

        media_file = None
        file = request.files.get("media_file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            media_file = filename

        if feedback_text and rating > 0:
            fb = Deccan(
                email=email,
                hostel_name="Deccan Space Hostels",
                rating=rating,
                feedback_text=feedback_text,
                media_file=media_file
            )
            db.session.add(fb)
            db.session.commit()
            flash("Feedback submitted successfully!", "success")
            return redirect(url_for("deccanspace"))
        else:
            flash("Please enter feedback text and select a rating.", "error")

    feedbacks = Deccan.query.filter_by(hostel_name="Deccan Space Hostels").order_by(Deccan.timestamp.desc()).all()
    return render_template("deccanspace.html", feedbacks=feedbacks)


@app.route("/jbhostel", methods=["GET", "POST"])
def jbhostel():
    # Clear session if user is switching from different hostel
    clear_hostel_session_if_different("J B Hostel")
    
    if request.method == "POST":
        if not is_logged_in_for_hostel("J B Hostel"):
            flash("Please login to J B Hostel to submit feedback", "warning")
            return redirect(url_for("login", next_page="jbhostel"))

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
                hostel_name="J B Hostel",
                rating=rating,
                feedback_text=feedback_text,
                media_file=media_file
            )
            db.session.add(fb)
            db.session.commit()
            flash("Feedback submitted successfully!", "success")
            return redirect(url_for("jbhostel"))
        else:
            flash("Please enter feedback text and select a rating.", "error")

    feedbacks = Feedback.query.filter_by(hostel_name="J B Hostel").order_by(Feedback.timestamp.desc()).all()
    return render_template("Jbhostel.html", feedbacks=feedbacks)


@app.route("/registration/<hostel_name>", methods=["GET", "POST"])
def registration(hostel_name):
    # Clear any previous flash messages when accessing registration page
    session.pop('_flashes', None)
    
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
            
            # Redirect to the correct hostel page based on hostel_name
            hostel_page_map = {
                "vriitee_girls_hostel": "vritteGirlshostel",
                "r_boys_hostel": "RBoyshostel",
                "rboys_hostel": "RBoyshostel", 
                "sunrise_hostel": "sunrisehostel",
                "sai_darbar": "saiDarbar",
                "saidarbar": "saiDarbar",
                "deccan_space_hostel": "deccanspace",
                "deccan_space_hostels": "deccanspace",
                "j_b_hostel": "jbhostel",
                "jb_hostel": "jbhostel",
                "jbhostel": "jbhostel"
            }
            
            # Normalize hostel_name for lookup
            normalized_hostel = hostel_name.lower().replace(" ", "_").replace("-", "_")
            redirect_page = hostel_page_map.get(normalized_hostel, "first")
            
            try:
                return redirect(url_for(redirect_page))
            except:
                return redirect(url_for("first"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("registration", hostel_name=hostel_name))

    return render_template("registration.html", display_name=display_name, hostel_name=hostel_name)



@app.route("/signup", methods=["GET", "POST"])
def signup():
    next_hostel = request.args.get("next_hostel")
    next_page = request.args.get("next_page")
    
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        cpassword = request.form["cpassword"]

        if password != cpassword:
            flash("Passwords do not match", "error")
            return redirect(url_for("signup", next_hostel=next_hostel, next_page=next_page))

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for("signup", next_hostel=next_hostel, next_page=next_page))

        new_user = User(fullname=fullname, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup Successful! Please Login", "success")
        return redirect(url_for("login", next_hostel=next_hostel, next_page=next_page))

    return render_template("signup.html", next_hostel=next_hostel, next_page=next_page)



@app.route("/login", methods=["GET", "POST"])
def login():
    next_hostel = request.form.get("next_hostel") or request.args.get("next_hostel")
    next_page = request.form.get("next_page") or request.args.get("next_page")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("⚠️ Email not registered! Please signup first.", "error")
            return render_template("login.html", next_hostel=next_hostel, next_page=next_page)

        if user.check_password(password):
            session["user"] = user.email
            
            # Store hostel-specific login
            if next_page:
                # Map pages to hostel names for hostel-specific login
                hostel_map = {
                    "vritteGirlshostel": "VRIITEE Girls hostel",
                    "RBoyshostel": "R Boys hostel", 
                    "sunrisehostel": "Sunrise Hostel",
                    "saiDarbar": "SaiDarbar Hostel",
                    "deccanspace": "Deccan Space Hostels",
                    "jbhostel": "J B Hostel"
                }
                if next_page in hostel_map:
                    session["logged_hostel"] = hostel_map[next_page]

            if next_hostel:
                return redirect(url_for("registration", hostel_name=next_hostel))
            elif next_page:
                try:
                    return redirect(url_for(next_page))
                except BuildError:
                    path = next_page if next_page.startswith('/') else f'/{next_page}'
                    return redirect(path)
            else:
                return redirect(url_for("first"))
        else:
            flash("Incorrect Password. Try again.", "error")
            return render_template("login.html", next_hostel=next_hostel, next_page=next_page)

    return render_template("login.html", next_hostel=next_hostel, next_page=next_page)

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("logged_hostel", None)  # Clear hostel-specific login
    flash("Logged out successfully", "info")
    return redirect(url_for("landing"))


@app.route("/debug/session")
def debug_session():
    return {
        'session_user': session.get('user'),
        'session_keys': list(session.keys()),
        'logged_hostel': session.get('logged_hostel'),
        'is_logged_in': 'user' in session,
        'session_clearing_enabled': True,
        'hostel_checks': {
            'VRIITEE Girls hostel': is_logged_in_for_hostel('VRIITEE Girls hostel'),
            'R Boys hostel': is_logged_in_for_hostel('R Boys hostel'),
            'Sunrise Hostel': is_logged_in_for_hostel('Sunrise Hostel'),
            'SaiDarbar Hostel': is_logged_in_for_hostel('SaiDarbar Hostel'),
            'Deccan Space Hostels': is_logged_in_for_hostel('Deccan Space Hostels'),
            'J B Hostel': is_logged_in_for_hostel('J B Hostel')
        }
    }

# Register admin blueprint
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
