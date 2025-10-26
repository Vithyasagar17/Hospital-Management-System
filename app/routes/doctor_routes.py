from flask import Blueprint, render_template
from flask_login import login_required
from app.routes.auth_decorator import role_required

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@doctor_bp.route('/dashboard')
@login_required
@role_required('Doctor')
def doctor_dashboard():
    return render_template('doctor_dashboard.html')
