import sys
from filterProfiles import filterProfiles, toDelete

# Konfigurierbare Mindestgröße in MB
minSizeMB = 50

# Beispielhafte Registry-Profile
sysProfiles = [
    ["max", r"C:\Users\max", "S-1-5-21-1111", 120],     # aktiv, groß genug → behalten
    ["emma", r"C:\Users\emma", "S-1-5-21-2222", 40],     # inaktiv, < minSize → löschen
    ["lisa", r"C:\Users\lisa", "S-1-5-21-3333", 10],     # inaktiv, < minSize → löschen
    ["jan", r"C:\Users\jan", "S-1-5-21-4444", 80],       # inaktiv, aber groß genug → behalten
    ["ghost", r"C:\Users\ghost", "S-1-5-21-5555", 0.0],  # Registry-Leiche (Ordner fehlt) → löschen
    ["admin", r"C:\Users\admin", "S-1-5-18", 300],       # Systemkonto → ignorieren
]

# Aktive AD-Nutzer (nur max ist aktiv)
activeADUsers = [
    ["S-1-5-21-1111", "max", "max@firma.de"],
]

# Simulierte Ordnerprofile – setze bewusst Fälle ohne Registry-Eintrag
def mock_getDirProfiles():
    return [
        ["max", r"C:\Users\max", 120],         # aktiv und vorhanden → behalten
        ["emma", r"C:\Users\emma", 40],        # Registry+Ordner, aber inaktiv & klein → löschen
        ["temp", r"C:\Users\temp", 8],         # DIR_ONLY, klein → löschen
        ["setup", r"C:\Users\setup", 250],     # DIR_ONLY, groß genug → behalten
        ["ghost", r"C:\Users\ghost", 0.0],     # Ordner fehlt → simulierte Registry-Leiche → löschen
    ]

# Mock für os.path.exists – simuliert fehlende Ordner
def mock_exists(path):
    missing = {r"C:\Users\ghost"}  # ghost gibt's nicht als Ordner
    return path not in missing

# Haupttestlauf
if __name__ == "__main__":
    import getProfiles
    import os

    # Mock anwenden
    getProfiles.getDirProfiles = mock_getDirProfiles
    os.path.exists = mock_exists

    try:
        filtered = filterProfiles(sysProfiles, activeADUsers)
        candidates = toDelete(filtered, minSizeMB)

        print("Löschkandidaten:")
        for c in candidates:
            print(f" - {c[0]} ({c[2]}) – {c[3]} MB")

    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet.")
        sys.exit()
