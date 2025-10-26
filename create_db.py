import os
from app import create_app, db
from app.models import User, Specialization, Doctor

app = create_app()

with app.app_context():
    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Absolute database path inside instance/
    db_path = os.path.join(app.instance_path, 'hms.db')

    # Always attempt to create tables (safe: create_all() is idempotent)
    db.create_all()
    print(f"✅ Ensured database and tables exist at: {db_path}")

    # Only insert sample data if it doesn't already exist
    if not User.query.filter_by(username='admin').first():
        # Create Admin User
        admin = User(username='admin', role='Admin')
        admin.set_password('supersecretadmin')
        db.session.add(admin)

    if not Specialization.query.filter_by(name='General Medicine').first():
        # Create a sample specialization
        specialization = Specialization(name='General Medicine', description='Primary Care')
        db.session.add(specialization)
        db.session.commit()
    else:
        specialization = Specialization.query.filter_by(name='General Medicine').first()

    if not User.query.filter_by(username='dr_sample').first():
        # Create Doctor User
        doctor_user = User(username='dr_sample', role='Doctor')
        doctor_user.set_password('doctorpass')
        db.session.add(doctor_user)
        db.session.commit()

        # Link Doctor User to Doctor Table
        doctor = Doctor(id=doctor_user.id, name='Dr. Alice Smith', specialization_id=specialization.id)
        db.session.add(doctor)
        db.session.commit()

    print("👨‍⚕️ Sample data ensured (admin + doctor + specialization).")

