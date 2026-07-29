import unittest
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "environment-level-design"


class EnvironmentLevelDesignSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.quality = (
            SKILL_ROOT / "references" / "quality-gates.md"
        ).read_text(encoding="utf-8")
        cls.landscape = (
            SKILL_ROOT / "references" / "landscape-ecology-and-collision.md"
        ).read_text(encoding="utf-8")
        cls.pcg = (
            SKILL_ROOT / "references" / "pcg-biome-orchestration.md"
        ).read_text(encoding="utf-8")
        cls.prompt = (
            SKILL_ROOT / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        cls.handoff = (
            REPO_ROOT / "docs" / "UNREAL_TOOLSETS_EXTENSION_HANDOFF.md"
        ).read_text(encoding="utf-8")
        cls.plugin_manifest = json.loads(
            (REPO_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )

    def test_visual_gate_precedes_performance_and_gameplay(self):
        visual = self.skill.index("Visual quality and art-direction fidelity")
        performance = self.skill.index("Technical stability and performance budgeting")
        gameplay = self.skill.index("Gameplay experience and encounter")
        self.assertLess(visual, performance)
        self.assertLess(performance, gameplay)
        self.assertIn("Do not start Gameplay Polish until this gate passes", self.quality)
        self.assertIn("Visual Gate regression", self.quality)
        self.assertIn("Visual Gate", self.prompt)
        self.assertTrue(
            any(
                "Visual Gate" in prompt and "before gameplay polish" in prompt
                for prompt in self.plugin_manifest["interface"]["defaultPrompt"]
            )
        )

    def test_minimum_safety_exception_is_narrow(self):
        for required in (
            "underwater or below terrain",
            "unavoidable lethal fall",
            "primary route is completely blocked",
            "global collision",
            "crashes",
        ):
            self.assertIn(required, self.quality)
        self.assertIn(
            "Do not broaden this gate into encounter, route, or performance polish",
            self.quality,
        )

    def test_visual_gate_requires_360_and_depth_evidence(self):
        for required in (
            "four cardinal directions",
            "low, player-height, middle, and elevated views",
            "foreground, midground, and background",
            "non-planar macro/mid terrain",
            "locally flat building pads",
            "empty-space ratio",
        ):
            self.assertIn(required, self.quality)

    def test_pcg_benchmark_and_orchestrator_are_required(self):
        for required in (
            "BqPhdQOweqU",
            "SCDZ8kobv1M",
            "`Biome Boundary`",
            "`Density Field`",
            "`Exclusion Sources`",
            "`Layer Subgraphs`",
            "`Output/Audit`",
            "edge-to-core density",
            "multi-scale noise",
        ):
            self.assertIn(required, self.pcg)

    def test_vertical_strata_are_independent(self):
        for stratum in (
            "canopy",
            "secondary trees and saplings",
            "shrubs",
            "fern and herb layer",
            "groundcover",
            "deadwood and debris",
            "geology",
        ):
            self.assertIn(stratum, self.pcg)
        self.assertIn("Do not mix all mesh sizes on one point set", self.pcg)

    def test_context_distribution_and_audit_contract(self):
        for required in (
            "water exclusion",
            "inner/outer bank bands",
            "surface, clear width, shoulder, and edge bands",
            "Poisson or blue-noise",
            "core/middle/edge coverage percentage",
            "explicit empty-volume reasons",
            "deterministic output fingerprint",
        ):
            self.assertIn(required, self.pcg)

    def test_safe_existing_tool_orchestration_and_gap_routing(self):
        for tool in (
            "ListNativeNodes",
            "CreateGraph",
            "SetGraphParams",
            "AddSubgraphNode",
            "ConnectNodePins",
            "GetGraphStructure",
            "SpawnGraphInstance",
            "ExecuteGraphInstance",
        ):
            self.assertIn(tool, self.pcg)
        self.assertIn("ambiguous generic `ArrayAdd`", self.pcg)
        self.assertIn("external runtime gap", self.pcg)
        self.assertIn("must not contain, build, package", self.handoff)

    def test_collision_preserves_visual_placement(self):
        for required in (
            "do not trust the stock `snap_to_ground`",
            "negative world Z",
            "`NoCollision`",
            "collision-safe duplicate",
            "trunk capsule",
        ):
            self.assertIn(required, self.landscape)
        self.assertIn(
            "Collision defects do not authorize deletion",
            self.landscape,
        )

    def test_handoff_covers_runtime_p0_p1_fab_and_distribution(self):
        for required in (
            "Unreal Toolsets Extension",
            "independent and unofficial",
            "`.r16` heightmaps",
            "Streaming Proxy audit",
            "`SnapActorToGround`",
            "`LandscapeGrassType`",
            "PCG weighted mesh entries",
            "`CaptureViewport`",
            "Fab feasibility",
            "separate public Unreal Editor plugin",
        ):
            self.assertIn(required, self.handoff)
        self.assertNotIn("CodexMiniArena", self.handoff)

    def test_reusable_skill_contains_no_project_specific_map(self):
        all_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_ROOT.rglob("*")
            if path.is_file()
        )
        for forbidden in (
            "CodexMiniArena",
            "Lvl_JoseonGrandRiverRetreat",
            "C:\\Users\\user",
        ):
            self.assertNotIn(forbidden, all_text)


if __name__ == "__main__":
    unittest.main()
