Hospital Management System (HMS) - README

Python: 3.10+ (recommended)

Quick run steps (Windows PowerShell):

1) Create & activate venv in powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

2) Install dependencies in powershell
pip install --upgrade pip
pip install -r requirements.txt

3) Create DB (optional) in powershell
python create_db.py

4) Run (in powershell)
python run.py

Access: http://127.0.0.1:5000

Seeded test accounts (created by `create_db.py`):
- Admin: admin / supersecretadmin
- Doctor: dr_sample / doctorpass
- Patient: patient_sample / patientpass (name: Kumar, age: 35, height: 175cm, weight: 75kg)

Note:
    The project ZIP does not include the virtual environment. Recreate `venv` as given above.


