"""Package initializer for app.routes.

This module re-exports the Blueprint objects defined in the individual
route modules so callers can do::

	from app.routes import auth_bp, admin_bp, doctor_bp, patient_bp

instead of importing each submodule directly.
"""

# Import and re-export the blueprints defined in the route modules
from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .doctor_routes import doctor_bp
from .patient_routes import patient_bp

__all__ = [
	'auth_bp',
	'admin_bp',
	'doctor_bp',
	'patient_bp',
]
