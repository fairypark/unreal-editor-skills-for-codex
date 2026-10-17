import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/environment-level-design/scripts/validate_spatial_field_samples.py"
spec = importlib.util.spec_from_file_location("field_samples", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture():
    authority = {"field_id": "habitat", "revision": "r1", "coordinate_frame": "local-xyz", "units": "cm"}
    points = [{"id": "interior", "position": [10, 20, 0], "value": 0.5}, {"id": "negative-edge", "position": [-100, 0, 0], "value": 0.25}]
    return {"schema_version": 1, "authority": authority, "tolerance": 0.01, "reference_samples": points, "consumers": [{"id": "shader", **authority, "samples": copy.deepcopy(points)}]}


class SpatialFieldSamplesTests(unittest.TestCase):
    def test_matching_samples_do_not_grant_visual_or_provenance_approval(self):
        result = module.validate(fixture())
        self.assertEqual(result["status"], "PASS_PARITY_ONLY")
        self.assertEqual(result["visual_approval"], "NOT_GRANTED")
        self.assertEqual(result["sample_provenance"], "NOT_VERIFIED")

    def test_changed_field_values_fail_even_with_same_identity(self):
        data = fixture()
        data["consumers"][0]["samples"][0]["value"] = 0.7
        self.assertEqual(module.validate(data)["status"], "FAIL_PARITY")

    def test_permuted_sample_order_is_supported(self):
        data = fixture()
        data["consumers"][0]["samples"].reverse()
        self.assertEqual(module.validate(data)["status"], "PASS_PARITY_ONLY")

    def test_every_consumer_and_sample_must_pass(self):
        data = fixture()
        bad = copy.deepcopy(data["consumers"][0])
        bad["id"] = "second-path"
        bad["samples"][1]["value"] = 0.5
        data["consumers"].append(bad)
        self.assertEqual(module.validate(data)["status"], "FAIL_PARITY")

    def test_stale_revision_units_and_coordinate_frame_are_invalid(self):
        for field in ("field_id", "revision", "units", "coordinate_frame"):
            with self.subTest(field=field):
                data = fixture()
                data["consumers"][0][field] = "other"
                self.assertEqual(module.validate(data)["status"], "INVALID_INPUT")

    def test_incomplete_or_duplicate_coverage_and_position_drift_are_invalid(self):
        for change in ("missing", "duplicate", "position", "extra"):
            with self.subTest(change=change):
                data = fixture()
                rows = data["consumers"][0]["samples"]
                if change == "missing": rows.pop()
                if change == "duplicate": rows.append(copy.deepcopy(rows[0]))
                if change == "position": rows[0]["position"][0] += 1
                if change == "extra": rows.append({"id": "extra", "position": [0, 0, 0], "value": 0})
                self.assertEqual(module.validate(data)["status"], "INVALID_INPUT")

    def test_nonfinite_bool_and_out_of_range_values_are_invalid(self):
        for value in (float("nan"), float("inf"), True, -0.1, 1.1, 10**1000):
            with self.subTest(value_type=type(value).__name__):
                data = fixture()
                data["consumers"][0]["samples"][0]["value"] = value
                self.assertEqual(module.validate(data)["status"], "INVALID_INPUT")

    def test_invalid_tolerances_and_empty_consumers_are_invalid(self):
        for value in (None, True, -1, 2, float("nan")):
            data = fixture()
            data["tolerance"] = value
            self.assertEqual(module.validate(data)["status"], "INVALID_INPUT")
        data = fixture()
        data["consumers"] = []
        self.assertEqual(module.validate(data)["status"], "INVALID_INPUT")

    def test_duplicate_consumers_are_invalid(self):
        data = fixture()
        data["consumers"].append(copy.deepcopy(data["consumers"][0]))
        self.assertEqual(module.validate(data)["status"], "INVALID_INPUT")

    def test_cli_rejects_duplicate_json_keys_at_any_depth(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "samples.json"
            valid = json.dumps(fixture())
            for text in (valid.replace('"schema_version": 1', '"schema_version": 2, "schema_version": 1', 1),
                         valid.replace('"value": 0.5', '"value": 1, "value": 0.5', 1)):
                path.write_text(text, encoding="utf-8")
                before = path.read_bytes()
                result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertEqual(path.read_bytes(), before)
                output = json.loads(result.stdout)
                self.assertEqual(output["status"], "INVALID_INPUT")
                self.assertIn("duplicate JSON object key", output["error"])

    def test_cli_exit_code_and_read_only_behavior(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "samples.json"
            for bad in (False, True):
                data = fixture()
                if bad: data["consumers"][0]["samples"][0]["value"] = 0
                path.write_text(json.dumps(data), encoding="utf-8")
                before = path.read_bytes()
                result = subprocess.run([sys.executable, "-B", str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1 if bad else 0)
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual(json.loads(result.stdout)["status"], "FAIL_PARITY" if bad else "PASS_PARITY_ONLY")


if __name__ == "__main__":
    unittest.main()
