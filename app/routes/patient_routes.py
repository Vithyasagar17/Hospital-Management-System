from flask import Blueprint, render_template
from flask_login import login_required
from app.routes.auth_decorator import role_required

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')

@patient_bp.route('/dashboard')
@login_required
@role_required('Patient')
def patient_dashboard():
    return render_template('patient_dashboard.html')
