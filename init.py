import argparse
import sys


minSize = 50

def getArgs():
    parser = argparse.ArgumentParser(description="Anwendung zum Anzeigen ungenutzter Benutzerprofile mit Möglichkeit zum Löschen.")
    parser.add_argument("minSize", 
                        type=int, 
                        help="[INTEGER] Setze mindestgröße zu Profilen, die gelöscht werdn sollen.")
    parser.add_argument("--compare", 
                        default="false", 
                        help="[true/false] Sollen die Windows-Benutzerkonten mit dem Nutzer-Ordnerverzeichnis verglichen werden?")
    parser.add_argument("--delProfiles", 
                        default="false", 
                        help="[true/false] Sollen die Profile gelöscht werden? Wenn compare = true, dann auch ungenutzte Nutzer im Ordnerverzeichnis.")
    return parser.parse_args() 

def main():
    args = getArgs()
    minSize: int = args.minSize
    isCompare: bool = args.compare.lower() == "true"
    isDelProfiles: bool = args.delProfiles.lower() == "true"




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet.")
        sys.exit()