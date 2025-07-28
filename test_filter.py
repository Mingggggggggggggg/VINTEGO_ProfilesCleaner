import unittest
import filterProfiles
import os
import json

class TestFilterProfiles(unittest.TestCase):

    def setUp(self):
        self.sysProfiles = [
            #["SysProfile", r"%systemroot%\system32\config\systemprofile", "S-1-5-18", 150.0],
            #["LocalServices", r"%systemroot%\ServiceProfiles\LocalService", "S-1-5-19", 5.5],
            #["NetworkServices", r"%systemroot%\ServiceProfiles\NetworkService", "S-1-5-20", 1.0],
            ["Max", r"C:\Users\Max", "S-1-5-21-1001", 150.0],
            ["Tester", r"C:\Users\Tester", "S-1-5-21-1003", 5.5],
            ["Archiv", r"C:\Users\Archiv", "S-1-5-21-1004", 1.0]
        ]
        self.activeADUsers = [
            ["S-1-5-21-1001", "Max", "max@firma.local"]
        ]

        self.dirProfiles = [
            ["Max", r"C:\Users\Max", 150.0],
            ["Tester", r"C:\Users\Tester", 5.5],
            ["Archiv", r"C:\Users\Archiv", 1.0],
            ["Backup", r"C:\Users\Backup", 0.8],
        ]

    def test_filterProfiles(self):
        filtered = filterProfiles.filterProfiles(self.sysProfiles, self.activeADUsers)
        print("\nGefilterte Profile (nicht aktiv):")
        for prof in filtered:
            print(f"  Name: {prof[0]}, Pfad: {prof[1]}, SID: {prof[2]}, Größe: {prof[3]} MB")

        filtered_sids = {p[2] for p in filtered}
        expected_sids = {"S-1-5-21-1003", "S-1-5-21-1004"}
        self.assertEqual(filtered_sids, expected_sids)

    def test_toDelete(self):
        filterProfiles.getProfiles.getDirProfiles = lambda: self.dirProfiles

        filtered = [
            ["Tester", r"C:\Users\Tester", "S-1-5-21-1003", 5.5],
            ["Archiv", r"C:\Users\Archiv", "S-1-5-21-1004", 1.0],
        ]

        original_exists = os.path.exists
        os.path.exists = lambda path: True

        candidates = filterProfiles.toDelete(filtered, minSizeMB=10)
        print("\nZu löschende Kandidaten:")
        for cand in candidates:
            print(f"  Name: {cand[0]}, Pfad: {cand[1]}, SID: {cand[2]}, Größe: {cand[3]} MB")

        os.path.exists = original_exists

        candidate_paths = {c[1].lower() for c in candidates}
        expected_paths = {r"c:\users\tester", r"c:\users\archiv", r"c:\users\backup"}
        self.assertTrue(expected_paths.issubset(candidate_paths))


if __name__ == "__main__":
    unittest.main()
