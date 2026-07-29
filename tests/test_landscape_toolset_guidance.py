import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CREATE_TOOLSET_SKILL = REPO_ROOT / "skills" / "create-toolset" / "SKILL.md"
UNREAL_MCP_SKILL = REPO_ROOT / "skills" / "unreal-mcp" / "SKILL.md"
LANDSCAPE_REFERENCE = (
    REPO_ROOT
    / "skills"
    / "create-toolset"
    / "references"
    / "landscape-toolset.md"
)


class LandscapeToolsetGuidanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = LANDSCAPE_REFERENCE.read_text(encoding="utf-8")
        cls.create_skill = CREATE_TOOLSET_SKILL.read_text(encoding="utf-8")
        cls.unreal_skill = UNREAL_MCP_SKILL.read_text(encoding="utf-8")

    def test_all_candidate_tools_have_typed_contracts(self):
        for tool_name in (
            "GetLandscapeInfo",
            "CreateLandscape",
            "ImportHeightmap",
            "ReimportHeightmap",
            "ImportWeightmap",
            "SetLandscapeMaterial",
            "GetHeightStatistics",
            "ValidateBuildingPad",
            "SaveLandscape",
        ):
            self.assertIn(f"static FLandscape", self.reference)
            self.assertIn(f"{tool_name}(", self.reference)

    def test_reimport_contract_covers_guarded_transaction(self):
        for required_text in (
            "GetHeightmapImportDescriptor",
            "LANDSCAPE_SOURCE_RESOLUTION_MISMATCH",
            "Save every dirty affected package before mutation",
            "capture the original uint16 height data",
            "LANDSCAPE_WORLD_PARTITION_PARTIAL",
            "center, four corners, and four edge midpoints",
            "world-space Z range",
            "Roll back on every failure",
            "typed success result or a raised failure",
        ):
            self.assertIn(required_text, self.reference)

    def test_ui_fallback_requires_observer_cleanup(self):
        self.assertIn("SlateInspectorToolset.Unobserve", self.reference)
        self.assertIn("including after errors", self.reference)
        self.assertIn("ListObservers", self.reference)
        self.assertIn("SlateInspectorToolset.Unobserve", self.unreal_skill)
        self.assertIn("finally-style cleanup", self.unreal_skill)

    def test_runtime_ownership_is_not_claimed_by_codex_plugin(self):
        self.assertIn(
            "does not ship its Unreal Editor implementation",
            self.reference,
        )
        self.assertIn("AllToolsets.uplugin", self.reference)
        self.assertIn("Never edit `AllToolsets.uplugin`", self.reference)
        self.assertIn(
            "does not own a runtime Unreal extension",
            self.create_skill,
        )

    def test_skills_route_without_duplicating_level_design(self):
        self.assertIn(
            "[references/landscape-toolset.md](references/landscape-toolset.md)",
            self.create_skill,
        )
        self.assertIn("environment-level-design", self.create_skill)
        self.assertIn("Never assume `LandscapeExtensionToolset` is installed", self.unreal_skill)
        self.assertIn("external-project handoff contract", self.unreal_skill)

    def test_batch_reimport_and_proxy_audit_are_handoff_requirements(self):
        for required_text in (
            "combined `.r16` heightmap and `.r8` layer-map workflow",
            "dry-run",
            "exact raw-data backup",
            "data layers",
            "streaming proxy audit",
            "proxy count",
            "stale-plan",
        ):
            self.assertIn(required_text, self.reference.lower())

    def test_skills_repository_contains_no_runtime_plugin_source(self):
        runtime_root = REPO_ROOT / "unreal-plugins"
        runtime_files = [
            path
            for path in runtime_root.rglob("*")
            if path.is_file()
        ] if runtime_root.exists() else []
        self.assertEqual([], runtime_files)
        for removed_path in (
            REPO_ROOT / "scripts" / "package-unreal-extension.ps1",
            REPO_ROOT / "scripts" / "build-unreal-extension-github-release.ps1",
        ):
            self.assertFalse(removed_path.exists())


if __name__ == "__main__":
    unittest.main()
