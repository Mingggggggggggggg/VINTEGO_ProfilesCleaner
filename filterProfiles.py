import getProfiles
import os

def filterProfiles(sysProfiles, activeADUsers):
    filteredActive = []
    activeSID = {user[0] for user in activeADUsers}

    for profile in sysProfiles:
        _, _, sid, _ = profile
        if sid not in activeSID:
            filteredActive.append(profile)
    return filteredActive


def toDelete(filteredActive, minSizeMB):
    candidates = []
    dirProfiles = getProfiles.getDirProfiles()
    regPaths = {p[1].lower() for p in filteredActive}

    for profile in filteredActive:
        if os.path.exists(profile[1]) and profile[3] < minSizeMB:
            candidates.append(profile)

    for dirProf in dirProfiles:
        path = dirProf[1].lower()
        size = dirProf[2]

        if path not in regPaths and size < minSizeMB and os.path.exists(path):
            candidates.append([dirProf[0], dirProf[1], "DIR_ONLY", size])

    return candidates


def initFilter(minSizeMB):
    sysProfiles, activeADUsers = getProfiles.initGetProfiles()
    filtered = filterProfiles(sysProfiles, activeADUsers)
    flagged = toDelete(filtered, minSizeMB)
    #print(flagged)
    return flagged
