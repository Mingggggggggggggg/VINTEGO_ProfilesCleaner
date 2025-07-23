import argparse
import sys
from getProfiles import getSysProfiles, getDirProfiles
from compareProfiles import compare


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

    sysProfileData = getSysProfiles()
    dirProfileData = getDirProfiles()
    
    #TODO DAS HIER
    if isCompare:
        sysDiff, dirDiff = compare(sysProfileData, dirProfileData)
        
        if sysDiff:
            for i in sysDiff:
                print(f"Nutzer in Registry gefunden, aber nicht im Ordnerverzeichnis: {sysDiff}. Manuelle Überprüfung erforderlich.")

    
    if isDelProfiles:
        if isCompare:
            #del diffRes + <50mb
            pass
        else: 
            #del <50mb
            pass



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet.")
        sys.exit()