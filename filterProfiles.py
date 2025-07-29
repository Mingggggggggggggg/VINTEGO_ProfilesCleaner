import getProfiles
import os

import logger
log = []

def filterProfiles(sysProfiles, activeADUsers):
    log.append("Starte Filteroperationen nach ADUser und in der Registry gelisteten Nutzern.")
    filteredActive = []
    activeSID = {user[0] for user in activeADUsers}

    for profile in sysProfiles:
        _, _, sid, _ = profile
        if sid not in activeSID:
            filteredActive.append(profile)
            log.append(f"Gefilterte Nutzer: {profile}")
    return filteredActive


def toDelete(filteredActive, minSizeMB):
    log.append("Starte Ermittlung der Löschkandidaten aus Filteroperation und verwaisten Nutzer im Ordnerverzeichnis")
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
            log.append(f"Löschkandidaten: {candidates}")
    return candidates


def initFilter(minSizeMB):
    sysProfiles, activeADUsers = getProfiles.initGetProfiles()
    filtered = filterProfiles(sysProfiles, activeADUsers)
    flagged = toDelete(filtered, minSizeMB)
    #print(flagged)
    logger.logMessages("FilterLog", log)
    return flagged
