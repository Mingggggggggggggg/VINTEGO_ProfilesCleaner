import getProfiles
import os

import logger
log = []

def filterProfiles(dirProfiles):
    filtered = []
    skipNames = set()

    for name, _ in dirProfiles:
        if name.startswith("local_"):
            baseName = name[len("local_"):]
            skipNames.add(baseName)
            skipNames.add(name)

    for name, path in dirProfiles:
        if name in skipNames:
            continue
        print(f"Gefilterte Nutzer: {[name, path]}")
        filtered.append([name, path])

    return filtered

def getFolderSize(profilePath):
    totalSize = 0
    for dirpath, _, filenames in os.walk(profilePath):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    totalSize += os.path.getsize(fp)
            except Exception as e:
                print(f"Fehler beim Berechnen der Ordnergröße: {e}")
                log.append(f"Fehler beim Berechnen der Ordnergröße: {e}")
                continue
    return totalSize / 1024**2  # MB


def toDelete(filtered, minSize):
    print("Löschkandidaten werden ermittelt. Ordnergrößen werden berechnet. Dies kann einen Moment dauern.")
    log.append("Ermittle Löschkandidaten.")
    candidate = []

    for profile in filtered:
        tempName = profile[0]
        tempPath = profile[1]
        sizeMB = getFolderSize(profile[1])
        if sizeMB < minSize:
            candidate.append([tempName, tempPath, sizeMB])
            print(f"Löschkandidat gefunden: {tempName}; {tempPath}; {sizeMB} MB")
            log.append(f"Löschkandidat gefunden: {tempName}; {tempPath}; {sizeMB} MB")

    return candidate


def initFilter(minSizeMB):
    dirProfile = getProfiles.initGetProfiles()
    filtered = filterProfiles(dirProfile)
    candidate = toDelete(filtered, minSizeMB)

    logger.logMessages("FilterLog", log)
    return candidate
