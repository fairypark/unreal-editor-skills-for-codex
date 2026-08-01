import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(
    os.environ.get(
        "UNREAL_METRICS_SCRIPT_UNDER_TEST",
        str(REPO_ROOT / "scripts" / "usage-metrics.ps1"),
    )
)
EXTENSION_CATALOG = REPO_ROOT / "scripts" / "unreal-toolsets-extension-catalog.json"


class UsageMetricsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.metrics_root = self.root / "metrics"
        self.project_root = self.root / "project"
        self.project_root.mkdir()
        (self.project_root / "TestProject.uproject").write_text("{}", encoding="utf-8")

    def tearDown(self):
        self.temporary.cleanup()

    def run_script(
        self,
        action="Hook",
        hook_input=None,
        rating=None,
        target=None,
        shareable=False,
        check=True,
    ):
        command = [
            "powershell.exe",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(SCRIPT),
            "-Action",
            action,
        ]
        if rating is not None:
            command.extend(["-Rating", str(rating)])
        if target is not None:
            command.extend(["-Target", target])
        if shareable:
            command.append("-Shareable")
        environment = os.environ.copy()
        environment["UNREAL_CODEX_METRICS_HOME"] = str(self.metrics_root)
        return subprocess.run(
            command,
            input=None if hook_input is None else json.dumps(hook_input),
            text=True,
            encoding="utf-8",
            capture_output=True,
            env=environment,
            check=check,
        )

    def read_events(self):
        path = self.metrics_root / "events.jsonl"
        if not path.exists():
            return []
        return [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def session_start(self, cwd=None):
        return {
            "session_id": "session-secret",
            "transcript_path": "C:/private/transcript.jsonl",
            "cwd": str(cwd or self.project_root),
            "hook_event_name": "SessionStart",
            "model": "test-model",
            "permission_mode": "default",
            "source": "startup",
        }

    def tool_event(
        self,
        event_name,
        response=None,
        toolset="ActorToolset",
        tool="SetActorTransform",
        meta_tool="call_tool",
        tool_use_id="tool-use-secret",
        arguments=None,
    ):
        event = {
            "session_id": "session-secret",
            "turn_id": "turn-secret",
            "transcript_path": "C:/private/transcript.jsonl",
            "cwd": str(self.project_root),
            "hook_event_name": event_name,
            "model": "test-model",
            "permission_mode": "default",
            "tool_name": f"mcp__unreal_mcp__{meta_tool}",
            "tool_use_id": tool_use_id,
            "tool_input": {
                "toolset_name": toolset,
                "tool_name": tool,
                "arguments": arguments
                if arguments is not None
                else {
                    "actor": "BP_PrivateHero",
                    "path": "C:/Private/Project/Content/SecretAsset.uasset",
                },
            },
        }
        if response is not None:
            event["tool_response"] = response
        return event

    def list_toolsets_event(self, event_name, response=None, tool_use_id="list-toolsets"):
        return self.tool_event(
            event_name,
            response=response,
            toolset=None,
            tool=None,
            meta_tool="list_toolsets",
            tool_use_id=tool_use_id,
            arguments={},
        )

    def stop_event(self, turn_id="turn-secret"):
        return {
            "session_id": "session-secret",
            "turn_id": turn_id,
            "cwd": str(self.project_root),
            "hook_event_name": "Stop",
            "permission_mode": "default",
            "stop_hook_active": False,
            "last_assistant_message": "Private assistant response",
        }

    def test_first_use_prompts_without_collecting(self):
        result = self.run_script(hook_input=self.session_start())
        payload = json.loads(result.stdout)
        context = payload["hookSpecificOutput"]["additionalContext"]
        self.assertIn("local-only anonymous usage metrics", context)
        self.assertFalse((self.metrics_root / "settings.json").exists())
        self.assertFalse((self.metrics_root / "events.jsonl").exists())

    def test_non_unreal_directory_does_not_prompt(self):
        other = self.root / "other"
        other.mkdir()
        result = self.run_script(hook_input=self.session_start(cwd=other))
        self.assertEqual("", result.stdout.strip())
        self.assertFalse(self.metrics_root.exists())

    def test_changed_consent_version_prompts_again_without_collecting(self):
        self.metrics_root.mkdir()
        (self.metrics_root / "settings.json").write_text(
            json.dumps(
                {
                    "consent_version": 1,
                    "status": "enabled",
                    "collection": "local_only",
                    "salt": "old-local-salt",
                }
            ),
            encoding="utf-8",
        )
        result = self.run_script(hook_input=self.session_start())
        self.assertIn("additionalContext", result.stdout)
        self.assertFalse((self.metrics_root / "events.jsonl").exists())
        status = json.loads(self.run_script(action="Status").stdout)
        self.assertEqual("unset", status["status"])
        self.assertEqual("enabled", status["saved_status"])
        self.assertEqual(2, status["current_consent_version"])

    def test_extension_adapter_catalog_is_versioned_and_exact(self):
        catalog = json.loads(EXTENSION_CATALOG.read_text(encoding="utf-8"))
        self.assertEqual(1, catalog["contract_version"])
        self.assertEqual("UnrealToolsetsExtension", catalog["extension"])
        self.assertEqual(7, len(set(catalog["toolsets"])))
        self.assertEqual(36, len(catalog["operations"]))
        self.assertEqual(
            36,
            len(
                {
                    (operation["toolset"], operation["operation"])
                    for operation in catalog["operations"]
                }
            ),
        )
        self.assertEqual(65, len(catalog["errors"]))
        self.assertEqual(
            65,
            len({descriptor["code"] for descriptor in catalog["errors"]}),
        )
        self.assertTrue(
            all(
                operation["class"]
                in {
                    "discovery",
                    "read",
                    "validation",
                    "mutation",
                    "mutation_capable",
                    "save",
                }
                for operation in catalog["operations"]
            )
        )
    def test_enable_collect_summarize_and_sanitize(self):
        enabled = json.loads(self.run_script(action="Enable").stdout)
        self.assertEqual("enabled", enabled["status"])

        self.run_script(hook_input=self.session_start())
        self.run_script(hook_input=self.tool_event("PreToolUse"))
        self.run_script(
            hook_input=self.tool_event(
                "PostToolUse",
                response={
                    "success": True,
                    "content": "Changed BP_PrivateHero at C:/Private/Project/SecretAsset.uasset",
                },
            )
        )
        stop = {
            "session_id": "session-secret",
            "turn_id": "turn-secret",
            "cwd": str(self.project_root),
            "hook_event_name": "Stop",
            "permission_mode": "default",
            "stop_hook_active": False,
            "last_assistant_message": "Private assistant response",
        }
        stop_result = self.run_script(hook_input=stop)
        self.assertEqual({}, json.loads(stop_result.stdout))

        raw_events = (self.metrics_root / "events.jsonl").read_text(encoding="utf-8")
        for private_value in (
            "session-secret",
            "turn-secret",
            "tool-use-secret",
            "BP_PrivateHero",
            "SecretAsset",
            "Private assistant response",
            "transcript.jsonl",
        ):
            self.assertNotIn(private_value, raw_events)

        events = self.read_events()
        self.assertEqual(
            ["session_eligible", "tool_started", "tool_finished", "turn_summary"],
            [event["event"] for event in events],
        )
        self.assertEqual("success", events[2]["outcome"])
        self.assertEqual("mutation", events[2]["operation"])

        summary = json.loads(self.run_script(action="Summary").stdout)
        self.assertEqual(1, summary["eligible_sessions"])
        self.assertEqual(1, summary["active_sessions"])
        self.assertEqual(1, summary["tool_calls"])
        self.assertEqual(100, summary["tool_success_rate_percent"])

    def test_structured_failure_is_counted(self):
        self.run_script(action="Enable")
        self.run_script(hook_input=self.tool_event("PreToolUse"))
        self.run_script(
            hook_input=self.tool_event(
                "PostToolUse",
                response={"result": {"status": "failed"}, "content": "not stored"},
            )
        )
        events = self.read_events()
        self.assertEqual("failure", events[-1]["outcome"])

    def test_extension_catalog_eligibility_outcomes_and_targeted_summary(self):
        self.run_script(action="Enable")
        self.run_script(hook_input=self.session_start())

        self.run_script(hook_input=self.list_toolsets_event("PreToolUse"))
        self.run_script(
            hook_input=self.list_toolsets_event(
                "PostToolUse",
                response={
                    "success": True,
                    "result": {
                        "toolsets": [
                            "ActorToolset",
                            "LandscapeExtensionToolset",
                            "ObservabilityExtensionToolset",
                        ]
                    },
                },
            )
        )

        self.run_script(
            hook_input=self.tool_event(
                "PreToolUse",
                toolset="ObservabilityExtensionToolset",
                tool="GetExtensionObservabilityInfo",
                tool_use_id="extension-info",
            )
        )
        self.run_script(
            hook_input=self.tool_event(
                "PostToolUse",
                response={
                    "success": True,
                    "result": {
                        "extension_version": "0.1.0",
                        "engine_version": "5.8.0",
                        "observability_contract_version": 1,
                        "private": "C:/Private/Project/DoNotStore",
                    },
                },
                toolset="ObservabilityExtensionToolset",
                tool="GetExtensionObservabilityInfo",
                tool_use_id="extension-info",
            )
        )

        self.run_script(
            hook_input=self.tool_event(
                "PreToolUse",
                toolset="PlacementExtensionToolset",
                tool="SnapActorToGround",
                tool_use_id="extension-mutation",
            )
        )
        self.run_script(
            hook_input=self.tool_event(
                "PostToolUse",
                response={
                    "success": True,
                    "content": "Moved BP_PrivateHero in C:/Private/Project",
                },
                toolset="PlacementExtensionToolset",
                tool="SnapActorToGround",
                tool_use_id="extension-mutation",
            )
        )
        self.run_script(
            hook_input=self.tool_event(
                "PreToolUse",
                toolset="LandscapeExtensionToolset",
                tool="GetLandscapeInfo",
                tool_use_id="extension-read",
            )
        )
        self.run_script(
            hook_input=self.tool_event(
                "PostToolUse",
                response={"success": True, "content": "Private Landscape payload"},
                toolset="LandscapeExtensionToolset",
                tool="GetLandscapeInfo",
                tool_use_id="extension-read",
            )
        )
        self.run_script(hook_input=self.stop_event())
        self.run_script(
            action="Feedback",
            rating=5,
            target="UnrealToolsetsExtension",
        )

        raw_events = (self.metrics_root / "events.jsonl").read_text(encoding="utf-8")
        for private_value in (
            "C:/Private/Project",
            "BP_PrivateHero",
            "Private Landscape payload",
            "DoNotStore",
        ):
            self.assertNotIn(private_value, raw_events)

        events = self.read_events()
        eligible = [event for event in events if event["event"] == "extension_eligible"]
        self.assertEqual(1, len(eligible))
        extension_calls = [
            event
            for event in events
            if event["event"] == "tool_finished"
            and event.get("extension") == "UnrealToolsetsExtension"
        ]
        self.assertEqual("0.1.0", extension_calls[0]["extension_version"])
        mutation = next(
            event
            for event in extension_calls
            if event.get("tool") == "SnapActorToGround"
        )
        self.assertEqual("mutation", mutation["extension_operation_class"])
        self.assertEqual(
            "internal_postcondition", mutation["extension_verification"]
        )

        summary = json.loads(
            self.run_script(
                action="Summary",
                target="UnrealToolsetsExtension",
            ).stdout
        )
        self.assertEqual(1, summary["eligible_sessions"])
        self.assertEqual(1, summary["active_sessions"])
        self.assertEqual(2, summary["tool_calls"])
        self.assertEqual(1, summary["successful_self_verifying_mutations"])
        self.assertEqual(1, summary["workflow_followup_verification_turns"])
        self.assertEqual(5, summary["average_feedback_rating"])
        self.assertFalse(summary["automatic_transmission"])

        shareable = json.loads(
            self.run_script(
                action="Summary",
                target="UnrealToolsetsExtension",
                shareable=True,
            ).stdout
        )
        self.assertEqual("shareable_aggregate", shareable["collection"])
        self.assertEqual(5, shareable["operation_minimum_sample_count"])
        self.assertEqual([], shareable["operations"])

    def test_extension_failure_keeps_only_allowlisted_error_code(self):
        self.run_script(action="Enable")
        self.run_script(
            hook_input=self.tool_event(
                "PreToolUse",
                toolset="PlacementExtensionToolset",
                tool="SnapActorToGround",
                tool_use_id="failed-extension-call",
            )
        )
        self.run_script(
            hook_input=self.tool_event(
                "PostToolUse",
                response={
                    "success": False,
                    "content": (
                        "[PLACEMENT_EXTENSION_NO_GROUND_HIT] "
                        "BP_PrivateHero at C:/Private/Secret had no hit"
                    ),
                },
                toolset="PlacementExtensionToolset",
                tool="SnapActorToGround",
                tool_use_id="failed-extension-call",
            )
        )
        event = self.read_events()[-1]
        self.assertEqual("PLACEMENT_EXTENSION_NO_GROUND_HIT", event["error_code"])
        self.assertEqual("precondition", event["failure_category"])
        raw_events = (self.metrics_root / "events.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("BP_PrivateHero", raw_events)
        self.assertNotIn("C:/Private/Secret", raw_events)

    def test_mutation_capable_dry_run_is_not_counted_as_confirmed_mutation(self):
        self.run_script(action="Enable")
        self.run_script(
            hook_input=self.tool_event(
                "PreToolUse",
                toolset="LandscapeExtensionToolset",
                tool="ReimportLandscapeData",
                tool_use_id="dry-run",
                arguments={
                    "request": {
                        "bDryRun": True,
                        "source": "C:/Private/Height.raw",
                    }
                },
            )
        )
        self.run_script(
            hook_input=self.tool_event(
                "PostToolUse",
                response={"success": True, "result": {"bDryRun": True}},
                toolset="LandscapeExtensionToolset",
                tool="ReimportLandscapeData",
                tool_use_id="dry-run",
            )
        )
        summary = json.loads(
            self.run_script(
                action="Summary",
                target="UnrealToolsetsExtension",
            ).stdout
        )
        self.assertEqual(0, summary["confirmed_mutation_calls"])
        self.assertEqual(1, summary["mutation_capable_calls"])
        raw_events = (self.metrics_root / "events.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("bDryRun", raw_events)
        self.assertNotIn("Height.raw", raw_events)

    def test_disable_stops_new_collection_without_deleting(self):
        self.run_script(action="Enable")
        self.run_script(hook_input=self.session_start())
        before = (self.metrics_root / "events.jsonl").read_text(encoding="utf-8")

        disabled = json.loads(self.run_script(action="Disable").stdout)
        self.assertEqual("disabled", disabled["status"])
        self.assertTrue(disabled["existing_data_retained"])

        self.run_script(hook_input=self.tool_event("PreToolUse"))
        after = (self.metrics_root / "events.jsonl").read_text(encoding="utf-8")
        self.assertEqual(before, after)

        stop = {
            "session_id": "session-secret",
            "turn_id": "turn-secret",
            "cwd": str(self.project_root),
            "hook_event_name": "Stop",
            "stop_hook_active": False,
        }
        self.assertEqual({}, json.loads(self.run_script(hook_input=stop).stdout))

    def test_feedback_and_delete(self):
        self.run_script(action="Enable")
        feedback = json.loads(self.run_script(action="Feedback", rating=5).stdout)
        self.assertTrue(feedback["recorded"])
        summary = json.loads(self.run_script(action="Summary").stdout)
        self.assertEqual(5, summary["average_feedback_rating"])

        deleted = json.loads(self.run_script(action="Delete").stdout)
        self.assertTrue(deleted["deleted"])
        self.assertFalse((self.metrics_root / "events.jsonl").exists())
        status = json.loads(self.run_script(action="Status").stdout)
        self.assertEqual("enabled", status["status"])


if __name__ == "__main__":
    unittest.main()
