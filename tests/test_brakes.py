import unittest

from scrub_s2.assessment import read_json
from scrub_s2.controller import simulate


class BrakeControllerTests(unittest.TestCase):
    def setUp(self):
        self.config = read_json("config/robot.json")

    def stop(self, **frame):
        return simulate(self.config, {"name": "test", "mode": "autonomous", "requested_speed_mps": 0, **frame})

    def test_normal_stop_waits_before_braking(self):
        self.assertFalse(self.stop(stationary_ms=399)["brakes_engaged"])
        self.assertTrue(self.stop(stationary_ms=400)["brakes_engaged"])

    def test_emergency_stop_brakes_immediately(self):
        self.assertTrue(self.stop(stationary_ms=0, e_stop=True)["brakes_engaged"])


if __name__ == "__main__":
    unittest.main()
