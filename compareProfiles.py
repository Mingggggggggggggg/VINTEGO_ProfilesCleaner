

def compare(sysProfiles, dirProfiles):
    sysUsers = {(entry[0], entry[2]) for entry in sysProfiles}
    dirUsers = {(entry[0], entry[2]) for entry in dirProfiles}

    sysUsersOverflow = sysUsers - dirUsers # sysUsers \ dirUsers
    dirUsersOverflow = dirUsers - sysUsers # dirUsers \ sysUsers
    
    if not sysUsersOverflow:
        print("Überschüssige Registryeinträge")
        for user in sorted(sysUsersOverflow):
            print(f"  - {user}")


    if not dirUsersOverflow:
        print("Überschüssige Ordnereinträge")
        for user in sorted(dirUsersOverflow):
            print(f"  - {user}")

    #TODO DAS HIER AUCH AAAAAAAAAAAAAAAAAAAAA
    return sysUsersOverflow, dirUsersOverflow
