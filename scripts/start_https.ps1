<#
Helper script to generate local mkcert TLS certs for the app's LAN hostname and start the Flask app with SSL.

Usage (PowerShell, run as Administrator if required):
  # Ensure mkcert is installed first (see https://github.com/FiloSottile/mkcert)
  .\start_https.ps1 -HostNames @('docuvoice.com','docuvoice.local','localhost','192.168.0.10') -Port 5000

This script will:
 - check for mkcert
 - run mkcert -install and generate a cert for the provided hostnames
 - set DOCUVOICE_CERT and DOCUVOICE_KEY env vars for the child process and start the app

Notes:
 - You must install mkcert beforehand. On Windows, use choco or download the binary.
 - For mobile devices you may need to trust the mkcert root CA on that device.
#>

param(
    [string[]] $HostNames = @('docuvoice.local','localhost'),
    [int] $Port = 5000,
    [string] $AppPath = "$PSScriptRoot\..\word_to_audio\app.py"
)

function Write-Info($m){ Write-Host "[info] $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "[warn] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[error] $m" -ForegroundColor Red }

Write-Info "Starting mkcert + HTTPS helper"

$mkcert = Get-Command mkcert -ErrorAction SilentlyContinue
if (-not $mkcert) {
    Write-Warn "mkcert not found in PATH. Please install mkcert first: https://github.com/FiloSottile/mkcert#installation"
    exit 1
}

Write-Info "Ensuring mkcert root CA is installed (may prompt for elevation)"
mkcert -install

$namesArg = $HostNames -join ' '
Write-Info "Generating certificate for: $namesArg"
$out = mkcert $namesArg 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Err "mkcert failed: $out"
    exit 1
}

# mkcert outputs files named like <name>+N.pem and <name>+N-key.pem in the current folder
# find the first pem pair in current folder
$pemFiles = Get-ChildItem -Path . -Filter '*.pem' | Sort-Object LastWriteTime -Descending
if ($pemFiles.Count -lt 2) {
    Write-Err "Could not find generated PEM files in the current folder. mkcert output: $out"
    exit 1
}

# pick the two most recent pem files (cert and key)
$certFile = $pemFiles[0].FullName
$keyFile = $pemFiles[1].FullName
Write-Info "Using cert: $certFile"
Write-Info "Using key:  $keyFile"

Write-Info "Launching the Flask app with SSL environment variables set for the child process"

$env:DOCUVOICE_CERT = $certFile
$env:DOCUVOICE_KEY = $keyFile
$env:DOCUVOICE_HOST = '0.0.0.0'
$env:DOCUVOICE_PORT = [string]$Port

Write-Info "Starting: python $AppPath (press Ctrl+C to stop)"
python $AppPath
