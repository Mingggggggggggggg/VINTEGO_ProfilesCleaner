import os
import winreg
import wmi
import logger

userPath = r"C:\Users"
registryPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"

sysProfiles = []
log = []

def getFolderSize(profilePath):
    totalSize = 0
    for dirpath, _, filenames in os.walk(profilePath):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    totalSize += os.path.getsize(fp)
            except Exception as e:
                log.append(f"Fehler beim Berechnen der Ordnergröße: {e}")
                continue
    return totalSize / 1024**2  # MB

#TODO überprüfen
def getSysProfiles():
    log.append("Profile werden über Registry abgerufen.")
    sysProfiles.clear()
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registryPath) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                regContentName = winreg.EnumKey(key, i)
                with winreg.OpenKey(key, regContentName) as regContent:
                    try:
                        path, _ = winreg.QueryValueEx(regContent, "ProfileImagePath")
                        username = os.path.basename(path)
                        if not os.path.exists(path):
                            continue
                        sizeMB = round(getFolderSize(path), 2)
                        sysProfiles.append([username, sizeMB, path])
                    except FileNotFoundError:
                        log.append("ProfileImagePath nicht gefunden.")
                        continue
    except Exception as e:
        log.append(f"Fehler beim Registry zugriff: {e}")
        print(f"Fehler beim Registry-Zugriff: {e}")

    return sysProfiles

#TODO überprüfen
def getDirProfiles(userPath):
    log.append("Profile werden über Ordnerverzeichnis abgerufen.")
    dirProfiles = []
    try:
        for name in os.listdir(userPath):
            fullPath = os.path.join(userPath, name)
            if not os.path.isdir(fullPath):
                continue
            sizeMB = round(getFolderSize(fullPath), 2)
            dirProfiles.append([name, sizeMB, fullPath])
    except Exception as e:
        log.append(f"Fehler beim Auslesen des Ordnerverzeichnisses: {e}")
        print(f"Fehler beim Auslesen des Ordnerverzeichnisses: {e}")
    return dirProfiles

#TODO überprüfen
def getActiveUsers():
    activeUsers = []
    try:
        c = wmi.WMI()
        for session in c.Win32_LoggedOnUser():
            user_obj = session.Antecedent
            username = user_obj.Name
            domain = user_obj.Domain
            if username:
                activeUsers.append(username.lower())
                activeUsers.append(f"{domain}\\{username}".lower())
    except Exception as e:
        log.append(f"Fehler beim Abrufen angemeldeter Benutzer: {e}")
        print(f"Fehler beim Abrufen angemeldeter Benutzer: {e}")
    return list(set(activeUsers))

#TODO überprüfen
def initGetProfiles():
    sysProfs = getSysProfiles()
    activeUsers = getActiveUsers()

    print("Systemprofile:")
    for sysProfile in sysProfs:
        print(f"{sysProfile[0]:20} | {sysProfile[1]:6.2f} MB | {sysProfile[2]}")
        log.append(f"{sysProfile[0]:20} | {sysProfile[1]:6.2f} MB | {sysProfile[2]}")

    print("\nAktive Benutzer:")
    for user in activeUsers:
        print(f" - {user}")
        log.append(user)


    return sysProfs, activeUsers