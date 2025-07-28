import os
import subprocess
import winreg
import wmi
import logger

userPath = r"C:\Users"
registryPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
excludeUsersDir = {"all users", "default", "gast", "default user", "public"}
excludeSID = ("S-1-5-18", "S-1-5-19", "S-1-5-20")

sysProfiles = []
activeUsers = []
dirProfiles = []
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

#excludeSID hier bereits angewandt
#[NAME, PFAD, SID, GRÖßE]
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
                            continue

                        username = os.path.basename(path)
                        sizeMB = round(getFolderSize(path), 2)
                        sysProfiles.append([username, path, sid, sizeMB])
                except FileNotFoundError:
                    log.append("ProfileImagePath nicht gefunden.")
                    continue
    except Exception as e:
        log.append(f"Fehler beim Registry zugriff: {e}")
        print(f"Fehler beim Registry-Zugriff: {e}")

    return sysProfiles

# [NAME, PFAD, GRÖßE]
def getDirProfiles():
    """
    Gibt Profile aus dem Ordnerverzeichnis als Liste zurück. Inklusive Name, Pfad und Größe.

    Returns
    ---------
    List
        [NAME, PFAD, GRÖßE]
    """
    log.append("Profile werden über Ordnerverzeichnis abgerufen. Es kann einen Moment dauern.")

    try:
        for name in os.listdir(userPath):
            if name.lower() in excludeUsersDir:
                continue

            fullPath = os.path.join(userPath, name)
            if not os.path.isdir(fullPath):
                continue

            sizeMB = round(getFolderSize(fullPath), 2)
            dirProfiles.append([name, fullPath, sizeMB])
    except Exception as e:
        log.append(f"Fehler beim Auslesen des Ordnerverzeichnisses: {e}")
        print(f"Fehler beim Auslesen des Ordnerverzeichnisses: {e}")
    return dirProfiles


def getActiveAdUsers():
    try:
        log.append("Rufe alle aktiven Nutzer ab. Es kann einen Moment dauern.")
        cmd = '''
        Get-ADUser -Filter "Enabled -eq 'True'" -Properties SID | 
        Select-Object SID, SamAccountName, UserPrincipalName | 
        Format-Table -HideTableHeaders -AutoSize
        '''
        output = subprocess.check_output(
            ["powershell", "-Command", cmd],
            text=True
        )

        lines = output.strip().splitlines()


        for line in lines:
            parts = line.split(None, 2)
            if len(parts) == 3:
                activeUsers.append([parts[0], parts[1], parts[2]])

        return activeUsers

    except subprocess.CalledProcessError as e:
        print(f"PowerShell-Fehler (Exitcode {e.returncode}): {e.output}")
        log.append(f"PowerShell-Fehler (Exitcode {e.returncode}): {e.output}")
        return []
    except Exception as e:
        print(f"Fehler: {e}")
        log.append(f"Fehler: {e}")
        return []


def initGetProfiles():
    sysProfs = getSysProfiles()
    activeADUsers = getActiveAdUsers()

    return sysProfs, activeADUsers
