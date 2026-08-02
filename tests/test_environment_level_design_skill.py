import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "environment-level-design"
REFERENCE_ROOT = SKILL_ROOT / "references"


class EnvironmentLevelDesignSkillTests(unittest.TestCase):
    def setUp(self):
        self.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.operations = (REFERENCE_ROOT / "editor-environment-operations.md").read_text(
            encoding="utf-8"
        )
        self.evidence = (REFERENCE_ROOT / "evidence-and-supervision.md").read_text(
            encoding="utf-8"
        )
        self.production = (REFERENCE_ROOT / "production-asset-operations.md").read_text(
            encoding="utf-8"
        )
        self.onboarding = (REFERENCE_ROOT / "visual-quality-onboarding.md").read_text(
            encoding="utf-8"
        )

    def test_skill_is_execution_layer_with_optional_handbook(self):
        for required in (
            "execution mechanics",
            "Unreal Development Handbook for Codex",
            "design-unreal-worlds-and-levels",
            "validate-unreal-production",
            "If the Handbook plugin is not installed, do not block",
            "minimum fallback contract",
        ):
            self.assertIn(required, self.skill)

    def test_first_level_activation_announces_mandatory_handbook_guidance(self):
        for required in (
            "first activated in a task",
            "Treat the Handbook plugin as installed",
            "explicitly tell the user",
            "Its applicable Skills and chapter guidance are mandatory",
            "before any Editor mutation",
            "must not weaken or override them",
            "If it is unavailable, do not block the task",
            "once at the first level-work Skill activation in the task",
        ):
            self.assertIn(required, self.skill)

    def test_removed_reasoning_documents_do_not_return(self):
        for removed in (
            "codex-mini-arena-case-study.md",
            "level-brief-and-iteration-log.md",
            "quality-gates.md",
            "visual-first-production-legacy.md",
            "reusable-production-assets.md",
            "reusable-production-assets.ko.md",
            "landscape-ecology-and-collision.md",
            "independent-visual-supervision.md",
        ):
            self.assertFalse((REFERENCE_ROOT / removed).exists(), removed)
            self.assertNotIn(removed, self.skill)

    def test_only_execution_references_are_loaded(self):
        for reference in (
            "editor-environment-operations.md",
            "evidence-and-supervision.md",
            "production-asset-operations.md",
            "visual-quality-onboarding.md",
        ):
            self.assertIn(reference, self.skill)
            self.assertTrue((REFERENCE_ROOT / reference).is_file())

    def test_live_mutations_are_sequential_and_verified(self):
        for required in (
            "Keep game-thread MCP calls sequential",
            "source-control or saved-copy recovery point",
            "re-query representative objects",
            "inspect the resulting state before retrying",
            "save state",
        ):
            self.assertIn(required, self.skill)

    def test_landscape_pcg_and_collision_operations_are_concrete(self):
        for required in (
            "trusted terrain surface",
            "deterministic seeds",
            "one candidate generation at a time",
            "Navigation influence",
            "parent-child transforms",
            "center and surrounding points",
            "actual player capsule",
            "Keep Unreal game-thread calls sequential",
        ):
            self.assertIn(required, self.operations)

    def test_persistent_camera_evidence_is_bound_and_reverified(self):
        self.assertIn("VisualEvidenceExtensionToolset", self.skill)
        self.assertIn("CaptureCameraToPng", self.skill)
        self.assertIn("VerifyEvidenceForSupervision", self.skill)
        for required in (
            "persistent `CameraActor`",
            ".evidence.json",
            "1280x720",
            "external trust anchors",
            "three warmup draws",
            "two consecutive stable frame pairs",
            "64-character SHA-256",
            "jointly rewritten",
        ):
            self.assertIn(required, self.evidence)

    def test_supervisor_handoff_is_neutral_and_read_only(self):
        for required in (
            "schema-restricted Review Submission",
            "reject unknown fields",
            "intended verdicts",
            "immutable Supervisor Packet",
            "read-only",
            "factual change scope",
            "Do not supply the intended verdict",
            "self-review; not independently supervised",
        ):
            self.assertIn(required, self.evidence)

    def test_model_configuration_is_not_frozen_in_plugin_content(self):
        combined = self.skill + self.evidence
        self.assertNotIn("gpt-5.6-sol", combined)
        self.assertNotIn('reasoning_effort="xhigh"', combined)
        self.assertIn("host or project policy", combined)

    def test_production_contracts_remain_installable(self):
        for required in (
            "ProductionAssetCatalog.template.json",
            "terrain-projected-gravel-route.system.json",
            "clustered-water-vegetation.system.json",
            "install_production_asset_templates.py",
            "refuses existing destinations",
            "REVALIDATION_REQUIRED",
            "Do not add project UAssets",
        ):
            self.assertIn(required, self.production)

    def test_workspace_initializer_cannot_manufacture_readiness(self):
        for required in (
            "refuse overwrites",
            "`PENDING_RUNTIME`",
            "must not invent captures",
            "File creation is setup, not visual approval",
        ):
            self.assertIn(required, self.onboarding)


if __name__ == "__main__":
    unittest.main()
