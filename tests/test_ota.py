import hashlib
import unittest

from scrub_s2 import ota
from scrub_s2.assessment import read_json


PAYLOAD = b"scrub-s2 firmware image"
MANIFEST = {"updates": [
    {"target": "navigation", "version": "4.3.0", "sha256": hashlib.sha256(PAYLOAD).hexdigest()},
    {"target": "safety_plc_firmware", "version": "2.4.0", "sha256": hashlib.sha256(PAYLOAD).hexdigest()},
]}
DOCKED = {"docked": True, "idle": True}


class OtaTests(unittest.TestCase):
    def setUp(self):
        config = read_json("config/robot.json")
        self.config = config
        self.installed = {"navigation": config["navigation_version"],
                          "safety_plc_firmware": config["safety_plc_firmware"]}

    def test_newer_versions_are_pending(self):
        pending = ota.pending_updates(self.config, self.installed, MANIFEST)
        self.assertEqual([entry["target"] for entry in pending], ["navigation", "safety_plc_firmware"])

    def test_installed_versions_are_not_pending(self):
        installed = {"navigation": "4.3.0", "safety_plc_firmware": "2.4.0"}
        self.assertEqual(ota.pending_updates(self.config, installed, MANIFEST), [])

    def test_install_requires_docked_and_idle(self):
        for state in [{}, {"docked": True}, {"idle": True}]:
            with self.subTest(state=state), self.assertRaises(RuntimeError):
                ota.apply(self.config, self.installed, MANIFEST["updates"][0], PAYLOAD, state)

    def test_checksum_mismatch_is_rejected(self):
        with self.assertRaises(ValueError):
            ota.apply(self.config, self.installed, MANIFEST["updates"][1], b"tampered", DOCKED)

    def test_apply_updates_installed_version(self):
        result = ota.apply(self.config, self.installed, MANIFEST["updates"][1], PAYLOAD, DOCKED)
        self.assertEqual(result["safety_plc_firmware"], "2.4.0")


if __name__ == "__main__":
    unittest.main()
