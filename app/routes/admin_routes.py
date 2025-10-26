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
    return render_template('admin_dashboard.html',
                           total_doctors=total_doctors,
                           total_patients=total_patients,
                           total_appointments=total_appointments)
