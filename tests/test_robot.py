import copy
import unittest

from scrub_s2.assessment import read_json
from scrub_s2.controller import simulate


class RobotBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.config = read_json("config/robot.json")

    def run_frame(self, **overrides):
        return simulate(self.config, {"name": "test", "mode": "autonomous", **overrides})

    def test_each_mode_caps_requested_speed(self):
        for mode, limit in {"autonomous": 0.8, "teleoperation": 0.5,
                            "setup": 0.3, "docking": 0.2}.items():
            with self.subTest(mode=mode):
                result = self.run_frame(mode=mode, requested_speed_mps=2, hold_to_run=True)
                self.assertEqual(result["speed_mps"], limit)

    def test_person_slowdown_boundary(self):
        for distance, expected in [(0, 0.3), (1.5, 0.3), (2, 0.3), (2.01, 0.8)]:
            with self.subTest(distance=distance):
                self.assertEqual(self.run_frame(person_distance_m=distance)["speed_mps"], expected)

    def test_each_protective_input_stops_drive_and_brushes_in_every_mode(self):
        for signal in ("e_stop", "protective_field", "bumper", "cliff"):
            for mode in self.config["speed_limits_mps"]:
                with self.subTest(signal=signal, mode=mode):
                    result = self.run_frame(mode=mode, hold_to_run=True, cleaning=True, **{signal: True})
                    self.assertEqual(result["speed_mps"], 0)
                    self.assertEqual(result["brushes_rpm"], 0)
                    self.assertTrue(result["brakes_engaged"])

    def test_protective_field_does_not_depend_on_rgb_camera(self):
        result = self.run_frame(protective_field=True, camera_available=False)
        self.assertIn("PER-02 safety LiDAR field occupied", result["stop_reasons"])

    def test_brushes_require_cleaning_motion_and_lowered_deck(self):
        self.assertEqual(self.run_frame(cleaning=True)["brushes_rpm"], 200)
        for changes in [{"deck_lifted": True}, {"requested_speed_mps": 0},
                        {"mode": "teleoperation"}, {"cleaning": False}]:
            with self.subTest(changes=changes):
                self.assertEqual(self.run_frame(**{"cleaning": True, **changes})["brushes_rpm"], 0)

    def test_video_latency_boundary(self):
        self.assertEqual(self.run_frame(mode="teleoperation", video_latency_ms=300)["speed_mps"], 0.5)
        self.assertEqual(self.run_frame(mode="teleoperation", video_latency_ms=301)["speed_mps"], 0)

    def test_heartbeat_timeout_boundary(self):
        self.assertEqual(self.run_frame(mode="teleoperation", heartbeat_age_ms=499)["speed_mps"], 0.5)
        self.assertEqual(self.run_frame(mode="teleoperation", heartbeat_age_ms=500)["speed_mps"], 0)

    def test_no_rgb_view_inhibits_remote_driving(self):
        result = self.run_frame(mode="teleoperation", camera_available=False)
        self.assertFalse(result["rgb_video_available"])
        self.assertEqual(result["speed_mps"], 0)

    def test_range_only_outputs_do_not_satisfy_video_dependency(self):
        self.config["perception"]["outputs"] = ["range_scan"]
        self.assertEqual(self.run_frame(mode="teleoperation")["speed_mps"], 0)

    def test_missing_camera_holds_autonomous_demo(self):
        self.assertEqual(self.run_frame(camera_available=False)["speed_mps"], 0)

    def test_setup_requires_hold_to_run(self):
        self.assertEqual(self.run_frame(mode="setup")["speed_mps"], 0)
        self.assertEqual(self.run_frame(mode="setup", hold_to_run=True)["speed_mps"], 0.3)

    def test_slowdown_never_increases_a_lower_requested_speed(self):
        self.assertEqual(self.run_frame(person_distance_m=1, requested_speed_mps=0.1)["speed_mps"], 0.1)

    def test_unknown_sensor_requires_an_implementation(self):
        self.config["perception"]["type"] = "navigation_lidar"
        with self.assertRaisesRegex(ValueError, "sensor adapter"):
            self.run_frame()

    def test_bad_motion_requests_are_rejected(self):
        for requested in [-1, float("nan"), float("inf"), "fast"]:
            with self.subTest(requested=requested), self.assertRaises(ValueError):
                self.run_frame(requested_speed_mps=requested)
        with self.assertRaises(ValueError):
            self.run_frame(mode="flight")

    def test_simulation_is_repeatable_without_mutating_inputs(self):
        for frame in read_json("fixtures/scenarios.json"):
            with self.subTest(frame=frame["name"]):
                before = copy.deepcopy((self.config, frame))
                self.assertEqual(simulate(self.config, frame), simulate(self.config, frame))
                self.assertEqual((self.config, frame), before)


if __name__ == "__main__":
    unittest.main()
