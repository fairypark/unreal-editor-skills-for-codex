import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "environment-level-design"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "install_production_asset_templates.py"


def load_installer():
    spec = importlib.util.spec_from_file_location("production_asset_installer", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProductionAssetTemplateTests(unittest.TestCase):
    def setUp(self):
        self.installer = load_installer()
        self.asset_root = SKILL_ROOT / "assets" / "production-assets"

    def test_bundled_json_contracts_are_dependency_free(self):
        for name in self.installer.TEMPLATE_NAMES:
            with (self.asset_root / name).open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            self.assertEqual(payload["schema_version"], 1)
            serialized = json.dumps(payload)
            self.assertNotIn("/Game/JoseonMoonlitFestivalGarden", serialized)
            self.assertNotIn("Seyeonjeong", serialized)

    def test_installer_writes_all_templates_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            result = self.installer.install(root)
            self.assertEqual(result["status"], "INSTALLED")
            self.assertEqual(len(result["installed"]), 3)
            for path in result["installed"]:
                self.assertTrue(Path(path).is_file())
            with self.assertRaises(FileExistsError):
                self.installer.install(root)

    def test_force_mode_reports_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.installer.install(root)
            result = self.installer.install(root, force=True)
            self.assertTrue(result["overwrote_existing"])


if __name__ == "__main__":
    unittest.main()
