$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$rootDir = Split-Path -Parent $scriptDir
$venvPath = Join-Path $rootDir ".venv/Scripts/Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating virtual environment..."
    & $venvPath
} else {
    Write-Host "Virtual environment activation script not found: $venvPath"
}
