# Name des Benutzers
$userName = "Test 2"

# Benutzerobjekt abrufen
$user = Get-WmiObject -Class Win32_UserAccount -Filter "Name='$userName' AND LocalAccount=True"

if ($user) {
    try {
        # Benutzerkonto löschen
        net user "$userName" /delete
        Write-Output "Benutzer '$userName' wurde gelöscht."

        # Profilverzeichnis ermitteln und löschen
        $profile = Get-WmiObject Win32_UserProfile | Where-Object {
            $_.LocalPath -like "*\$userName" -and !$_.Special
        }

        if ($profile) {
            $profile.Delete()
            Write-Output "Profilverzeichnis von '$userName' wurde gelöscht."
        } else {
            Write-Warning "Kein Profilverzeichnis für '$userName' gefunden."
        }
    } catch {
        Write-Error "Fehler beim Löschen von '$userName': $_"
    }
} else {
    Write-Warning "Benutzer '$userName' wurde nicht gefunden."
}
