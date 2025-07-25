import os
import getProfiles
import filterProfiles
import shutil
import logger
import winreg

#TODO Recherche und überarbeiten
def deleteRegistryProfile(username):
    try:
        regPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regPath, 0, winreg.KEY_ALL_ACCESS) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, subkey_name) as subkey:
                    path, _ = winreg.QueryValueEx(subkey, "ProfileImagePath")
                    if username.lower() == os.path.basename(path).lower():
                        winreg.DeleteKey(key, subkey_name)
                        logger.logMessages("Löschung", [f"Registry-Profil von {username} gelöscht"])
                        print(f"Registry-Profil von {username} gelöscht.")
                        return True
    except Exception as e:
        logger.logMessages("Fehler", [f"Fehler beim Löschen des Registry-Profils {username}: {e}"])
        print(f"Fehler beim Löschen des Registry-Profils {username}: {e}")
    return False

#TODO überprüfen
def cleanSysProfiles(minSizeMB=50):
    sysProfs, activeUsers = getProfiles.initGetProfiles()
    candidates = filterProfiles.initFilter(sysProfs, activeUsers, minSizeMB)
    
    if not candidates:
        print("Keine Profile zum Löschen gefunden.")
        return

    for prof in candidates:
        username, size, path = prof
        print(f"Lösche Registry-Profil: {username} ({size} MB)")
        logger.logMessages("Löschung", [f"Lösche Registry-Profil: {username} ({size} MB)"])
        deleteRegistryProfile(username)

#TODO überprüfen
def cleanDirProfiles(minSizeMB=50):
    dirProfs = getProfiles.getDirProfiles(getProfiles.userPath)
    sysProfs, activeUsers = getProfiles.initGetProfiles()
    sysUsernames = set(p[0].lower() for p in sysProfs)
    
    orphanDirs = [p for p in dirProfs if p[0].lower() not in sysUsernames]
    
    toDelete = [p for p in orphanDirs if p[1] < minSizeMB]
    
    if not toDelete:
        print("Keine verwaisten Ordner zum Löschen gefunden.")
        return

    for prof in toDelete:
        username, size, path = prof
        print(f"Lösche verwaisten Benutzerordner: {username} ({size} MB)")
        logger.logMessages("Löschung", [f"Lösche verwaisten Benutzerordner: {username} ({size} MB)"])
        try:
            shutil.rmtree(path)
        except Exception as e:
            logger.logMessages("Fehler", [f"Fehler beim Löschen von {path}: {e}"])
            print(f"Fehler beim Löschen von {path}: {e}")

#TODO überprüfen
def initCleanup(minSizeMB=50):
    cleanSysProfiles(minSizeMB)
    cleanDirProfiles(minSizeMB)
