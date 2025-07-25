import argparse
import sys
import getProfiles
import manageProfiles
import logger

log = []

def getArgs():
    parser = argparse.ArgumentParser(description="Anwendung zum Anzeigen ungenutzter Benutzerprofile mit Möglichkeit zum Löschen. Verwaiste Nutzer im Ordnerverzeichnis und Nutzer unter der Mindestgröße werden gelöscht.")
    parser.add_argument("minSize", 
                        type=int, 
                        help="[INTEGER] Mindestgröße in MB von Profilen, die gelöscht werden sollen.")
    parser.add_argument("--delProfiles", 
                        default="false", 
                        help="[true/false] Sollen die Profile gelöscht werden?")
    return parser.parse_args()

def main():
    args = getArgs()
    minSize = args.minSize
    delProfile = args.delProfiles.lower() == "true"

    log.append(f"Mindestgröße: {minSize} MB Löschen aktiviert: {delProfile}")

    sysProfiles, activeUsers = getProfiles.initGetProfiles()
    
    if not sysProfiles:
        print("Keine Profile gefunden.")
        return

    if delProfile:
        log.append("Starte Profilbereinigung.")
        manageProfiles.cleanSysProfiles(minSize)
        manageProfiles.cleanDirProfiles(minSize)
        log.append("Profilbereinigung abgeschlossen.")
    else:
        print("\nKeine Löschung durchgeführt. Nur Anzeige der Profile.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet.")
        sys.exit()