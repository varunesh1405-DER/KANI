<#
Start a local ngrok HTTPS tunnel to your Flask app on the given port and open the public URL in the browser.

Usage:
  .\start_ngrok.ps1 -Port 5000

Requirements:
 - ngrok must be installed and available on PATH. Download from https://ngrok.com/download
 - This script will start ngrok in the background and query the local ngrok API at http://127.0.0.1:4040

Notes:
 - Free ngrok gives a temporary public HTTPS URL (works for getUserMedia since it's HTTPS).
 - Keep the PowerShell session running to keep ngrok alive, or find the ngrok process and stop it when done.
#>

param(
    [int] $Port = 5000,
    [int] $ApiPollSeconds = 10
)

function Write-Info($m){ Write-Host "[info] $m" -ForegroundColor Cyan }
function Write-Warn($m){ Write-Host "[warn] $m" -ForegroundColor Yellow }
function Write-Err($m){ Write-Host "[error] $m" -ForegroundColor Red }

Write-Info "Starting ngrok helper for port $Port"

$ngrokCmd = Get-Command ngrok -ErrorAction SilentlyContinue
if (-not $ngrokCmd) {
    Write-Err "ngrok not found in PATH. Download and install it from https://ngrok.com/download then retry."
    exit 1
}

Write-Info "Launching ngrok (http $Port)"
# start ngrok in a new window (background)
$startInfo = Start-Process -FilePath $ngrokCmd.Source -ArgumentList "http", "$Port" -WindowStyle Hidden -PassThru

Write-Info "Waiting up to $ApiPollSeconds seconds for ngrok API to report the public URL..."

$apiUrl = 'http://127.0.0.1:4040/api/tunnels'
$publicUrl = $null
$tries = 0
while ($tries -lt $ApiPollSeconds -and -not $publicUrl) {
    Start-Sleep -Seconds 1
    try {
        $resp = Invoke-RestMethod -Uri $apiUrl -ErrorAction Stop
        if ($resp.tunnels -and $resp.tunnels.Count -gt 0) {
            # prefer https tunnel
            $t = $resp.tunnels | Where-Object { $_.public_url -match '^https://' } | Select-Object -First 1
            if (-not $t) { $t = $resp.tunnels[0] }
            $publicUrl = $t.public_url
            break
        }
    } catch {
        # API not ready yet
    }
    $tries++
}

if (-not $publicUrl) {
    Write-Warn "Could not get ngrok public URL within timeout. You can check the ngrok web UI at http://127.0.0.1:4040/"
    exit 1
}

Write-Info "ngrok public URL: $publicUrl"
Write-Info "Opening in the default browser..."
Start-Process $publicUrl

Write-Info "ngrok started (PID $($startInfo.Id)). To stop it, end the ngrok process or close this session." 
