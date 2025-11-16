from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Patient, Doctor, Specialization

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            if user.role == 'Admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'Doctor':
                return redirect(url_for('doctor.doctor_dashboard'))
            elif user.role == 'Patient':
                return redirect(url_for('patient.patient_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'Patient')

        name = request.form.get('name', '').strip()
        contact = request.form.get('contact', '').strip()
        address = request.form.get('address', '').strip()

        if not username or not password:
            flash('Username and password are required.', 'warning')
        elif role in ('Patient', 'Doctor') and not name:
            flash('Full name is required for Doctors and Patients.', 'warning')
        elif User.query.filter_by(username=username).first():
            flash('Username already exists', 'warning')
        else:
            user = User(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            if role == 'Patient':
                patient = Patient(id=user.id, name=name or None, contact=contact or None, address=address or None)
                db.session.add(patient)
                db.session.commit()

                login_user(user)
                return redirect(url_for('patient.patient_profile'))

            elif role == 'Doctor':
                spec_id = request.form.get('specialization')
                try:
                    spec_id = int(spec_id) if spec_id else None
                except ValueError:
                    spec_id = None

                doctor = Doctor(id=user.id, name=name, specialization_id=spec_id)
                db.session.add(doctor)
                db.session.commit()

            return redirect(url_for('auth.login'))
    specializations = Specialization.query.order_by(Specialization.name).all()
    return render_template('register.html', specializations=specializations)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
