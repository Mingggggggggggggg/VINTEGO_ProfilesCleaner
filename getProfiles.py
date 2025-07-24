import os
import winreg

userPath = r"C:\Users"
registryPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
excludeUsersDir = ["All Users", "Default", "Gast", "Default User", "Public"]

sysProfiles = []
dirProfiles = []
log = []
log.append("--------------- Profile Log ---------------")

def getFolderSize(profilePath):
    totalSize = 0
    for dirpath, _, filenames in os.walk(profilePath):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    totalSize += os.path.getsize(fp)
            except:
                continue
    return totalSize / 1024**2  # MB

def getSysProfiles():
    print("Profile werden über Windows Registry abgerufen. Es kann einen Moment dauern.")
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
                        print("Kein Nutzer gefunden.")
                        continue
    except Exception as e:
        print(f"Fehler beim Registry-Zugriff: {e}")

    return sysProfiles

def getDirProfiles(userPath):
    print("Nutzer innerhalb des Ordnerverzeichnisses werden abgerufen. Dies kann einen Moment dauern.")
    dirProfiles = []
    try:
        for name in os.listdir(userPath):
            fullPath = os.path.join(userPath, name)
            if not os.path.isdir(fullPath):
                continue
            if name in excludeUsersDir:
                continue
            sizeMB = round(getFolderSize(fullPath), 2)
            dirProfiles.append([name, sizeMB, fullPath])
    except Exception as e:
        print(f"Fehler beim Auslesen des Ordnerberzeichnisses: {e}")
    return dirProfiles


def initGetProfiles():
    
    sysProfs = getSysProfiles()
    for sysProfile in sysProfs:
        print(f"{sysProfile[0]:20} | {sysProfile[1]:6.2f} MB | {sysProfile[2]}")
        log.append(f"{sysProfile[0]:20} | {sysProfile[1]:6.2f} MB | {sysProfile[2]}")
        

    dirProfs = getDirProfiles(userPath)
    for dirProfile in dirProfs:
        print(f"{dirProfile[0]:20} | {dirProfile[1]:6.2f} MB | {dirProfile[2]}")
        log.append(f"{dirProfile[0]:20} | {dirProfile[1]:6.2f} MB | {dirProfile[2]}")
        
    return sysProfs, dirProfs

if __name__ == "__main__":
    initGetProfiles()