<#
add-host.ps1
Usage: Right-click the file and choose "Run with PowerShell" (it will prompt for elevation),
or run from an elevated PowerShell:

    .\add-host.ps1 -ip '192.168.0.10' -hostName 'docuvoice.local.com'

This script creates a backup of the hosts file and appends a mapping. It uses ASCII encoding
when appending to avoid BOM issues.
#>

param(
    [string]$ip = '192.168.0.10',
    [string]$hostName = 'docuvoice.local.com'
)

$hosts = 'C:\Windows\System32\drivers\etc\hosts'
$backup = 'C:\Windows\System32\drivers\etc\hosts.bak'

function Is-Administrator {
    $current = [Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()
    return $current.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if (-not (Is-Administrator)) {
    Write-Host 'Not running elevated. Relaunching as administrator...' -ForegroundColor Yellow
    Start-Process -FilePath 'powershell.exe' -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -ip `"$ip`" -hostName `"$hostName`"" -Verb RunAs
    exit
}

try {
    Write-Host "Backing up hosts to $backup" -ForegroundColor Cyan
    Copy-Item -Path $hosts -Destination $backup -Force -ErrorAction Stop
} catch {
    Write-Error "Failed to backup hosts file: $_"
    exit 1
}

try {
    $line = "$ip $hostName"
    # make sure the line isn't already present
    $existing = Select-String -Path $hosts -Pattern "^\s*${ip}\s+${hostName}$" -SimpleMatch -Quiet
    if ($existing) {
        Write-Host "Entry already exists in hosts: $line" -ForegroundColor Green
    } else {
        Write-Host "Appending entry to hosts: $line" -ForegroundColor Cyan
        $line | Out-File -FilePath $hosts -Encoding ASCII -Append
        Write-Host 'Appended.' -ForegroundColor Green
    }
    ipconfig /flushdns | Out-Null
    Write-Host "Flushed DNS cache." -ForegroundColor Gray
    Write-Host "Done. Verify with: Get-Content $hosts | Select-String $hostName" -ForegroundColor Green
} catch {
    Write-Error "Failed to update hosts file: $_"
    # attempt to restore backup
    if (Test-Path $backup) {
        Write-Host 'Attempting to restore backup...' -ForegroundColor Yellow
        Copy-Item -Path $backup -Destination $hosts -Force
        Write-Host 'Backup restored.' -ForegroundColor Green
    }
    exit 1
}
