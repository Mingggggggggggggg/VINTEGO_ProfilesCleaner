import os
import logger
import subprocess

log = []
successLog = []

def deleteDir(candidates):
    for c in candidates:
        path = c[1]
        try:
            subprocess.run(
                ["powershell", "-Command", f'Remove-Item -LiteralPath "{path}" -Recurse -Force'],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"Profilordner {path} gelöscht.")
            log.append(f"Profilordner {path} gelöscht.")
        except subprocess.CalledProcessError as e:
            print(f"Löschvorgang fehlgeschlagen für {path}: {e.stderr.strip()}")
            log.append(f"Löschvorgang fehlgeschlagen für {path}: {e.stderr.strip()}")

def checkSuccess(candidates):
    for c in candidates:
        path = c[1]
        if os.path.exists(path):
            successLog.append(f"Ordner {path} wurde nicht gelöscht.")
        else:
            successLog.append(f"Ordner {path} wurde erfolgreich gelöscht.")
    return successLog



def initCleanup(candidates):
    log.append(f"Löschevorgang wird gestartet.")
    deleteDir(candidates)

    logger.logMessages("Bereinigung", log)