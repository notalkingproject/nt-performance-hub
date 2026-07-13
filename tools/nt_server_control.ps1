param(
  [ValidateSet("start", "stop", "restart", "status")]
  [string]$Action = "status",
  [string]$HostName = "0.0.0.0",
  [int]$Port = 8080,
  [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..")).Path
$AppPath = Join-Path $RepoRoot "app.py"
$LogsDir = Join-Path $RepoRoot "logs"
$DataDir = Join-Path $RepoRoot "data"
$PidPath = Join-Path $DataDir "server.pid"
$OutLog = Join-Path $LogsDir "server.out.log"
$ErrLog = Join-Path $LogsDir "server.err.log"
$LocalUrl = "http://127.0.0.1:$Port/"
$HealthUrl = "http://127.0.0.1:$Port/health"
$PreflightApiUrl = "http://127.0.0.1:$Port/api/preflight"
$IdentityUrl = "http://127.0.0.1:$Port/api/identity"

function Ensure-Folders {
  New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
  New-Item -ItemType Directory -Path $DataDir -Force | Out-Null
}

function Find-PythonCommand {
  $venvPython = Join-Path $RepoRoot ".venv\Scripts\python.exe"
  if (Test-Path -LiteralPath $venvPython) {
    return @{ FilePath = $venvPython; PrefixArguments = @(); Label = "venv" }
  }
  $py = Get-Command py -ErrorAction SilentlyContinue
  if ($py) {
    return @{ FilePath = $py.Source; PrefixArguments = @("-3"); Label = "py -3" }
  }
  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) {
    return @{ FilePath = $python.Source; PrefixArguments = @(); Label = "python" }
  }
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
      return @{ FilePath = $candidate; PrefixArguments = @(); Label = $candidate }
    }
  }
  throw "Python 3 was not found. Run Install NT Performance Hub.bat first, or install Python 3.11+."
}

function Get-PidFileProcess {
  if (-not (Test-Path -LiteralPath $PidPath)) { return $null }
  try {
    $pidText = (Get-Content -LiteralPath $PidPath -Raw -ErrorAction Stop).Trim()
    if (-not $pidText) { return $null }
    $pidValue = [int]$pidText
    return Get-Process -Id $pidValue -ErrorAction SilentlyContinue
  } catch {
    return $null
  }
}

function Get-AppProcessIds {
  $ids = @()
  $pidFileProcess = Get-PidFileProcess
  if ($pidFileProcess) { $ids += $pidFileProcess.Id }
  $ids | Where-Object { $_ } | Select-Object -Unique
}

function Get-PortListenerPids {
  $lines = netstat -ano -p tcp 2>$null
  foreach ($line in $lines) {
    if ($line -match "^\s*TCP\s+\S+[:.]$Port\s+\S+\s+LISTENING\s+(\d+)\s*$") {
      [int]$matches[1]
    }
  }
}

function Test-Health {
  try {
    $health = Invoke-RestMethod -Uri $HealthUrl -TimeoutSec 2
    return [bool]$health.ok
  } catch {
    return $false
  }
}

function Test-AppIdentity {
  try {
    $identity = Invoke-RestMethod -Uri $IdentityUrl -TimeoutSec 1
    return $identity.app.name -eq "NT Performance Hub"
  } catch {
    return $false
  }
}
function Open-LocalBrowser {
  try {
    Start-Process $LocalUrl | Out-Null
  } catch {
    Write-Host "Open this URL in your browser: $LocalUrl"
  }
}

function Get-LanUrls {
  $urls = @()
  try {
    $interfaces = [System.Net.NetworkInformation.NetworkInterface]::GetAllNetworkInterfaces() |
      Where-Object { $_.OperationalStatus -eq [System.Net.NetworkInformation.OperationalStatus]::Up }
    foreach ($interface in $interfaces) {
      foreach ($address in $interface.GetIPProperties().UnicastAddresses) {
        $ip = $address.Address.ToString()
        if ($address.Address.AddressFamily -eq [System.Net.Sockets.AddressFamily]::InterNetwork -and $ip -notlike "127.*" -and $ip -notlike "169.254.*") {
          $urls += "http://${ip}:$Port/"
        }
      }
    }
  } catch {
    try {
      $hostEntry = [System.Net.Dns]::GetHostEntry([System.Net.Dns]::GetHostName())
      foreach ($address in $hostEntry.AddressList) {
        $ip = $address.ToString()
        if ($address.AddressFamily -eq [System.Net.Sockets.AddressFamily]::InterNetwork -and $ip -notlike "127.*" -and $ip -notlike "169.254.*") {
          $urls += "http://${ip}:$Port/"
        }
      }
    } catch {}
  }
  $urls | Select-Object -Unique
}

function Show-Status {
  $knownPids = @(Get-AppProcessIds)
  $listeners = @(Get-PortListenerPids | Select-Object -Unique)
  $healthy = Test-Health
  Write-Host "NT Performance Hub status"
  Write-Host "Local:  $LocalUrl"
  Write-Host "Preflight: http://127.0.0.1:$Port/preflight"
  foreach ($url in Get-LanUrls) { Write-Host "Remote: $url" }
  Write-Host "Health: $(if ($healthy) { 'ok' } else { 'not responding' })"
  if ($knownPids.Count) {
    Write-Host "App process PID(s): $($knownPids -join ', ')"
  } else {
    Write-Host "App process PID(s): none"
  }
  if ($listeners.Count) {
    Write-Host "Port $Port listener PID(s): $($listeners -join ', ')"
  } else {
    Write-Host "Port $Port listener PID(s): none"
  }
}

function Start-App {
  Ensure-Folders
  if (Test-AppIdentity -or ((Test-Health) -and @(Get-AppProcessIds).Count)) {
    Write-Host "NT Performance Hub is already running."
    Show-Status
    if ($OpenBrowser) { Open-LocalBrowser }
    return
  }

  $listeners = @(Get-PortListenerPids | Select-Object -Unique)
  if ($listeners.Count) {
    $appPids = @(Get-AppProcessIds)
    $other = @($listeners | Where-Object { $appPids -notcontains $_ })
    if ($other.Count) {
      throw "Port $Port is already in use by PID(s): $($other -join ', '). Stop that app or choose another port."
    }
  }

  $python = Find-PythonCommand
  Write-Host "Starting NT Performance Hub with $($python.Label)..."
  Write-Host "Logs: $OutLog"

  $launcherPath = Join-Path $PSScriptRoot "nt_launch_server.py"
  $launcherArgs = @(
    $launcherPath,
    "--app", $AppPath,
    "--cwd", $RepoRoot,
    "--host", $HostName,
    "--port", [string]$Port,
    "--stdout", $OutLog,
    "--stderr", $ErrLog,
    "--pid", $PidPath
  )

  Push-Location $RepoRoot
  try {
    & $python.FilePath @($python.PrefixArguments + $launcherArgs) | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Server launcher failed with code $LASTEXITCODE." }
  } finally {
    Pop-Location
  }

  $ready = $false
  for ($i = 0; $i -lt 20; $i++) {
    Start-Sleep -Milliseconds 500
    if (Test-Health) { $ready = $true; break }
  }

  if (-not $ready) {
    Write-Host "Server did not become healthy yet. Check logs:"
    Write-Host "  $OutLog"
    Write-Host "  $ErrLog"
    throw "Server process started but /health did not respond within 10 seconds."
  }

  Show-Status
  if ($OpenBrowser) { Open-LocalBrowser }
}

function Stop-App {
  $processIds = @(Get-AppProcessIds)
  if (-not $processIds.Count) {
    if (Test-Path -LiteralPath $PidPath) { Remove-Item -LiteralPath $PidPath -Force }
    Write-Host "NT Performance Hub is not running."
    return
  }
  foreach ($processId in $processIds) {
    Write-Host "Stopping NT Performance Hub PID $processId..."
    Stop-Process -Id $processId -Force
  }
  if (Test-Path -LiteralPath $PidPath) { Remove-Item -LiteralPath $PidPath -Force }
  Start-Sleep -Milliseconds 500
  Write-Host "Stopped."
}

switch ($Action) {
  "start" { Start-App }
  "stop" { Stop-App }
  "restart" { Stop-App; Start-App }
  "status" { Show-Status }
}
