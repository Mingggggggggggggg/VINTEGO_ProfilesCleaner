import subprocess
import os

# Get-WmiObject Win32_LoggedOnUser | Select Antecedent -Unique # Alle aktiven Nutzer nach Name=
# oder Get-WMIObject -class Win32_ComputerSystem | select username
# Get-LocalUser | Select *
# Get-LocalUser | Select-Object -ExpandProperty Name
# net user
# HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList


userPath = r"C:\\Users"
#TODO Exclude Rules implementieren
excludeUsersSys = ["DefaultAccount", "Gast", "Administrator", "WDAGUtilityAccount"]
excludeUsersDir = ["All Users", "Default", "Gast", "Default User", "Praktikant WHV", "Public"]

def getSysProfiles():
    try:
        cmd = ["powershell", "-Command", "Get-LocalUser | Select-Object -ExpandProperty Name"]
        output = subprocess.check_output(cmd, text=True, encoding="mbcs", stderr=subprocess.DEVNULL)
        #print(output)
        users = []
        for line in output.splitlines():
            name = line.strip()
            if name:
                users.append(name)

        print(users)
        return users
    except Exception as e:
        print(f"Fehler beim Auslesen der Nutzer mit PowerShell: {e}")


def getDirProfiles(userPath):
    userDir = []

    for name in os.listdir(userPath):
        full_path = os.path.join(userPath, name)
        if os.path.isdir(full_path):
            size_bytes = 0
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    try:
                        filepath = os.path.join(root, file)
                        size_bytes += os.path.getsize(filepath)
                    except:
                        pass 

            size_mb = round(size_bytes / (1024 * 1024), 2)
            userDir.append([name, size_mb])

    print(userDir)
    return userDir



def initGetProfiles():
    pass

if __name__ == "__main__":
    getSysProfiles()
    getDirProfiles(userPath)