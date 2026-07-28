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

    def run_script(self, action="Hook", hook_input=None, rating=None, check=True):
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

    def tool_event(self, event_name, response=None):
        event = {
            "session_id": "session-secret",
            "turn_id": "turn-secret",
            "transcript_path": "C:/private/transcript.jsonl",
            "cwd": str(self.project_root),
            "hook_event_name": event_name,
            "model": "test-model",
            "permission_mode": "default",
            "tool_name": "mcp__unreal_mcp__call_tool",
            "tool_use_id": "tool-use-secret",
            "tool_input": {
                "toolset_name": "ActorToolset",
                "tool_name": "SetActorTransform",
                "arguments": {
                    "actor": "BP_PrivateHero",
                    "path": "C:/Private/Project/Content/SecretAsset.uasset",
                },
            },
        }
        if response is not None:
            event["tool_response"] = response
        return event

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
                    "consent_version": 0,
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
