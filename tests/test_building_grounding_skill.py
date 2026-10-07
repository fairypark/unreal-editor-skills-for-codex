import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "building-grounding"


class BuildingGroundingSkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.normalized_skill = " ".join(self.skill.split())
        self.interface = (SKILL_ROOT / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )

    def test_skill_has_codex_metadata_and_interface(self):
        for required in (
            "name: building-grounding",
            "description:",
            "Four-Corner Building Grounding",
            "$building-grounding",
        ):
            self.assertIn(required, self.skill + self.interface)

    def test_grounding_is_four_corner_and_not_center_only(self):
        for required in (
            "SW",
            "SE",
            "NW",
            "NE",
            "all four named base corners",
            "A result with three grounded corners",
            "center height",
            "edge midpoints",
        ):
            self.assertIn(required, self.normalized_skill)

    def test_surface_authority_and_trace_safety_are_explicit(self):
        for required in (
            "trusted Landscape",
            "ignore the target Actor and its children",
            "reject hits on props",
            "no authoritative hit",
            "PENDING_EVIDENCE",
        ):
            self.assertIn(required, self.normalized_skill)

    def test_rigid_slope_and_non_planar_fallback_are_defined(self):
        for required in (
            "SLOPE_ALIGN",
            "VERTICAL_FOUNDATION",
            "Fit a support plane",
            "preserving the intended heading",
            "terrain is not sufficiently planar",
            "authored stepped/retaining foundation",
        ):
            self.assertIn(required, self.skill)

    def test_transform_collision_persistence_and_sequential_safety_are_defined(self):
        for required in (
            "Preserve scale",
            "Keep Unreal game-thread calls sequential",
            "Preserve location, rotation, and scale together",
            "collision and Navigation check",
            "Save the affected level",
            "re-read them to confirm persistence",
        ):
            self.assertIn(required, self.normalized_skill)

    def test_success_requires_four_final_measurements(self):
        for required in (
            "Recompute the four final world-space support corners",
            "Require all four rows to pass",
            "Mark the",
            "PASS",
            "within tolerance",
        ):
            self.assertIn(required, self.skill)


if __name__ == "__main__":
    unittest.main()
