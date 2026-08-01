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

    def tearDown(self):
        self.temp_dir.cleanup()

    def inspect(self, **overrides):
        arguments = {
            "client_configs": [self.client],
            "log_path": self.log,
            "netstat_text": self.netstat,
            "process_name_lookup": lambda _pid: "UnrealEditor.exe",
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


if __name__ == "__main__":
    unittest.main()
