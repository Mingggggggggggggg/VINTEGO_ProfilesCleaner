

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


def toDelete(sysProfiles, dirProfiles, sysSizeFlag, dirSizeFlag, sysOverflow, dirOverflow):
    toDeleteSys = []
    toDeleteDir = []

    for profile in sysSizeFlag:
        if profile in sysProfiles:
            toDeleteSys.append(profile)

    for name, path in sysOverflow:
        toDeleteSys.append([name, 0.0, path])  # Größe ist unbekannt oder egal

    for profile in dirSizeFlag:
        if profile in dirProfiles:
            toDeleteDir.append(profile)

    for name, path in dirOverflow:
        toDeleteDir.append([name, 0.0, path])

    return toDeleteSys, toDeleteDir





def initCompare(minSize, sysProfiles, dirProfiles):
    sysUsersOverflow, dirUsersOverflow = compare(sysProfiles, dirProfiles)
    sysSizeFlag, dirSizeFlag = flagSize(minSize, sysProfiles, dirProfiles)
    toDeleteSys, toDeleteDir = toDelete(sysProfiles, dirProfiles, sysSizeFlag, dirSizeFlag, sysUsersOverflow, dirUsersOverflow)
    print(f"TODELETESYS: {toDeleteSys} -- TODELETEDIR: {toDeleteDir}")
    return toDeleteSys, toDeleteDir
    #return sysUsersOverflow, dirUsersOverflow, sysSizeFlag, dirSizeFlag