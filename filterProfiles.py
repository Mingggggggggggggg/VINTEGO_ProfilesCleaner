import getProfiles
import os

import logger
log = []
candidateLog = []

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
        print(f"Profile ohne _local: {[name, path]}")
        log.append(f"Profile ohne _local: {[name, path]}")
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
    candidateLog.append("Ermittle Löschkandidaten.")
    candidate = []

    for profile in filtered:
        tempName = profile[0]
        tempPath = profile[1]
        sizeMB = getFolderSize(profile[1])
        if sizeMB < minSize:
            candidate.append([tempName, tempPath, sizeMB])
            print(f"Löschkandidat gefunden: {tempName:<10} {tempPath:^10} {sizeMB:>10} MB")
            candidateLog.append(f"Löschkandidat gefunden: {tempName:<10} {tempPath:^10} {sizeMB:>10} MB")

    return candidate


def initFilter(minSizeMB):
    dirProfile = getProfiles.initGetProfiles()
    filtered = filterProfiles(dirProfile)
    candidate = toDelete(filtered, minSizeMB)

    logger.logMessages("FilterLog", log)
    logger.logMessages("LöschkandidatenLog", candidateLog)
    return candidate
