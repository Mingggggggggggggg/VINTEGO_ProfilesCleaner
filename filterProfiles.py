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
        if not os.path.exists(profile[1]):
            candidates.append([profile[0], profile[1], "REG_ONLY", 0.0])
            log.append(f"Löschkandidat: Registry-Leiche ohne Ordner – {profile[0]}")
        elif profile[3] < minSizeMB:
            candidates.append(profile)
            log.append(f"Löschkandidat: Registry-Profil, Größe unter Minimum – {profile[0]} ({profile[3]} MB)")

    for dirProf in dirProfiles:
        path = dirProf[1].lower()
        size = dirProf[2]

        if path not in regPaths and size < minSizeMB and os.path.exists(path):
            candidates.append([dirProf[0], dirProf[1], "DIR_ONLY", size])
            log.append(f"Löschkandidat: Nur Ordnerprofil ohne Registry-Eintrag – {dirProf[0]} ({size} MB)")

    return candidates


def initFilter(minSizeMB):
    sysProfiles, activeADUsers = getProfiles.initGetProfiles()
    filtered = filterProfiles(sysProfiles, activeADUsers)
    flagged = toDelete(filtered, minSizeMB)
    logger.logMessages("FilterLog", log)
    return flagged
