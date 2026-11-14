import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "unreal-mcp" / "scripts" / "check_endpoint.py"
SPEC = importlib.util.spec_from_file_location("check_endpoint", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class UnrealMcpEndpointPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project = Path(self.temp_dir.name)
        (self.project / "Sample.uproject").write_text("{}", encoding="utf-8")
        self.client = self.project / ".mcp.json"
        self.client.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "unreal-mcp": {
                            "type": "http",
                            "url": "http://127.0.0.1:8008/mcp",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        ini = (
            self.project
            / "Saved"
            / "Config"
            / "WindowsEditor"
            / "EditorPerProjectUserSettings.ini"
        )
        ini.parent.mkdir(parents=True)
        ini.write_text(
            "[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]\n"
            "ServerUrlPath=/mcp\n"
            "ServerPortNumber=8008\n"
            "bAutoStartServer=True\n"
            "bEnableToolSearch=True\n",
            encoding="utf-8",
        )
        self.log = self.project / "Saved" / "Logs" / "Sample.log"
        self.log.parent.mkdir(parents=True)
        self.log.write_text(
            "LogModelContextProtocol: Starting MCP server on port 8008 "
            "(override with -ModelContextProtocolPort=N).\n"
            "LogHttpListener: Created new HttpListener on 127.0.0.1:8008\n",
            encoding="utf-8",
        )
        self.netstat = (
            "  TCP    127.0.0.1:8008    0.0.0.0:0    LISTENING    4242\n"
        )
        self.workspace_config = self.project / ".codex" / "config.toml"
        self.workspace_config.parent.mkdir()
        self.plugin = self.project / "installed-plugin"
        self.plugin.mkdir()
        self.bundled = self.plugin / ".mcp.json"
        self.bundled.write_text(
            '{"mcpServers":{"unreal-mcp":{"url":"http://127.0.0.1:8000/mcp"}}}',
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def inspect(self, **overrides):
        arguments = {
            "client_configs": [self.client],
            "log_path": self.log,
            "netstat_text": self.netstat,
            "process_name_lookup": lambda _pid: "UnrealEditor.exe",
            "script_path": self.plugin / "skills/unreal-mcp/scripts/check_endpoint.py",
        }
        arguments.update(overrides)
        return MODULE.inspect_endpoint(self.project, **arguments)

    def test_matching_runtime_evidence_passes_but_keeps_mutation_gate_pending(self):
        result = self.inspect()
        self.assertEqual("PASS", result["runtime_endpoint_verdict"])
        self.assertEqual("PENDING_LIST_TOOLSETS", result["mutation_gate"])
        self.assertEqual(4242, result["listener_owner"]["pid"])
        self.assertTrue(result["unreal_settings"]["config_path"].endswith(".ini"))
        self.assertEqual("/mcp", result["unreal_settings"]["path"])
        self.assertIn("list_toolsets", result["next_required_check"])

    def test_client_and_unreal_setting_port_mismatch_blocks(self):
        ini = (
            self.project
            / "Saved"
            / "Config"
            / "WindowsEditor"
            / "EditorPerProjectUserSettings.ini"
        )
        ini.write_text(
            "[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]\n"
            "ServerUrlPath=/mcp\nServerPortNumber=8000\nbAutoStartServer=True\n",
            encoding="utf-8",
        )
        result = self.inspect()
        self.assertEqual("FAIL", result["runtime_endpoint_verdict"])
        self.assertTrue(any("does not match client port" in item for item in result["errors"]))

    def test_wrong_latest_log_port_blocks(self):
        self.log.write_text(
            "LogModelContextProtocol: Starting MCP server on port 8000\n"
            "LogHttpListener: Created new HttpListener on 127.0.0.1:8000\n",
            encoding="utf-8",
        )
        result = self.inspect()
        self.assertEqual("FAIL", result["runtime_endpoint_verdict"])
        self.assertTrue(any("Latest log start port 8000" in item for item in result["errors"]))

    def test_non_unreal_listener_owner_blocks(self):
        result = self.inspect(process_name_lookup=lambda _pid: "python.exe")
        self.assertEqual("FAIL", result["runtime_endpoint_verdict"])
        self.assertTrue(any("not UnrealEditor" in item for item in result["errors"]))

    def test_disagreeing_client_configs_block(self):
        second = self.project / "other.mcp.json"
        second.write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "unreal-mcp": {"url": "http://127.0.0.1:8000/mcp"}
                    }
                }
            ),
            encoding="utf-8",
        )
        result = self.inspect(client_configs=[self.client, second])
        self.assertEqual("FAIL", result["runtime_endpoint_verdict"])
        self.assertTrue(any("disagree" in item for item in result["errors"]))

    def test_workspace_toml_overrides_project_json_and_bundled_default(self):
        self.client.write_bytes(self.bundled.read_bytes())
        self.workspace_config.write_text(
            '[plugins."unreal-editor-skills-for-codex@personal".mcp_servers.unreal-mcp]\n'
            'enabled = false\n[mcp_servers.unreal-mcp]\nurl = "http://127.0.0.1:8008/mcp"\n',
            encoding="utf-8",
        )
        result = self.inspect(client_configs=None)
        self.assertEqual("PASS", result["runtime_endpoint_verdict"])
        self.assertEqual(str(self.workspace_config), result["client_configs"][0]["path"])
        self.assertEqual("PENDING_LIST_TOOLSETS", result["mutation_gate"])

    def test_toml_without_unreal_falls_back_to_project_json(self):
        self.workspace_config.write_text(
            '[mcp_servers.other]\nurl = "http://127.0.0.1:9000/mcp"', encoding="utf-8"
        )
        result = self.inspect(client_configs=None)
        self.assertEqual("PASS", result["runtime_endpoint_verdict"])
        self.assertEqual(str(self.client), result["client_configs"][-1]["path"])
        self.assertNotIn("9000", json.dumps(result))

    def test_bundled_endpoint_used_when_project_has_no_unreal_config(self):
        self.bundled.write_bytes(self.client.read_bytes())
        self.client.unlink()
        result = self.inspect(client_configs=None)
        self.assertEqual("PASS", result["runtime_endpoint_verdict"])
        self.assertEqual(str(self.bundled), result["client_configs"][-1]["path"])

    def test_disabled_direct_and_proxy_entries_cannot_fall_through_to_http(self):
        for config in (
            '[mcp_servers.unreal-mcp]\nenabled = false\nurl = "http://127.0.0.1:8008/mcp"',
            '[plugins."unreal-editor-skills-for-codex@personal".mcp_servers.unreal-mcp]\nenabled = false',
            '[mcp_servers.unreal-mcp-proxy]\ncommand = "proxy"',
        ):
            with self.subTest(config=config):
                self.workspace_config.write_text(config, encoding="utf-8")
                result = self.inspect(client_configs=None)
                self.assertIsNone(result["client_url"])
                self.assertEqual("BLOCKED", result["mutation_gate"])

    def test_proxy_installer_metadata_is_not_a_direct_connection(self):
        proxy = {"command": "proxy", "_upstreamEntry": {"url": "http://127.0.0.1:8008/mcp"}}
        self.client.write_text(json.dumps({"mcpServers": {"unreal-mcp-proxy": proxy}}))
        result = self.inspect()
        self.assertIsNone(result["client_url"])
        self.assertEqual("BLOCKED", result["mutation_gate"])

    def test_renamed_server_requires_explicit_selection(self):
        self.client.write_text(
            '{"mcpServers":{"my-editor":{"url":"http://127.0.0.1:8008/mcp"}}}',
            encoding="utf-8",
        )
        self.assertEqual("BLOCKED", self.inspect()["mutation_gate"])
        self.assertEqual("PASS", self.inspect(server_name="my-editor")["runtime_endpoint_verdict"])

    def test_minimal_auto_start_ini_uses_documented_engine_defaults(self):
        self.client.write_bytes(self.bundled.read_bytes())
        ini = self.project / "Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini"
        ini.write_text(f"[{MODULE.SETTINGS_SECTION}]\nbAutoStartServer=True\n", encoding="utf-8")
        self.log.write_text(self.log.read_text().replace("8008", "8000"), encoding="utf-8")
        result = self.inspect(netstat_text=self.netstat.replace("8008", "8000"))
        self.assertEqual("PASS", result["runtime_endpoint_verdict"])
        self.assertEqual(8000, result["unreal_settings"]["port"])
        self.assertEqual("/mcp", result["unreal_settings"]["path"])

    def test_ambiguous_listener_ownership_blocks(self):
        result = self.inspect(netstat_text=self.netstat + self.netstat.replace("4242", "4243"))
        self.assertEqual("BLOCKED", result["mutation_gate"])

    def test_launch_port_overrides_saved_value_and_still_needs_matching_listener(self):
        ini = self.project / "Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini"
        ini.write_text(f"[{MODULE.SETTINGS_SECTION}]\nbAutoStartServer=True\n", encoding="utf-8")
        startup = self.log.read_text()
        self.log.write_text("LogInit: Command Line: -ModelContextProtocolPort=8008\n" + startup)
        result = self.inspect()
        self.assertEqual(8000, result["unreal_settings"]["port"])
        self.assertEqual([8008], result["unreal_log"]["launch_ports"])
        self.assertEqual("PASS", result["runtime_endpoint_verdict"])
        self.assertEqual("BLOCKED", self.inspect(netstat_text="")["mutation_gate"])
        ini.unlink()
        self.assertEqual("PASS", self.inspect()["runtime_endpoint_verdict"])
        with self.log.open("a") as log:
            log.write("LogInit: Command Line: -log\n")
        self.assertEqual("BLOCKED", self.inspect()["mutation_gate"])


if __name__ == "__main__":
    unittest.main()
