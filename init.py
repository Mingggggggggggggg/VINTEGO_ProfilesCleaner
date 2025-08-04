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
            print(f"{c}")
            log.append(f"{c}")
        manageProfiles.initCleanup(candidates)
        log.append("Profilbereinigung abgeschlossen.")
        log.append("\nÜberprüfe Erfolg.")
        successLog = manageProfiles.checkSuccess(candidates)
        log.append("Check beendet")
        logger.logMessages("Erfolgsmessung", successLog)
    else:
        print("Löschen deaktiviert. Folgende Profile wären betroffen:")
        log.append("Löschen deaktiviert. Zeige Löschkandidaten.")
        for c in candidates:
            print(f"{c}")
            log.append(f"{c}")
        print("Ende Löschkandidaten")
        log.append("Ende Löschkndidaten")

    logger.logMessages("Status", log, top=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet.")
        sys.exit()