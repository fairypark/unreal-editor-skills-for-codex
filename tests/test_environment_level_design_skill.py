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

    def test_architecture_placement_requires_automatic_four_corner_routing(self):
        for required in (
            "$building-grounding",
            "Mandatory building-grounding routing",
            "before the first architecture mutation",
            "every building Actor",
            "all four load-bearing base",
            "PCG",
            "Blueprint construction script",
        ):
            self.assertIn(required, self.skill)

    def test_area_composition_plan_is_a_blocking_preprototype_gate(self):
        for required in (
            "Mandatory Area Composition Plan preflight",
            "after the approved source references and before the first cube or graybox prototype",
            "zone boundaries and stable IDs",
            "terrain elevations and steps",
            "primary circulation",
            "rivers and bridges",
            "building footprints and typology hierarchy",
            "fixed validation cameras",
            "Do not create the first cube",
            "broad asset-placement batch",
            "reconstructed from a blockout afterward",
        ):
            self.assertIn(required, self.skill)

        for required in (
            "Area Composition Plan preflight",
            "plan ID or path",
            "perform read-only inspection only",
            "Reopen the plan gate",
            "Area Composition Plan ID and version",
        ):
            self.assertIn(required, self.operations)

    def test_blank_level_lighting_waits_for_approved_design(self):
        for required in (
            "Gate blank-level observation lighting behind approved design",
            "created, saved, and inspected read-only earlier",
            "do not spawn or modify",
            "Stage 1 Concept",
            "Stage 2 Area Composition Plan",
            "contract and Area Composition Plan",
            "Keep the lighting mutation read-only",
            "Post-design blank-level observation baseline",
            "record and preserve its World Partition",
            "Do not change partition",
        ):
            self.assertIn(required, self.skill)

        self.assertLess(
            self.skill.index("### 0. Area Composition Plan and design preflight"),
            self.skill.index("### 0a. Post-design blank-level observation baseline"),
        )

    def test_blockout_enforces_the_approved_floor_plan_spatial_lock(self):
        for required in (
            "Enforce the approved floor plan during blockout",
            "exact approved version becomes the spatial mutation lock",
            "plan feature ID",
            "Reject unmapped or freehand placement",
            "re-query the realized transforms",
            "stop all subsequent blockout placement",
            "Do not backfit the plan",
            "post-batch spatial-conformance audit",
            "fallback plan-feature trace",
            "it does not depend on Handbook stage numbering",
        ):
            self.assertIn(required, self.skill)

        self.assertLess(
            self.skill.index("## Enforce the approved floor plan during blockout"),
            self.skill.index("### 1. Playable skeleton"),
        )

    def test_blockout_requires_independent_reference_fidelity_iteration(self):
        for required in (
            "Gate blockout promotion through independent supervision",
            "BLOCKOUT_REFERENCE_FIDELITY_REVIEW=PASS",
            "separate read-only independent supervisor",
            "self-review cannot promote the blockout",
            "DESIGN_REVIEW_REQUIRED",
            "Report any material delay to the user immediately",
            "Do not wait for the budget to expire",
            "### 1a. Independent blockout reference-fidelity gate",
        ):
            self.assertIn(required, self.skill)

        for required in (
            "Mandatory blockout fidelity loop",
            "raw concept art and floor plan when required by the contract",
            "never use them to waive missing required evidence",
            "Handbook stage numbering is not a standalone prerequisite",
            "same camera and runtime conditions",
            "root-cause record",
            "Do not wait until the budget expires before reporting",
        ):
            self.assertIn(required, self.evidence)

        self.assertLess(
            self.skill.index("### 1a. Independent blockout reference-fidelity gate"),
            self.skill.index("### 2. Representative slice"),
        )

    def test_blockout_cubes_remain_internal_and_non_visual(self):
        for required in (
            "Retire blockout cubes from the production visual surface",
            "`REPLACE`, `RETIRE`, or `RETAIN_INTERNAL_SKELETON`",
            "non-visual internal skeleton",
            "Do not expose a face",
            "assign a production finish material",
            "BLOCKOUT_CUBE_VISUAL_RETIREMENT=PASS",
            "Any visible or material-finished blockout primitive",
            "### 1b. Blockout-cube visual-retirement gate",
            "Material assignment never promotes blockout geometry",
            "Permit bounded replacement and meshing after Stage 1a passes",
            "do not require whole-level retirement before making the first slice",
            "before accepting the slice or expanding its systems",
        ):
            self.assertIn(required, self.skill)

        for required in (
            "Blockout primitive visual retirement",
            "current material and render state",
            "fully enclose the primitive with approved production geometry",
            "hidden-in-game",
            "Do not assign a production finish material to an exposed blockout cube",
            "treat material replacement as production meshing",
            "Reject any material batch",
            "BLOCKOUT_CUBE_VISUAL_RETIREMENT=PASS",
        ):
            self.assertIn(required, self.operations)

        self.assertLess(
            self.skill.index("### 1a. Independent blockout reference-fidelity gate"),
            self.skill.index("### 1b. Blockout-cube visual-retirement gate"),
        )
        self.assertLess(
            self.skill.index("### 1b. Blockout-cube visual-retirement gate"),
            self.skill.index("### 2. Representative slice"),
        )

    def test_typology_critical_layout_uses_axis_and_hard_failures(self):
        for required in (
            "matching building sizes alone does not pass",
            "gate -> outer court -> middle gate -> central courtyard -> main hall axis",
            "fortress- or castle-like silhouette is a hard failure",
        ):
            self.assertIn(required, self.skill)

        for required in (
            "Typology-critical layout checks",
            "Do not approve a typology from width, length, height, or Actor bounds alone",
            "dominant keep",
            "return to the Area Composition Plan",
        ):
            self.assertIn(required, self.operations)

    def test_zone_markers_persist_from_preprototype_through_asset_placement(self):
        for required in (
            "Mandatory zone-identification lifecycle",
            "Before the first prototype geometry mutation",
            "LD_ZONE_MARKER",
            "numeric ID plus ASCII fallback",
            "completion of production asset placement",
            "all numeric IDs and ASCII fallbacks readable",
            "player-scale reference",
            "explicit cleanup step",
            "do not retire markers as part of blockout cleanup",
        ):
            self.assertIn(required, self.skill)

        for required in (
            "Zone markers and scale evidence",
            "stable zone registry",
            "numeric review ID",
            "active font supporting it",
            "completed production asset placement",
            "player-scale character or metric reference",
            "zone-marker inventory",
        ):
            self.assertIn(required, self.operations)

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

    def test_gameplay_visibility_uses_player_camera_not_overview(self):
        for required in (
            "project's actual player tracking camera",
            "height above local ground and FOV",
            "`DIAGNOSTIC_ONLY`",
            "never use them to approve player visibility",
            "overview-only evidence",
        ):
            self.assertIn(required, self.evidence)

        for required in (
            "project's actual player tracking camera",
            "Label high overview or bird's-eye cameras `DIAGNOSTIC_ONLY`",
            "never use them to approve player visibility",
        ):
            self.assertIn(required, self.skill)

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
