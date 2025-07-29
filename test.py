import sys
from filterProfiles import filterProfiles, toDelete

sysProfiles = [
    ["max", r"C:\Users\max", "S-1-5-21-1111", 120],     # aktiv, groß genug → behalten
    ["emma", r"C:\Users\emma", "S-1-5-21-2222", 40],     # inaktiv, < minSize → löschen
    ["lisa", r"C:\Users\lisa", "S-1-5-21-3333", 10],     # inaktiv, < minSize → löschen
    ["admin", r"C:\Users\admin", "S-1-5-18", 300],       # ausgeschlossen → wird ignoriert
]
activeADUsers = [
    ["S-1-5-21-1111", "max", "max@firma.de"],
]
dirProfiles = [
    ["max", r"C:\Users\max", 120],       # gehört zu aktivem Benutzer → behalten
    ["emma", r"C:\Users\emma", 40],      # Registry + Ordner, inaktiv → löschen
    ["temp", r"C:\Users\temp", 8],       # Nur Ordner, kein Registry-Eintrag → löschen
    ["setup", r"C:\Users\setup", 250],   # Nur Ordner, groß genug → behalten
]

if __name__ == "__main__":
    try:
        pass
    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet.")
        sys.exit()
