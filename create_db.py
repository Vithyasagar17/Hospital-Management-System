import os
from app import create_app, db
from app.models import User, Specialization, Doctor, Patient

app = create_app()

with app.app_context():
    os.makedirs(app.instance_path, exist_ok=True)

    db_path = os.path.join(app.instance_path, 'hms.db')
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    db.create_all()

    from sqlalchemy import text
    
    try:
        existing_appt_cols = {row[1] for row in db.session.execute(text("PRAGMA table_info('appointment')")).fetchall()}
    except Exception:
        existing_appt_cols = set()

    appt_extras = {
        'notes': 'TEXT',
        'created_at': 'DATETIME',
        'updated_at': 'DATETIME'
    }

    for col, sqltype in appt_extras.items():
        if col not in existing_appt_cols:
            try:
                db.session.execute(text(f"ALTER TABLE appointment ADD COLUMN {col} {sqltype}"))
            except Exception as e:
                # Could not add column; keep original exception handling but avoid printing
                _ = e
    db.session.commit()

    try:
        existing_cols = {row[1] for row in db.session.execute(text("PRAGMA table_info('patient')")).fetchall()}
    except Exception:
        existing_cols = set()

    extras = {
        'age': 'INTEGER',
        'gender': 'VARCHAR(20)',
        'height': 'REAL',
        'weight': 'REAL',
    }

    for col, sqltype in extras.items():
        if col not in existing_cols:
            try:
                db.session.execute(text(f"ALTER TABLE patient ADD COLUMN {col} {sqltype}"))
            except Exception as e:
                # Could not add column; keep original exception handling but avoid printing
                _ = e
    db.session.commit()

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', role='Admin')
        admin.set_password('supersecretadmin')
        db.session.add(admin)

    if not Specialization.query.filter_by(name='General Medicine').first():
        specialization = Specialization(name='General Medicine', description='Primary Care')
        db.session.add(specialization)
        db.session.commit()
    else:
        specialization = Specialization.query.filter_by(name='General Medicine').first()

    if not User.query.filter_by(username='dr_sample').first():
        doctor_user = User(username='dr_sample', role='Doctor')
        doctor_user.set_password('doctorpass')
        db.session.add(doctor_user)
        db.session.commit()

        doctor = Doctor(id=doctor_user.id, name='Alice Smith', specialization_id=specialization.id)
        db.session.add(doctor)
        db.session.commit()

    if not User.query.filter_by(username='patient_sample').first():
        patient_user = User(username='patient_sample', role='Patient')
        patient_user.set_password('patientpass')
        db.session.add(patient_user)
        db.session.commit()

        patient = Patient(id=patient_user.id, name='Kumar', age=35, height=175, weight=75, contact=None, address=None)
        db.session.add(patient)
        db.session.commit()

    # Sample data ensured (admin + doctor + patient + specialization).

