from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Doctor, Patient, Appointment
from app.routes.auth_decorator import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('Admin')
def admin_dashboard():
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    return render_template('admin_dashboard.html',total_doctors=total_doctors,total_patients=total_patients,total_appointments=total_appointments)


@admin_bp.route('/overview')
@login_required
@role_required('Admin')
def admin_overview():
    doctors = Doctor.query.order_by(Doctor.name).all()
    patients = Patient.query.order_by(Patient.name).all()
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin_overview.html', doctors=doctors, patients=patients, appointments=appointments)


@admin_bp.route('/doctors')
@login_required
@role_required('Admin')
def admin_doctors():
    doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template('admin_doctors.html', doctors=doctors)


@admin_bp.route('/patients')
@login_required
@role_required('Admin')
def admin_patients():
    patients = Patient.query.order_by(Patient.name).all()
    return render_template('admin_patients.html', patients=patients)


@admin_bp.route('/appointments')
@login_required
@role_required('Admin')
def admin_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc()).all()
    return render_template('admin_appointments.html', appointments=appointments)
