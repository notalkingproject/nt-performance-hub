param(
  [int]$Port = 8080,
  [switch]$NoRestartPrompt
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$ActionScript = Join-Path $PSScriptRoot "nt_server_action.py"
$HealthUrl = "http://127.0.0.1:$Port/health"

function Test-Running {
  try {
    $health = Invoke-RestMethod -Uri $HealthUrl -TimeoutSec 2
    return [bool]$health.ok
  } catch {
    return $false
  }
}

function Invoke-Git($arguments) {
  & git -C $RepoRoot @arguments
  if ($LASTEXITCODE -ne 0) { throw "git $($arguments -join ' ') failed." }
}

function Find-Python {
  $venvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
  if (Test-Path -LiteralPath $venvPython) {
    return @{ FilePath = $venvPython; Arguments = @(); Label = $venvPython }
  }

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
    if ($candidate -and (Test-Path -LiteralPath $candidate)) {
      return @{ FilePath = $candidate; Arguments = @(); Label = $candidate }
    }
  }

  throw "Python 3 was not found. Run Install NT Performance Hub.bat first, or install Python 3.11+ and try again."
}

function Invoke-ServerAction($action) {
  if (-not (Test-Path -LiteralPath $ActionScript)) {
    throw "Server action script was not found: $ActionScript"
  }

  $python = Find-Python
  & $python.FilePath @($python.Arguments + @($ActionScript, $action, "--open", "--port", $Port))
  if ($LASTEXITCODE -ne 0) { throw "$action failed." }
}
Write-Host "NT Performance Hub - Update From GitHub"
Write-Host "Repo: $RepoRoot"
Write-Host ""

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw "Git was not found. Install Git for Windows, then run this again."
}

$dirty = & git -C $RepoRoot status --porcelain
if ($LASTEXITCODE -ne 0) { throw "git status failed." }
if ($dirty) {
  Write-Host "This performance PC has local code changes. Update stopped to avoid overwriting them." -ForegroundColor Yellow
  Write-Host ""
  $dirty | ForEach-Object { Write-Host $_ }
  Write-Host ""
  Write-Host "Commit, stash, or discard those local changes before updating. Local config files ignored by Git are fine."
  exit 2
}

$wasRunning = Test-Running
if ($wasRunning) { Write-Host "Server is currently running." } else { Write-Host "Server is not currently running." }
Write-Host ""

Write-Host "Fetching latest code..."
Invoke-Git -arguments @("fetch", "--prune")

Write-Host "Pulling latest code..."
Invoke-Git -arguments @("pull", "--ff-only")

Write-Host ""
Write-Host "Update complete."

if ($wasRunning -and -not $NoRestartPrompt) {
  $answer = Read-Host "Restart NT Performance Hub now? [Y/n]"
  if ($answer.Trim().ToLowerInvariant() -notin @("n", "no")) {
    Invoke-ServerAction "restart"
  } else {
    Write-Host "Leaving the currently running server alone. Restart later to use the updated code."
  }
} elseif (-not $wasRunning) {
  $answer = Read-Host "Start NT Performance Hub now? [Y/n]"
  if ($answer.Trim().ToLowerInvariant() -notin @("n", "no")) {
    Invoke-ServerAction "start"
  }
}
