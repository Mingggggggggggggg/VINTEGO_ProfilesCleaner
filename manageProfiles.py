import subprocess
import shutil
import os

def removeProfiles(toDeleteSys):

    for name, path in toDeleteSys:
        print(f"Entferne Benutzerprofil '{name}' ")

        try:
            subprocess.run([
                "powershell", "-Command",
                f"Remove-LocalUser -Name '{name}'"
            ], check=True)
            print(f"✔ Benutzer '{name}' erfolgreich entfernt.")
        except subprocess.CalledProcessError as e:
            print(f"✖ Fehler beim Entfernen von '{name}': {e}")
        except Exception as e:
            print(f"✖ Unerwarteter Fehler: {e}")


def delUserFolder(toDeleteDir):
    for name, path in toDeleteDir:
        print(f"[Ordner] Versuche, Ordner von '{name}' zu löschen: {path}")
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                print(f"✔ Ordner '{path}' erfolgreich gelöscht.")
            else:
                print(f"⚠ Ordner '{path}' existiert nicht mehr.")
        except Exception as e:
            print(f"✖ Fehler beim Löschen von '{path}': {e}")
