# Hospital Management System (HMS)

A small Flask-based hospital management demo app. This README explains how to set up the project in PowerShell on Windows, create the database, and run the application using the bundled virtual environment.

## Prerequisites
- Python 3.10+ installed (the project uses a venv under `venv/`).
- PowerShell (built-in on Windows).

## Quick setup (PowerShell)
Open PowerShell in the project root (`C:\Users\Vithyasagar\HMS_Project_24f2001900`) and run the following commands.

1. Create a virtual environment (only if you don't have `venv/` already):

```powershell
python -m venv venv
```

2. Activate the virtual environment (PowerShell session):

```powershell
# If ExecutionPolicy blocks activation, run PowerShell as Administrator and:
# Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
.
.\venv\Scripts\Activate.ps1
```

You should now see `(venv)` in your prompt.

3. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Create the database and seed sample data:

```powershell
python create_db.py
```

This will create `instance/hms.db` (if missing) and seed an `admin` and `dr_sample` user plus a sample specialization.

5. Run the app:

```powershell
python run.py
```

Open http://127.0.0.1:5000 in your browser.

## Useful notes
- Default seeded users created by `create_db.py`:
  - Admin: username `admin`, password `supersecretadmin`
  - Doctor: username `dr_sample`, password `doctorpass`

- If you see `ModuleNotFoundError` for Flask-related packages, ensure you activated the venv and ran `pip install -r requirements.txt` in the same environment used to run `python run.py`.

- Database location: `instance/hms.db`. If you delete this file and re-run `create_db.py` it will recreate the tables and seed sample data again.

## Troubleshooting
- Static files 404: templates reference files in `app/static/`. Ensure `app/static/style.css` and `app/static/logo.svg` exist (they do in this repo). If the browser shows cached results, hard-refresh (Ctrl+F5).

- Permissions / ExecutionPolicy: If `Activate.ps1` is blocked by PowerShell execution policy, run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` as Administrator or use `venv\Scripts\activate.bat` in cmd.exe.

- Want to run without activating venv? Use the venv python executable explicitly:

```powershell
C:\path\to\project\venv\Scripts\python.exe run.py
```

(Replace `C:\path\to\project` with your project path.)

## Next steps (suggestions)
- Create a `start.ps1` to automate activation and running.
- Use `flask-migrate` to create and manage schema migrations instead of `create_db.py` for production-grade workflows.
- Replace CDN Bootstrap with locally served files if offline usage is required.

If you want, I can add `start.ps1` and/or create a `docs/` folder with more developer notes. Just tell me which to add next.
