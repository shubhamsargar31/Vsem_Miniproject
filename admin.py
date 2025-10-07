from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from functools import wraps
from Database import db, User, Student, Feedback, FeedbackRboys, sunrise, Deccan, saidarbar, AdminRole, Hostel
from sqlalchemy import func, or_
import os
import json

# Automatic export function
def export_hostels_to_json():
    """Automatically export hostels to JSON file after any database operation"""
    try:
        out_path = os.path.join(current_app.root_path, 'static', 'hostels.json')
        
        # Read existing JSON to preserve original data
        existing_data = {}
        try:
            with open(out_path, 'r', encoding='utf-8') as f:
                existing_json = json.load(f)
                for item in existing_json:
                    key = item.get('page') or item.get('name', '')
                    existing_data[key] = item
        except (FileNotFoundError, json.JSONDecodeError):
            print("No existing JSON file found or invalid JSON, creating new one")
        
        hostels = Hostel.query.order_by(Hostel.id.asc()).all()
        payload = []
        
        for h in hostels:
            try:
                rooms = json.loads(h.rooms) if h.rooms else []
            except Exception:
                rooms = []
            try:
                types = json.loads(h.types) if h.types else []
            except Exception:
                types = []
            
            # Check if this hostel exists in existing JSON
            existing_item = existing_data.get(h.page) or existing_data.get(h.name)
            
            # If exists, preserve original data but update from database
            if existing_item:
                hostel_data = {
                    "id": str(h.id),
                    "name": h.name,
                    "mess": h.mess,
                    "type": h.type,
                    "img": existing_item.get('img', h.img or ""),  # Preserve original image
                    "hostel_name": h.name,
                    "page": h.page,
                    "rooms": rooms if rooms else existing_item.get('rooms', []),  # Use DB data if available
                    "types": types if types else existing_item.get('types', []),  # Use DB data if available
                    "gym": bool(h.gym) if h.gym is not None else existing_item.get('gym', False),
                }
            else:
                # New hostel, use database data
                hostel_data = {
                    "id": str(h.id),
                    "name": h.name,
                    "mess": h.mess,
                    "type": h.type,
                    "img": h.img or "/static/default-hostel.png",
                    "hostel_name": h.name,
                    "page": h.page,
                    "rooms": rooms,
                    "types": types,
                    "gym": bool(h.gym),
                }
            
            payload.append(hostel_data)
        
        # Write updated JSON
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Auto-exported {len(payload)} hostels to hostels.json (preserved existing data)")
        return True
    except Exception as e:
        print(f"❌ Auto-export failed: {e}")
        return False

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        email = session.get('user')
        if not email:
            flash('Session expired. Please login again.', 'warning')
            return redirect(url_for('start_admin'))
        role = AdminRole.query.filter_by(email=email).first()
        if not role:
            flash('Admin access required', 'error')
            return redirect(url_for('start_admin'))
        return view(*args, **kwargs)
    return wrapped

@admin_bp.route('/')
@admin_required
def dashboard():
    counts = {
        'users': User.query.count(),
        'students': Student.query.count(),
        'feedback_total': (
            Feedback.query.count() +
            FeedbackRboys.query.count() +
            sunrise.query.count() +
            Deccan.query.count() +
            saidarbar.query.count()
        ),
        'hostels': Hostel.query.count(),
    }
    latest_regs = Student.query.order_by(Student.id.desc()).limit(5).all()
    return render_template('admin/dashboard.html', counts=counts, latest_regs=latest_regs)

@admin_bp.route('/feedbacks')
@admin_required
def feedbacks():
    items = []
    sources = [
        (Feedback, 'Generic/JB/VRIITEE'),
        (FeedbackRboys, 'R Boys'),
        (sunrise, 'Sunrise'),
        (Deccan, 'Deccan Space'),
        (saidarbar, 'Sai Darbar'),
    ]
    for model, label in sources:
        for fb in model.query.order_by(model.timestamp.desc()).limit(300).all():
            items.append({
                'id': fb.id,
                'model': model.__name__,
                'hostel': label,
                'email': fb.email,
                'rating': fb.rating,
                'text': fb.feedback_text,
                'media_file': getattr(fb, 'media_file', None),
                'timestamp': fb.timestamp,
            })
    return render_template('admin/feedbacks.html', items=items)

@admin_bp.post('/feedbacks/delete')
@admin_required
def delete_feedback():
    model_name = request.form.get('model')
    fid = request.form.get('id', type=int)
    model_map = {
        'Feedback': Feedback, 'FeedbackRboys': FeedbackRboys,
        'sunrise': sunrise, 'Deccan': Deccan, 'saidarbar': saidarbar
    }
    model = model_map.get(model_name)
    if not model or fid is None:
        flash('Invalid delete request', 'error')
        return redirect(url_for('admin.feedbacks'))
    obj = model.query.get(fid)
    if obj:
        db.session.delete(obj)
        db.session.commit()
        flash('Feedback deleted', 'success')
    return redirect(url_for('admin.feedbacks'))

@admin_bp.route('/students')
@admin_required
def students():
    search_query = request.args.get('search', '').strip()
    
    if search_query:
        # Search by name (firstname, middlename, surname) or email
        rows = Student.query.filter(
            or_(
                Student.firstname.ilike(f'%{search_query}%'),
                Student.middlename.ilike(f'%{search_query}%'),
                Student.surname.ilike(f'%{search_query}%'),
                Student.email.ilike(f'%{search_query}%')
            )
        ).order_by(Student.id.desc()).limit(500).all()
    else:
        rows = Student.query.order_by(Student.id.desc()).limit(500).all()
    
    return render_template('admin/students.html', rows=rows, search_query=search_query)

# ---------- Hostels Management ----------
@admin_bp.route('/hostels')
@admin_required
def hostels():
    rows = Hostel.query.order_by(Hostel.id.desc()).all()
    return render_template('admin/hostels.html', rows=rows)

@admin_bp.route('/hostels/new', methods=['GET','POST'])
@admin_required
def hostels_new():
    if request.method == 'POST':
        try:
            h = Hostel(
                name=request.form['name'],
                page=request.form['page'],
                mess=request.form.get('mess'),
                type=request.form.get('type'),
                rooms=json.dumps([r.strip() for r in request.form.get('rooms','').split(',') if r.strip()]),
                types=json.dumps([t.strip() for t in request.form.get('types','').split(',') if t.strip()]),
                gym=(request.form.get('gym') == 'on'),
                img=request.form.get('img','')
            )
            db.session.add(h)
            db.session.commit()
            # Automatically export to JSON after adding
            export_hostels_to_json()
            flash('Hostel created successfully! JSON file updated.', 'success')
            return redirect(url_for('admin.hostels'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating hostel: {str(e)}', 'error')
            print(f"Error creating hostel: {e}")  # For debugging
    return render_template('admin/hostel_form.html', hostel=None)

@admin_bp.route('/hostels/<int:id>/edit', methods=['GET','POST'])
@admin_required
def hostels_edit(id):
    h = Hostel.query.get_or_404(id)
    if request.method == 'POST':
        try:
            h.name = request.form['name']
            h.page = request.form['page']
            h.mess = request.form.get('mess')
            h.type = request.form.get('type')
            h.rooms = json.dumps([r.strip() for r in request.form.get('rooms','').split(',') if r.strip()])
            h.types = json.dumps([t.strip() for t in request.form.get('types','').split(',') if t.strip()])
            h.gym = (request.form.get('gym') == 'on')
            h.img = request.form.get('img','')
            db.session.commit()
            # Automatically export to JSON after updating
            export_hostels_to_json()
            flash('Hostel updated successfully! JSON file updated.', 'success')
            return redirect(url_for('admin.hostels'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating hostel: {str(e)}', 'error')
            print(f"Error updating hostel: {e}")  # For debugging
    return render_template('admin/hostel_form.html', hostel=h)

@admin_bp.post('/hostels/<int:id>/delete')
@admin_required
def hostels_delete(id):
    try:
        h = Hostel.query.get_or_404(id)
        hostel_name = h.name  # Store name for success message
        db.session.delete(h)
        db.session.commit()
        # Automatically export to JSON after deleting
        export_hostels_to_json()
        flash(f'Hostel "{hostel_name}" deleted successfully! JSON file updated.', 'success')
        return redirect(url_for('admin.hostels'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting hostel: {str(e)}', 'error')
        print(f"Error deleting hostel: {e}")  # For debugging
        return redirect(url_for('admin.hostels'))

@admin_bp.route('/hostels/<int:id>')
@admin_required
def hostels_view(id):
    h = Hostel.query.get_or_404(id)
    # Students for this hostel (case-insensitive name match)
    students = Student.query.filter(func.lower(Student.hostel_name) == func.lower(h.name)).order_by(Student.id.desc()).all()

    # Feedbacks across all tables, matching by name (case-insensitive) or partial
    fb_items = []
    def collect(Model, label):
        rows_eq = Model.query.filter(func.lower(Model.hostel_name) == func.lower(h.name)).all()
        rows_like = Model.query.filter(Model.hostel_name.ilike(f"%{h.name}%")).all()
        rows = {r.id: r for r in rows_eq}
        for r in rows_like:
            rows.setdefault(r.id, r)
        for r in rows.values():
            fb_items.append({
                'model': Model.__name__,
                'hostel': label,
                'email': r.email,
                'rating': getattr(r, 'rating', None),
                'text': getattr(r, 'feedback_text', ''),
                'media_file': getattr(r, 'media_file', None),
                'timestamp': getattr(r, 'timestamp', None),
            })

    collect(Feedback, 'Generic/JB/VRIITEE')
    collect(FeedbackRboys, 'R Boys')
    collect(sunrise, 'Sunrise')
    collect(Deccan, 'Deccan Space')
    collect(saidarbar, 'Sai Darbar')

    fb_items.sort(key=lambda x: (x['timestamp'] or ''), reverse=True)

    return render_template('admin/hostel_view.html', hostel=h, students=students, feedbacks=fb_items)

@admin_bp.post('/hostels/export')
@admin_required
def hostels_export():
    # Export hostels to static/hostels.json so registration page can use it
    hostels = Hostel.query.order_by(Hostel.id.asc()).all()
    payload = []
    for h in hostels:
        try:
            rooms = json.loads(h.rooms) if h.rooms else []
        except Exception:
            rooms = []
        try:
            types = json.loads(h.types) if h.types else []
        except Exception:
            types = []
        payload.append({
            "id": str(h.id),
            "name": h.name,
            "mess": h.mess,
            "type": h.type,
            "img": h.img or "",
            "hostel_name": h.name,
            "page": h.page,
            "rooms": rooms,
            "types": types,
            "gym": bool(h.gym),
        })
    out_path = os.path.join(current_app.root_path, 'static', 'hostels.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    flash('Exported hostels to static/hostels.json', 'success')
    return redirect(url_for('admin.hostels'))

@admin_bp.post('/hostels/import')
@admin_required
def hostels_import():
    # Import hostels from static/hostels.json into DB (upsert by page or name)
    src_path = os.path.join(current_app.root_path, 'static', 'hostels.json')
    if not os.path.exists(src_path):
        flash('static/hostels.json not found', 'error')
        return redirect(url_for('admin.hostels'))
    try:
        with open(src_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        flash(f'Failed to read hostels.json: {e}', 'error')
        return redirect(url_for('admin.hostels'))

    created = 0
    updated = 0
    for item in (data or []):
        page = (item.get('page') or '').strip()
        name = (item.get('name') or item.get('hostel_name') or '').strip()
        mess = item.get('mess')
        htype = item.get('type')
        rooms = item.get('rooms') or []
        types = item.get('types') or []
        gym = bool(item.get('gym', False))
        img = item.get('img') or ''

        # Try upsert by page first, else by name
        h = None
        if page:
            h = Hostel.query.filter_by(page=page).first()
        if not h and name:
            h = Hostel.query.filter_by(name=name).first()
        if not h:
            h = Hostel(name=name or page or 'Hostel', page=page or name.replace(' ', '')[:50] or 'hostel')
            created += 1
            db.session.add(h)
        else:
            updated += 1
        h.mess = mess
        h.type = htype
        try:
            h.rooms = json.dumps(rooms)
        except Exception:
            h.rooms = json.dumps([])
        try:
            h.types = json.dumps(types)
        except Exception:
            h.types = json.dumps([])
        h.gym = gym
        h.img = img

    db.session.commit()
    flash(f'Imported hostels.json (created {created}, updated {updated})', 'success')
    return redirect(url_for('admin.hostels'))
