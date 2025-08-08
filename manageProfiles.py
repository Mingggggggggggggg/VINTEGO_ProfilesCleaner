import os
import winreg
import logger
import subprocess

log = []
successLog = []

def deleteReg(candidates, sysProfiles):
    path_to_sid = {p[1].lower(): p[2] for p in sysProfiles if len(p) > 2}

    for c in candidates:
        path = c[1].lower()
        sid = path_to_sid.get(path)

        if not sid:
            print(f"Kein Registry-Eintrag für {path} gefunden.")
            log.append(f"Kein Registry-Eintrag für {path} gefunden.")
            continue

        regPath = f"HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\{sid}"
        try:
            subprocess.run(
                ["powershell", "-Command", f'Remove-Item -LiteralPath "{regPath}" -Recurse -Force'],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"Registryeintrag {regPath} gelöscht.")
            log.append(f"Registryeintrag {regPath} gelöscht.")
        except subprocess.CalledProcessError as e:
            print(f"Löschen des Registryeintrags fehlgeschlagen für {regPath}: {e.stderr.strip()}")
            log.append(f"Löschen des Registryeintrags fehlgeschlagen für {regPath}: {e.stderr.strip()}")



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


def checkSuccess(candidates, sysProfiles):
    pathSID = {p[1].lower(): p[2] for p in sysProfiles if len(p) > 2}

    for c in candidates:
        path = c[1].lower()
        sid = pathSID.get(path)


        if os.path.exists(path):
            successLog.append(f"Ordner {path} wurde nicht gelöscht.")
        else:
            successLog.append(f"Ordner {path} wurde erfolgreich gelöscht.")


        if sid:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, fr"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\{sid}") as key:
                    successLog.append(f"Registryeintrag für SID {sid} existiert noch.")
            except FileNotFoundError:
                successLog.append(f"Registryeintrag für SID {sid} wurde erfolgreich gelöscht.")
        else:
            successLog.append(f"Kein Registryeintrag für Pfad {path} vorhanden (kein SID).")

    return successLog



def initCleanup(candidates, sysProfiles):
    log.append(f"Löschevorgang wird gestartet.")

    deleteReg(candidates, sysProfiles)
    deleteDir(candidates)

    logger.logMessages("Bereinigung", log)