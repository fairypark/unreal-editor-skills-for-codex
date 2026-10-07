import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills" / "unreal-mcp" / "SKILL.md").read_text(encoding="utf-8")
NORMALIZED_SKILL = " ".join(SKILL.split())
OPERATIONS = (
    ROOT / "skills" / "unreal-mcp" / "references" / "operations.md"
).read_text(encoding="utf-8")
SETUP = (ROOT / "skills" / "unreal-mcp" / "references" / "setup.md").read_text(
    encoding="utf-8"
)
PREFLIGHT = (
    ROOT / "skills" / "unreal-mcp" / "scripts" / "check_endpoint.py"
).read_text(encoding="utf-8")


class UnrealMcpRecoveryPolicyTests(unittest.TestCase):
    def test_new_level_work_routes_through_the_handbook_gate(self):
        for required in (
            "creates, rebuilds, dresses, or materially changes a level",
            "do not use this low-level Skill as the first execution path",
            "environment-level-design",
            "its first level-work activation must announce",
            "before any Editor mutation",
        ):
            self.assertIn(required, SKILL)

    def test_isolated_building_placement_routes_through_grounding(self):
        for required in (
            "$building-grounding",
            "narrow operation",
            "all four load-bearing base corners",
            "A low-level transform or spawn success does not replace",
        ):
            self.assertIn(required, NORMALIZED_SKILL)

    def test_skill_routes_custom_port_recovery_to_operations(self):
        self.assertIn("non-default endpoint", SKILL)
        self.assertIn("Do not run the no-argument", SKILL)
        self.assertIn("references/operations.md", SKILL)

    def test_runtime_endpoint_requires_three_independent_facts(self):
        self.assertIn("three independent facts", OPERATIONS)
        self.assertIn("Codex MCP URL", OPERATIONS)
        self.assertIn("Unreal settings", OPERATIONS)
        self.assertIn("live listener", OPERATIONS)

    def test_custom_port_recovery_preserves_unsaved_work(self):
        self.assertIn("Save the affected level and assets", OPERATIONS)
        self.assertIn("-ModelContextProtocolStartServer", OPERATIONS)
        self.assertIn("-ModelContextProtocolPort=<port>", OPERATIONS)

    def test_wrong_port_restart_is_not_accepted(self):
        self.assertIn("starting on port 8000", OPERATIONS)
        self.assertIn("failed recovery", OPERATIONS)
        self.assertIn("do not issue repeated start commands", OPERATIONS)

    def test_recovered_listener_does_not_imply_current_task_reconnected(self):
        self.assertIn("does not prove that the current task reconnected", OPERATIONS)
        self.assertIn("Start a new task", OPERATIONS)

    def test_setup_requires_runtime_evidence(self):
        self.assertIn("Configuration files alone are not runtime evidence", SETUP)
        self.assertIn("owned by the Unreal Editor process", SETUP)

    def test_skill_requires_deterministic_preflight_before_mutation(self):
        self.assertIn("scripts/check_endpoint.py", SKILL)
        self.assertIn("PENDING_LIST_TOOLSETS", SKILL)
        self.assertIn("runtime_endpoint_verdict", PREFLIGHT)
        self.assertIn("listener_owner", PREFLIGHT)


if __name__ == "__main__":
    unittest.main()
