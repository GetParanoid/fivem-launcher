$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootDir = Split-Path -Parent $scriptDir
Write-Host "Switching to project root: $rootDir"
Push-Location $rootDir

#? Activate venv
$venvActivate = Join-Path $rootDir ".venv/Scripts/Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..."
    & $venvActivate
} else {
    Write-Host "Virtual environment not found. Exiting."
    Pop-Location
    exit 1
}

#? Install packages
Write-Host "Installing required packages..."
pip install pyinstaller

#? Build exe
Write-Host "Building the executable with PyInstaller and custom icon..."
$iconPath = Join-Path $rootDir "assets/icon.ico"
pyinstaller --onefile --windowed --icon "$iconPath" fivem_launcher.py

Write-Host "Build complete. Check the 'dist' folder for the .exe file."
Pop-Location
