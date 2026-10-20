import csv
import unittest

from scrub_s2.assessment import ROOT, component_hazards, elements, read_json, summary


class AssessmentTraceTests(unittest.TestCase):
    def setUp(self):
        self.assessment = read_json("RA-S2-WGH-01.json")["assessment"]
        self.nodes = {n["reference"]: n for n in elements(self.assessment["system"])}

    def test_camera_links_resolve_from_source_ids(self):
        self.assertEqual([h["reference"] for h in component_hazards(self.assessment, "PER-01")],
                         ["HS-01", "HS-02", "HS-18"])

    def test_pending_site_release_is_preserved(self):
        report = summary()
        self.assertEqual(report["site_release"], "PENDING")
        self.assertEqual(report["pending_hazards"], ["HS-05", "HS-09", "HS-13", "HS-19"])

    def test_bom_contains_every_component_with_original_identifier(self):
        with (ROOT / "hardware/bom.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        expected = {ref for ref, node in self.nodes.items() if node["kind"] == "COMPONENT"}
        self.assertEqual({row["reference"] for row in rows}, expected)
        self.assertEqual(len(rows), len(expected))
        for row in rows:
            self.assertEqual(row["assessment_element_id"], self.nodes[row["reference"]]["id"])
            self.assertEqual(row["name"], self.nodes[row["reference"]]["name"])

    def test_traceability_resolves_real_components_and_files(self):
        trace = read_json("config/traceability.json")
        for component in trace["components"]:
            with self.subTest(reference=component["reference"]):
                self.assertEqual(component["assessment_element_id"], self.nodes[component["reference"]]["id"])
                for path in component["implementation_paths"]:
                    self.assertTrue((ROOT / path).is_file(), path)

    def test_camera_and_safety_scanner_have_distinct_owners(self):
        robot = read_json("config/robot.json")
        self.assertEqual(robot["perception"]["component_ref"], "PER-01")
        self.assertFalse(robot["perception"]["safety_rated"])
        self.assertEqual(robot["perception"]["connected_to"], "CTL-01")
        self.assertEqual(robot["safety_scanner"]["component_ref"], "PER-02")
        self.assertEqual(robot["safety_scanner"]["connected_to"], "CTL-02")

    def test_unknown_component_is_not_silently_reported_as_unaffected(self):
        with self.assertRaises(ValueError):
            component_hazards(self.assessment, "PER-99")


if __name__ == "__main__":
    unittest.main()
