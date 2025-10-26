<#
start.ps1 - simple helper to activate venv, install requirements (optional), create DB, and run the app
Usage:
  .\start.ps1            # activate venv, create DB, run app
  .\start.ps1 -Install   # also pip install -r requirements.txt
  .\start.ps1 -CreateDB  # only create DB
  .\start.ps1 -Run       # only run the app
#>

param(
    [switch]$Install,
    [switch]$CreateDB,
    [switch]$Run
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$venvPath = Join-Path $scriptDir 'venv'
$activate = Join-Path $venvPath 'Scripts\Activate.ps1'

function Write-Log($msg){ Write-Host "[start.ps1] $msg" }

if (Test-Path $activate) {
    Write-Log "Activating virtual environment at: $venvPath"
    # Use dot-sourcing to activate in this session
    . $activate
} else {
    Write-Log "Virtual environment not found at $venvPath. Creating one now..."
    python -m venv venv
    . $activate
}

if ($Install) {
    Write-Log "Installing dependencies from requirements.txt"
    pip install --upgrade pip
    pip install -r requirements.txt
}

if (-not ($CreateDB -or $Run)) {
    # default behaviour: create DB then run
    $CreateDB = $true
    $Run = $true
}

if ($CreateDB) {
    Write-Log "Creating or ensuring database..."
    python create_db.py
}

if ($Run) {
    Write-Log "Starting Flask app (run.py)"
    # Use python to run run.py so it uses the activated venv
    python run.py
}
