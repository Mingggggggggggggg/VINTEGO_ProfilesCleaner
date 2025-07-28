import os
import getProfiles
import filterProfiles
import shutil
import logger
import winreg

#Wenn DIR_ONLY an Index 2 gefunden wird, dann den Ordner im Ordnerverzeichnis löschen
#Wenn SID an Index 2, dann AD-User über powershell entfernen, Ordner im Verzeichnis löschen und ggf Registry!!!!! Wichtig ist nachgefragt
#TODO Recherche und überarbeiten
def deleteRegistryProfile(candidates):
    #Lösche Registryeintrag. UNBEKANNT OB MUSS!
    pass

def deleteADUser(candidates):
    #Lösche ADUser über Powershell
    pass

def deleteDir(candidates):
    # Wenn DIR_ONLY dann Ordner löschen 
    pass

#TODO überprüfen
def initCleanup(candidates):
    pass
