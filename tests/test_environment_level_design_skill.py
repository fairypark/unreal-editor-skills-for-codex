import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "environment-level-design"


class EnvironmentLevelDesignSkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.gates = (SKILL_ROOT / "references" / "quality-gates.md").read_text(
            encoding="utf-8"
        )
        self.supervision = (
            SKILL_ROOT / "references" / "independent-visual-supervision.md"
        ).read_text(encoding="utf-8")
        self.onboarding = (
            SKILL_ROOT / "references" / "visual-quality-onboarding.md"
        ).read_text(encoding="utf-8")
        self.case_study = (
            SKILL_ROOT / "references" / "codex-mini-arena-case-study.md"
        ).read_text(encoding="utf-8")
        self.legacy = (
            SKILL_ROOT / "references" / "visual-first-production-legacy.md"
        ).read_text(encoding="utf-8")
        self.production_assets = (
            SKILL_ROOT / "references" / "reusable-production-assets.md"
        ).read_text(encoding="utf-8")
        self.production_assets_ko = (
            SKILL_ROOT / "references" / "reusable-production-assets.ko.md"
        ).read_text(encoding="utf-8")

    def test_skill_loads_independent_supervision_for_multi_system_work(self):
        self.assertIn("independent-visual-supervision.md", self.skill)
        self.assertIn("multi-system level build", self.skill)

    def test_builder_and_supervisor_roles_are_separated(self):
        self.assertIn("Keep the primary agent as the builder", self.supervision)
        self.assertIn("Remain read-only", self.supervision)
        self.assertIn("Do not mutate Unreal state", self.supervision)

    def test_target_pass_does_not_clear_full_level_gate(self):
        self.assertIn(
            "target `PASS` does not imply full-level `GO`", self.supervision
        )
        self.assertIn(
            "A focused target `PASS` closes only that target", self.gates
        )

    def test_independence_and_evidence_are_protected(self):
        self.assertIn("Do not give it:", self.supervision)
        self.assertIn("the intended verdict", self.supervision)
        self.assertIn("raw capture paths", self.supervision)
        self.assertIn("Change a score only", self.supervision)

    def test_fallback_never_claims_independent_supervision(self):
        phrase = "self-review; not independently supervised"
        self.assertIn(phrase, self.skill)
        self.assertIn(phrase, self.gates)
        self.assertIn(phrase, self.supervision)

    def test_new_project_setup_routes_to_onboarding(self):
        self.assertIn("visual-quality-onboarding.md", self.skill)
        self.assertIn("CodexMiniArena case study", self.skill)
        self.assertIn("`off`, `recommended`, or `strict`", self.skill)

    def test_case_study_is_procedural_not_a_preset(self):
        self.assertIn("not a preset", self.case_study)
        self.assertIn("It does not prescribe", self.case_study)
        self.assertIn("project and machine paths", self.case_study)
        self.assertNotIn("C:/Users/", self.case_study)
        self.assertNotIn("/Game/", self.case_study)

    def test_onboarding_preserves_project_authority(self):
        self.assertIn("Do not edit `AGENTS.md` silently", self.onboarding)
        self.assertIn("A level recipe may make a gate stricter", self.onboarding)
        self.assertIn(
            "Read-only supervision is a role contract", self.onboarding
        )

    def test_visual_quality_templates_are_bundled(self):
        assets = SKILL_ROOT / "assets" / "visual-quality"
        expected = {
            "project-policy.template.yaml",
            "visual-recipe.template.yaml",
            "visual-audit.template.json",
        }
        self.assertEqual(
            expected,
            {path.name for path in assets.iterdir() if path.is_file()},
        )
        audit = json.loads(
            (assets / "visual-audit.template.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            "read-only independent visual evaluator",
            audit["evaluator_role"],
        )
        self.assertEqual("PENDING", audit["verdict"])

    def test_visual_first_legacy_is_loaded_and_portable(self):
        self.assertIn("visual-first-production-legacy.md", self.skill)
        self.assertIn("Persistent Camera Actors", self.legacy)
        self.assertIn("10-30 m golden slice", self.legacy)
        self.assertIn("gpt-5.6-sol", self.legacy)
        self.assertIn("xhigh", self.legacy)
        self.assertIn("NoCollision", self.legacy)
        self.assertIn("Accelerate only approved quality", self.legacy)
        self.assertNotIn("C:/Users/", self.legacy)
        self.assertNotIn("/Game/", self.legacy)

    def test_reusable_production_assets_are_public_contracts(self):
        self.assertIn("reusable-production-assets.md", self.skill)
        self.assertIn("install_production_asset_templates.py", self.skill)
        self.assertIn("Project source library", self.production_assets)
        self.assertIn("Portable system contract", self.production_assets)
        self.assertIn("Unreal content plugin", self.production_assets)
        self.assertIn("REVALIDATION_REQUIRED", self.production_assets)
        self.assertIn("license and dependency audit", self.production_assets)

    def test_korean_production_asset_guide_is_discoverable_and_actionable(self):
        self.assertIn("reusable-production-assets.ko.md", self.skill)
        self.assertIn("reusable-production-assets.ko.md", self.production_assets)
        self.assertIn("재사용 가능한 생산 자산 사용 안내", self.production_assets_ko)
        self.assertIn("가장 쉬운 사용 방법", self.production_assets_ko)
        self.assertIn("terrain-projected-gravel-route.system.json", self.production_assets_ko)
        self.assertIn("clustered-water-vegetation.system.json", self.production_assets_ko)
        self.assertIn("REVALIDATION_REQUIRED", self.production_assets_ko)
        self.assertIn("NoCollision", self.production_assets_ko)
        self.assertNotIn("C:/Users/", self.production_assets_ko)
        self.assertNotIn("/Game/", self.production_assets_ko)

    def test_independent_supervisor_uses_requested_model_and_effort(self):
        self.assertIn('model="gpt-5.6-sol"', self.skill)
        self.assertIn('reasoning_effort="xhigh"', self.skill)
        self.assertIn("visual_critic", self.skill)


if __name__ == "__main__":
    unittest.main()
