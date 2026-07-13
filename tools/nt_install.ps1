param()

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$VenvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"

function Find-PythonInstaller {
  $py = Get-Command py -ErrorAction SilentlyContinue
  if ($py) { return @{ FilePath = $py.Source; Arguments = @("-3"); Label = "py -3" } }
  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) { return @{ FilePath = $python.Source; Arguments = @(); Label = "python" } }
  $localPythonCandidates = @()
  if ($env:LOCALAPPDATA) {
    $localPythonCandidates += Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
    $pythonRoot = Join-Path $env:LOCALAPPDATA "Programs\Python"
    if (Test-Path -LiteralPath $pythonRoot) {
      $localPythonCandidates += Get-ChildItem -LiteralPath $pythonRoot -Directory -Filter "Python3*" -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending |
        ForEach-Object { Join-Path $_.FullName "python.exe" }
    }
  }
  foreach ($candidate in ($localPythonCandidates | Select-Object -Unique)) {
    if ($candidate -and (Test-Path -LiteralPath $candidate)) { return @{ FilePath = $candidate; Arguments = @(); Label = $candidate } }
  }
  throw "Python 3 was not found. Install Python 3.11+ from python.org, then run this again."
}

function Invoke-Python($python, $arguments) {
  & $python.FilePath @($python.Arguments + $arguments)
  if ($LASTEXITCODE -ne 0) { throw "Python command failed: $($arguments -join ' ')" }
}

$python = Find-PythonInstaller
Write-Host "Using Python: $($python.Label)"
Write-Host "Creating local virtual environment in .venv ..."
Invoke-Python $python @("-m", "venv", (Join-Path $RepoRoot ".venv"))

Write-Host "Installing Python dependencies ..."
& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed." }
& $VenvPython -m pip install -r (Join-Path $RepoRoot "requirements.txt")
if ($LASTEXITCODE -ne 0) { throw "requirements install failed." }

Write-Host ""
Write-Host "Install complete. Start the app with Start NT Performance Hub.bat."