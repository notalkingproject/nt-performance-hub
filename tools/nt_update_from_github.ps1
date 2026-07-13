param(
  [int]$Port = 8080,
  [switch]$NoRestartPrompt
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$ControlScript = Join-Path $PSScriptRoot "nt_server_control.ps1"
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
    & powershell -NoProfile -ExecutionPolicy Bypass -File $ControlScript restart -OpenBrowser -Port $Port
    if ($LASTEXITCODE -ne 0) { throw "Restart failed." }
  } else {
    Write-Host "Leaving the currently running server alone. Restart later to use the updated code."
  }
} elseif (-not $wasRunning) {
  $answer = Read-Host "Start NT Performance Hub now? [Y/n]"
  if ($answer.Trim().ToLowerInvariant() -notin @("n", "no")) {
    & powershell -NoProfile -ExecutionPolicy Bypass -File $ControlScript start -OpenBrowser -Port $Port
    if ($LASTEXITCODE -ne 0) { throw "Start failed." }
  }
}