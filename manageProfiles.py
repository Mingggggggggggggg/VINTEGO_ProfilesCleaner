import os
import shutil
import logger
import winreg
import subprocess

log = []

registryPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"


def deleteRegistryProfile(candidates):
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath, 0, winreg.KEY_ALL_ACCESS) as reg:
            for c in candidates:
                sid = c[2]
                if sid in ("REG_ONLY",) or (sid not in ("DIR_ONLY", "REG_ONLY")):
                    try:
                        winreg.DeleteKey(reg, sid)
                        log.append(f"Registry-Eintrag für SID {sid} (Profil {c[0]}) gelöscht.")
                    except FileNotFoundError:
                        log.append(f"Registry-Eintrag für SID {sid} (Profil {c[0]}) nicht gefunden.")
                    except OSError as e:
                        log.append(f"Fehler beim Löschen des Registry-Eintrags {sid} (Profil {c[0]}): {e}")
    except Exception as e:
        log.append(f"Fehler beim Registry-Zugriff: {e}")


def deleteADUser(candidates):
    for c in candidates:
        sid = c[2]
        if sid != "DIR_ONLY":
            cmd = f"""
            try {{
                $user = Get-ADUser -Filter {{SID -eq '{sid}'}}
                if ($null -ne $user) {{
                    Remove-ADUser -Identity $user -Confirm:$false -ErrorAction Stop
                    Write-Output 'User gelöscht'
                }} else {{
                    Write-Output 'User nicht gefunden'
                }}
            }} catch {{
                Write-Output 'Fehler beim Löschen: ' + $_.Exception.Message
                exit 1
            }}
            """
            try:
                result = subprocess.run(
                    ["powershell", "-Command", cmd],
                    capture_output=True, text=True, check=True
                )
                stdout = result.stdout.strip()
                if "User gelöscht" in stdout:
                    log.append(f"AD-Benutzer {sid} aus Kandidat {c} gelöscht.")
                elif "User nicht gefunden" in stdout:
                    log.append(f"AD-Benutzer {sid} nicht gefunden, evtl. schon gelöscht.")
                else:
                    log.append(f"Unbekannte Ausgabe beim Löschen von AD-Benutzer {sid}: {stdout}")
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
        else:
            log.append(f"Profilordner {path} zu {c} nicht gefunden, evtl. schon gelöscht.")


def initCleanup(candidates):
    for c in candidates:
        identifier = c[2]

        if identifier == "DIR_ONLY":
            log.append(f"Lösche nur Ordner für Kandidat: {c}")
            deleteDir([c])

        elif identifier == "REG_ONLY":
            log.append(f"Lösche nur Registry für Kandidat: {c}")
            deleteRegistryProfile([c])


    logger.logMessages("Bereinigung", log)
