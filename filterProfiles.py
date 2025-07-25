excludeUsersDir = {"all users", "default", "gast", "default user", "public"}

#TODO Nochmal überprüfen
def filterProfiles(sysProfiles, activeUsers):
    filtered = []
    activeUsersSet = set(user.lower() for user in activeUsers)
    for profile in sysProfiles:
        username = profile[0].lower()
        if username in activeUsersSet:
            continue
        if username in excludeUsersDir:
            continue
        filtered.append(profile)
    return filtered

def toDelete(filtered, minSizeMB):
    candidates = [p for p in filtered if p[1] < minSizeMB]
    return candidates

def initFilter(sysProfiles, activeUsers, minSizeMB=50):
    filtered = filterProfiles(sysProfiles, activeUsers)
    candidates = toDelete(filtered, minSizeMB)
    return candidates
