from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = (
    ROOT
    / "skills"
    / "environment-level-design"
    / "references"
    / "editor-environment-operations.md"
)
SKILL = ROOT / "skills" / "environment-level-design" / "SKILL.md"


class PcgExecutionFallbackTests(unittest.TestCase):
    def test_fallback_keeps_only_operational_exclusion_and_culling_checks(self):
        text = REFERENCE.read_text(encoding="utf-8")
        for required in (
            "Dependent-Strata Strategy Gate",
            "CONSIDERED",
            "VIDEO_DISTANCE_EXCLUSION",
            "selected mode",
            "dependent placement read-only",
            "single exclusion authority",
            "clearance or transition band",
            "final bounds gap",
            "do not rely only on center-point distance",
            "Do not infer that enabling Nanite enables distance culling",
            "target platform",
        ):
            self.assertIn(required, text)

    def test_skill_blocks_dependent_mutation_until_strategy_is_recorded(self):
        text = SKILL.read_text(encoding="utf-8")
        for required in (
            "Dependent-Strata Strategy Gate",
            "discovering or invoking",
            "first PCG",
            "dependent placement read-only",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
