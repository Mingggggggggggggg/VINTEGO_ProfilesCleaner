import os
import shutil
import logger
import winreg
import subprocess

log = []

registryPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
#Wenn DIR_ONLY an Index 2 gefunden wird, dann den Ordner im Ordnerverzeichnis löschen
#Wenn SID an Index 2, dann AD-User über powershell entfernen, Ordner im Verzeichnis löschen und ggf Registry!!!!! Wichtig ist nachgefragt
#TODO Recherche und überarbeiten
def deleteRegistryProfile(candidates):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath, 0, winreg.KEY_ALL_ACCESS) as reg:
            for c in candidates:
                sid = c[2]
                if sid != "DIR_ONLY":
                    try:
                        winreg.DeleteKey(reg, sid)
                        log.append(f"Registry-Eintrag zu {c} und {sid} gelöscht.")
                    except FileNotFoundError:
                        log.append(f"Registry-Eintrag zu {c} und {sid} nicht gefunden.")
    except Exception as e:
        log.append(f"Fehler beim Registry-Zugriff: {e}")


def deleteADUser(candidates):
    for c in candidates:
        sid = c[2]
        if sid != "DIR_ONLY":
            try:
                cmd = f'''
                $user = Get-ADUser -Filter {{SID -eq '{sid}'}} 
                if ($user) {{
                    Remove-ADUser -Identity $user -Confirm:$false
                }}
                '''
                subprocess.run(["powershell", "-Command", cmd], check=True)
                log.append(f"AD-Benutzer {sid} aus Kandidat {c} gelöscht.")
            except subprocess.CalledProcessError as e:
                log.append(f"Fehler beim Löschen von AD-Benutzer {sid} und Kandidat {c}: {e}")


def deleteDir(candidates):
    for c in candidates:
        path = c[1]
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                log.append(f"Profilordner {path} zu {c} gelöscht.")
            except Exception as e:
                log.append(f"Fehler beim Löschen des Ordners {path} - {c}: {e}")


def checkSuccess(candidates):

    results = []

    # Überprüfe Ordner
    for c in candidates:
        username, path, sid, size = c if len(c) == 4 else (*c, None)
        if os.path.exists(path):
            results.append(f"Profilordner {path} existiert noch. {c}")
        else:
            results.append(f"Profilordner {path} gelöscht. {c}")

    # Überprüfe Registrykandidaten
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath) as reg:
            existingSids = {winreg.EnumKey(reg, i) for i in range(winreg.QueryInfoKey(reg)[0])}
    except Exception as e:
        results.append(f"Fehler beim Zugriff auf Registry für Erfolgskontrolle: {e}")
        existingSids = set()

    for c in candidates:
        sid = c[2]
        if sid != "DIR_ONLY":
            if sid in existingSids:
                results.append(f"Registry-Eintrag {sid} noch vorhanden. {c}")
            else:
                results.append(f"Registry-Eintrag {sid} gelöscht. {c}")


    for c in candidates:
        sid = c[2]
        if sid != "DIR_ONLY":
            try:
                cmd = f"Get-ADUser -Filter {{SID -eq '{sid}'}}"
                output = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True)
                if output.returncode == 0 and output.stdout.strip():
                    results.append(f"AD-Benutzer {sid} noch vorhanden. {c}")
                else:
                    results.append(f"AD-Benutzer {sid} gelöscht. {c}")
            except Exception as e:
                results.append(f"Fehler bei AD-Benutzerprüfung {sid}: {e}")

    return results


def initCleanup(candidates):
    deleteADUser(candidates)
    deleteRegistryProfile(candidates)
    deleteDir(candidates)
    logger.logMessages("Bereinigung", log)
