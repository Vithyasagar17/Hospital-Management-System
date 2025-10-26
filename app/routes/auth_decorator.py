from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(role):
    """Decorator to restrict access by user role."""
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash(f"Access denied. Only {role}s allowed.", 'danger')
                return redirect(url_for('auth.login'))
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
