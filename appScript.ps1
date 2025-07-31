$appPath = "C:\VINTEGO-Technik\Tools"
$appUrl = "https://github.com/Mingggggggggggggg/VINTEGO_ProfilesCleaner/releases/download/v0.3/profileCleaner.exe"
$exeFile = Join-Path -Path $appPath -ChildPath "profileCleaner.exe"
$logPath = "C:\VINTEGO-Technik\Logs\profileCleanerLog.txt"

function runExec {
    $argList = @()

    if ($env:minsizemb) {
        $argList += $env:minsizemb
    } else {
        Write-Output "Fehler: Keine Mindestgröße angegeben."
        exit 1
    }

    if ($env:deleteProfiles) {
        $argList += "--delProfile"
    }
    Write-Output "Starte profileCleaner mit Argumenten: $argList"
    Start-Process -FilePath $exeFile -ArgumentList $argList -NoNewWindow -Wait
}

function readLogs {
    if (Test-Path $logPath) {
        return Get-Content $logPath -Raw
    } else {
        return "Kein Log gefunden."
    }
}

function getApp {
    if (-not (Test-Path $exeFile)) {
        if (-not (Test-Path $appPath)) {
            New-Item -Path $appPath -ItemType Directory | Out-Null
        }

        Write-Output "Lade Anwendung von $appUrl herunter..."
        Invoke-WebRequest -Uri $appUrl -OutFile $exeFile

        if (-not (Test-Path $exeFile)) {
            Write-Output "Fehler: Anwendung konnte nicht heruntergeladen werden."
            exit 1
        }

        Write-Output "Anwendung erfolgreich heruntergeladen."
    } else {
        Write-Output "Anwendung bereits vorhanden."
    }

    runExec
}

getApp
#Warte 5 Sekunden, weil keine Ahnung, ob die Logs gelesen werden, wenn die Anwendung noch läuft. aaaaaaaaaaaaaaaaaaaaaa
Start-Sleep 5

$logs = readLogs
ninja-property-set profileCleanerLog "$logs"
Write-Output "Skript beendet."
