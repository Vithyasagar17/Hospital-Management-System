param(
    [switch]$Install,
    [switch]$CreateDB,
    [switch]$Run
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$venvPath = Join-Path $scriptDir 'venv'
$activate = Join-Path $venvPath 'Scripts\Activate.ps1'

if (Test-Path $activate) {
    . $activate
} else {
    python -m venv venv
    . $activate
}

if ($Install) {
    pip install --upgrade pip
    pip install -r requirements.txt
}

if (-not ($CreateDB -or $Run)) {
    $CreateDB = $true
    $Run = $true
}

if ($CreateDB) {
    python create_db.py
}

if ($Run) {
    python run.py
}
