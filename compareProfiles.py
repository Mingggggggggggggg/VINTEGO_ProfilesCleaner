

def compare(sysProfiles, dirProfiles):
    sysUsers = {(entry[0], entry[2]) for entry in sysProfiles}
    dirUsers = {(entry[0], entry[2]) for entry in dirProfiles}

    sysUsersOverflow = sysUsers - dirUsers # sysUsers \ dirUsers
    dirUsersOverflow = dirUsers - sysUsers # dirUsers \ sysUsers

    
    if sysUsersOverflow:
        print("Überschüssige Registryeinträge")
        for user in sorted(sysUsersOverflow):
            print(f"{user}")


    if dirUsersOverflow:
        print("Überschüssige Ordnereinträge")
        for user in sorted(dirUsersOverflow):
            print(f"{user}")

    return sysUsersOverflow, dirUsersOverflow

def flagSize(minSize, sysProfiles, dirProfiles):
    sysSizeFlag = []
    dirSizeFlag = []
    
    for profile in sysProfiles:
        if profile[1] < minSize:
            sysSizeFlag.append(profile)
            print(f"SYS: {profile}")
            
    for profile in dirProfiles:
        if profile[1] < minSize:
            dirSizeFlag.append(profile)
            print(f"DIR: {profile}")

    return sysSizeFlag, dirSizeFlag


def toDelete(sysSizeFlag, dirSizeFlag, sysOverflow, dirOverflow):

    def clean_entry(name, path):
        return (name.lower(), path.strip())

    # Registry-Profile
    toDeleteSys = set()
    for name, _, path in sysSizeFlag:
        toDeleteSys.add(clean_entry(name, path))
    for name, path in sysOverflow:
        toDeleteSys.add(clean_entry(name, path))

    # Ordner-Profile
    toDeleteDir = set()
    for name, _, path in dirSizeFlag:
        toDeleteDir.add(clean_entry(name, path))
    for name, path in dirOverflow:
        toDeleteDir.add(clean_entry(name, path))

    return list(toDeleteSys), list(toDeleteDir)







def initCompare(minSize, sysProfiles, dirProfiles):
    sysUsersOverflow, dirUsersOverflow = compare(sysProfiles, dirProfiles)
    sysSizeFlag, dirSizeFlag = flagSize(minSize, sysProfiles, dirProfiles)
    
    toDeleteSys, toDeleteDir = toDelete(sysSizeFlag, dirSizeFlag, sysUsersOverflow, dirUsersOverflow)
    
    return toDeleteSys, toDeleteDir
