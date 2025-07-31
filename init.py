import argparse
import sys
import manageProfiles
import logger
from filterProfiles import initFilter


log = []

def getArgs():
    parser = argparse.ArgumentParser(description="Anwendung zum Anzeigen ungenutzter Benutzerprofile mit Möglichkeit zum Löschen. Verwaiste Nutzer im Ordnerverzeichnis und Nutzer unter der Mindestgröße werden gelöscht.")
    parser.add_argument("minSize", 
                        type=int, 
                        help="[INTEGER] Mindestgröße in MB von Profilen, die gelöscht werden sollen.")
    parser.add_argument("--delProfiles", 
                        action="store_true", 
                        help="Sollen die Profile gelöscht werden?")
    return parser.parse_args()

def main():
    args = getArgs()
    minSize = args.minSize
    delProfile = args.delProfiles

    log.append(f"Mindestgröße: {minSize} MB | Löschen aktiviert: {delProfile}")


    candidates = initFilter(minSize)

    if delProfile:
        log.append("Starte Profilbereinigung von:")
        for c in candidates:
            username, path, sid, size = c
            print(f"{username:<20} {size:>6} MB  | {sid}")
            log.append(f"{username:<20} {size:>6} MB  | {sid}")
        manageProfiles.initCleanup(candidates)
        log.append("Profilbereinigung abgeschlossen.")
        log.append("\nÜberprüfe Erfolg.")
        success = manageProfiles.checkSuccess(candidates)
        log.append("Check beendet")
        logger.logMessages("Erfolgsmessung", success)
    else:
        print("Löschen deaktiviert. Folgende Profile wären betroffen:")
        log.append("Löschen deaktiviert. Zeige Löschkandidaten an")
        for c in candidates:
            username, path, sid, size = c
            print(f"{username:<20} {size:>6} MB  | {sid}")
            log.append(f"{username:<20} {size:>6} MB  | {sid}")
        print("Ende Löschkandidaten")
        log.append("Ende Löschkndidaten")

    logger.logMessages("Status", log, top=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet.")
        sys.exit()