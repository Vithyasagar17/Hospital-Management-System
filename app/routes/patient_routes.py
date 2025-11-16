from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.routes.auth_decorator import role_required
from app.models import Patient, Doctor, Appointment
from app import db
from datetime import datetime

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')


@patient_bp.route('/dashboard')
@login_required
@role_required('Patient')
def patient_dashboard():
    patient = Patient.query.filter_by(id=current_user.id).first()
    patient_name = patient.name if patient and patient.name else current_user.username
    return render_template('patient_dashboard.html', patient_name=patient_name)


@patient_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('Patient')
def patient_profile():
    patient = Patient.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        contact = request.form.get('contact', '').strip()
        address = request.form.get('address', '').strip()
        age = request.form.get('age')
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')

        if not name:
            flash('Full name is required.', 'warning')
            return redirect(url_for('patient.patient_profile'))

        if not patient:
            patient = Patient(id=current_user.id)
            db.session.add(patient)

        patient.name = name
        patient.contact = contact or None
        patient.address = address or None
        try:
            patient.age = int(age) if age else None
        except ValueError:
            patient.age = None
        patient.gender = gender or None
        try:
            patient.height = float(height) if height else None
        except ValueError:
            patient.height = None
        try:
            patient.weight = float(weight) if weight else None
        except ValueError:
            patient.weight = None

        db.session.commit()
        return redirect(url_for('patient.patient_dashboard'))

    return render_template('patient_profile.html', patient=patient)


@patient_bp.route('/medical-history')
@login_required
@role_required('Patient')
def medical_history():
    appointments = Appointment.query.filter_by(patient_id=current_user.id)\
        .order_by(Appointment.date.desc())\
        .all()
    return render_template('medical_history.html', appointments=appointments)

@patient_bp.route('/book_appointment', methods=['GET', 'POST'])
@login_required
@role_required('Patient')
def book_appointment():
    patient = Patient.query.filter_by(id=current_user.id).first()
    doctors = Doctor.query.all()
    
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        reason = request.form.get('reason')
        
        if not all([doctor_id, date_str, time_str, reason]):
            flash('All fields are required.', 'error')
            return redirect(url_for('patient.book_appointment'))
            
        try:
            date = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
            
            if date < datetime.now():
                flash('Cannot book appointments in the past.', 'error')
                return redirect(url_for('patient.book_appointment'))
            
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=doctor_id,
                date=date,
                time=time_str,  
                reason=reason,
                status='Pending'
            )
            
            db.session.add(appointment)
            db.session.commit()
            return redirect(url_for('patient.view_appointments'))
            
        except ValueError as e:
            flash('Invalid date or time format.', 'error')
            return redirect(url_for('patient.book_appointment'))
            
    return render_template('book_appointment.html', 
                           doctors=doctors, 
                           patient=patient,
                           now=datetime.now())

@patient_bp.route('/appointments')
@login_required
@role_required('Patient')
def view_appointments():
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(Appointment.date.desc()).all()
    return render_template('view_appointments.html', appointments=appointments)
