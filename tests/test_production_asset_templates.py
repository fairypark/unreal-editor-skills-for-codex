import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skills" / "environment-level-design"
ASSET_ROOT = SKILL_ROOT / "assets" / "production-assets"
SCRIPT_PATH = SKILL_ROOT / "scripts" / "install_production_asset_templates.py"


def load_installer():
    spec = importlib.util.spec_from_file_location("production_asset_installer", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProductionAssetTemplateTests(unittest.TestCase):
    def test_templates_are_versioned_and_machine_independent(self):
        expected = {
            "ProductionAssetCatalog.template.json",
            "terrain-projected-gravel-route.system.json",
            "clustered-water-vegetation.system.json",
        }
        self.assertEqual(expected, {path.name for path in ASSET_ROOT.iterdir()})
        for path in ASSET_ROOT.iterdir():
            text = path.read_text(encoding="utf-8")
            value = json.loads(text)
            self.assertEqual(1, value["schema_version"])
            self.assertNotIn("C:/Users/", text)
            self.assertNotIn("/Game/", text)

    def test_installer_refuses_overwrite_then_force_replaces(self):
        installer = load_installer()
        with tempfile.TemporaryDirectory() as directory:
            project_root = Path(directory)
            first = installer.install(project_root)
            self.assertEqual("INSTALLED", first["status"])
            self.assertEqual(3, len(first["installed"]))
            self.assertFalse(first["overwrote_existing"])

            with self.assertRaises(FileExistsError):
                installer.install(project_root)

            forced = installer.install(project_root, force=True)
            self.assertTrue(forced["overwrote_existing"])


if __name__ == "__main__":
    unittest.main()
