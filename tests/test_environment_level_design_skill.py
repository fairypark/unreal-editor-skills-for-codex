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
        self.landscape = (
            SKILL_ROOT
            / "references"
            / "landscape-ecology-and-collision.md"
        ).read_text(encoding="utf-8")
        self.brief = (
            SKILL_ROOT / "references" / "level-brief-and-iteration-log.md"
        ).read_text(encoding="utf-8")
        self.legacy = (
            SKILL_ROOT / "references" / "visual-first-production-legacy.md"
        ).read_text(encoding="utf-8")

    def test_visual_first_legacy_is_loaded_for_every_level(self):
        self.assertIn("visual-first-production-legacy.md", self.skill)
        for required in (
            "arrival, hero,",
            "route, and reverse",
            "persistent `CameraActor`",
            "10–30 m golden slice",
            "visual_critic",
            "`gpt-5.6-sol`",
            "`xhigh`",
            "at least 4/5",
            "NoCollision",
            "Landscape, mesh terrain, or a hybrid",
            "waterline mist",
            "one width-bearing surface",
            "Accelerate only approved quality",
            "Previous approval never transfers",
        ):
            self.assertIn(required, self.legacy)

    def test_reusable_production_assets_are_public_plugin_resources(self):
        self.assertIn("reusable-production-assets.md", self.skill)
        self.assertIn("install_production_asset_templates.py", self.skill)
        reference = (
            SKILL_ROOT / "references" / "reusable-production-assets.md"
        ).read_text(encoding="utf-8")
        for required in (
            "Project source library",
            "Portable system contract",
            "Unreal content plugin",
            "REVALIDATION_REQUIRED",
            "license and dependency audit",
            "terrain-projected-gravel-route.system.json",
            "clustered-water-vegetation.system.json",
        ):
            self.assertIn(required, reference)

    def test_skill_loads_independent_supervision_for_multi_system_work(self):
        self.assertIn("independent-visual-supervision.md", self.skill)
        self.assertIn("multi-system level build", self.skill)

    def test_builder_and_supervisor_roles_are_separated(self):
        self.assertIn("Keep the primary agent as the builder", self.supervision)
        self.assertIn("Remain read-only", self.supervision)
        self.assertIn("Do not mutate Unreal state", self.supervision)

    def test_independent_supervisor_uses_xhigh_reasoning(self):
        for document in (self.skill, self.supervision):
            self.assertIn('model="gpt-5.6-sol"', document)
            self.assertIn('reasoning_effort="xhigh"', document)
            self.assertIn("visual_critic", document)
            self.assertIn("highest supported", document)
        self.assertIn(
            "Do not raise the builder's reasoning",
            self.skill,
        )
        self.assertIn("Never silently downgrade", self.supervision)

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

    def test_persistent_camera_evidence_is_file_and_metadata_verified(self):
        self.assertIn(
            "VisualEvidenceExtensionToolset.CaptureCameraToPng",
            self.skill,
        )
        self.assertIn("VerifyEvidenceForSupervision", self.skill)
        for required in (
            "persistent `CameraActor`",
            "CameraRole",
            ".evidence.json",
            "1280x720",
            "receipt SHA-256",
            "trust anchors",
            "jointly-rewritten",
            "three warmup draws",
            "two consecutive stable frame pairs",
            "64-character",
            "SHA-256",
            "thumbnail-sized fallback",
            "handoff time",
        ):
            self.assertIn(required, self.supervision)
        self.assertIn(
            "successful handoff-time verification is not evidence",
            self.gates,
        )

    def test_procedural_patterns_promote_relationship_then_contact(self):
        for required in (
            "relationship before proceduralizing it",
            "semantic root",
            "dependent children",
            "isolated assembly relationship",
            "placement contact",
            "surrounding points",
            "surface-normal tolerances",
        ):
            self.assertIn(required, self.landscape)
        self.assertIn("Procedural pattern cards", self.brief)
        self.assertIn("Hero, Reverse, and Contact", self.brief)

    def test_procedural_comparisons_validate_inputs_and_isolate_outputs(self):
        for required in (
            "line up every candidate spawn mesh",
            "final material",
            "exactly one procedural candidate at a time",
            "Overlapping generations",
            "invalidate",
            "structured technical audit",
            "generated instance count by responsibility",
            "Navigation influence",
            "grounded ratio at a documented tolerance",
            "do not grant visual",
            "approval",
            "initial authoring time separately from regeneration time",
        ):
            self.assertIn(required, self.landscape)

    def test_final_render_evidence_requires_gpu_warmup(self):
        for document in (self.gates, self.supervision):
            self.assertIn("Render Warm Up Frames", document)
            self.assertIn("Object ID", document)
            self.assertIn("beauty evidence", document)

    def test_complete_decision_package_has_unambiguous_statuses(self):
        for required in (
            "quality-run manifest",
            "external PNG/receipt",
            "MRQ/MRG beauty-render configuration",
            "`GO`",
            "`NO-GO`",
            "`PENDING_RUNTIME`",
            "`INVALID`",
            "complete decision package has not returned `GO`",
        ):
            self.assertIn(required, self.gates)

    def test_workspace_initializer_cannot_manufacture_readiness(self):
        for required in (
            "workspace initializer",
            "`PENDING_RUNTIME`",
            "must not invent an",
            "evidence hashes",
            "`GO` verdict",
            "Refuse overwrites",
        ):
            self.assertIn(required, self.skill)
        for required in (
            "refuse overwrites",
            "never manufacture an audit",
            "Concept-ready cameras may remain",
            "`aspirational_frame_ready`",
        ):
            self.assertIn(required, self.gates)

    def test_repeated_no_go_forces_documented_composition_reset(self):
        for required in (
            "visual iteration history",
            "macro-composition ID",
            "consecutive `NO-GO` threshold",
            "documented composition reset",
            "new macro ID",
            "More dressing cannot clear",
        ):
            self.assertIn(required, self.skill)
        for required in (
            "append-only visual iteration history",
            "`composition_reset=true`",
            "new macro-composition ID",
            "Fog, foliage, props, lighting",
        ):
            self.assertIn(required, self.gates)
        self.assertIn("Current macro-composition ID", self.brief)

    def test_supervisor_handoff_uses_sanitized_packet(self):
        for required in (
            "schema-restricted Review Submission",
            "rejects unknown fields",
            "builder scores",
            "intended verdicts",
            "completion claims",
            "external PNG/receipt hash trust anchors",
            "immutable Supervisor Packet",
            "hand-written summary is not a",
        ):
            self.assertIn(required, self.supervision)
        self.assertIn("supervisor-packet", self.skill)

    def test_concept_is_an_observable_frame_contract(self):
        for required in (
            "observable frame contract",
            "normalized anchor",
            "depth layers",
            "value hierarchy",
            "horizon",
            "target and tolerance",
            "primary-mass occupancy",
            "maximum unarticulated",
            "diagnostic constraints",
            "automatic beauty",
        ):
            self.assertIn(required, self.skill)
        self.assertIn("frame-contract overlay", self.gates)
        self.assertIn(
            "applicable observable frame contracts",
            self.supervision,
        )


if __name__ == "__main__":
    unittest.main()
