import os
import winreg
import logger

userPath = r"C:\Users"
registryPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
excludeUsersDir = {"all users", "default", "gast", "default user", "public", "administrator", "standardprofil", "platzhalter"}
excludeSID = ("S-1-5-18", "S-1-5-19", "S-1-5-20")

sysProfiles = []
dirProfiles = []
log = []

def getSysProfiles():
    """
    Gibt Profile in der Registry als Liste zurück. Inklusive Name, Pfad, SID und Größe.

    Returns List

        [NAME, PFAD, SID, GRÖßE]
    """
    log.append("Profile werden über Registry abgerufen. Es kann einen Moment dauern.")
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                sid = winreg.EnumKey(key, i)

                if sid in excludeSID:
                    continue

                try:
                    with winreg.OpenKey(key, sid) as regContent:
                        path, _ = winreg.QueryValueEx(regContent, "ProfileImagePath")

                        if not os.path.exists(path):
                            log.append(f"Registry-Leiche erkannt – Ordner fehlt: {sid} - {path}")
                            sysProfiles.append([os.path.basename(path), path, sid, 0.0]) 
                            continue

                        username = os.path.basename(path)
                        sysProfiles.append([username, path, sid])
                except FileNotFoundError:
                    log.append("ProfileImagePath nicht gefunden.")
                    continue
    except Exception as e:
        log.append(f"Fehler beim Registry zugriff: {e}")
        print(f"Fehler beim Registry-Zugriff: {e}")

    return sysProfiles

def getDirProfiles():
    print("Profile werden über Ordnerverzeichnis abgerufen. Es kann einen Moment dauern.")    
    log.append("Profile werden über Ordnerverzeichnis abgerufen.")
    try:
        for name in os.listdir(userPath):
            if name.lower() in excludeUsersDir:
                continue

            fullPath = os.path.join(userPath, name)
            if not os.path.isdir(fullPath):
                continue

            dirProfiles.append([name, fullPath])
    except Exception as e:
        log.append(f"Fehler beim Auslesen des Ordnerverzeichnisses: {e}")
        print(f"Fehler beim Auslesen des Ordnerverzeichnisses: {e}")
    return dirProfiles


def initGetProfiles():
    dirProfiles = getDirProfiles()
    sysProfiles = getSysProfiles()
    logger.logMessages("Profilabruf", log)
    return dirProfiles, sysProfiles