from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_manifest_matches_skill_name(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        name = re.search(r"^name:\s*(\S+)", skill, re.M).group(1)
        self.assertEqual(manifest["name"], name)
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")

    def test_references_linked_from_skill_exist(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for ref in set(re.findall(r"references/[\w./-]+\.md", skill)):
            self.assertTrue((ROOT / ref).is_file(), ref)

    def test_scripts_show_help(self) -> None:
        for script in sorted((ROOT / "scripts").glob("*.py")):
            result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, f"{script.name}: {result.stderr[-300:]}")


if __name__ == "__main__":
    unittest.main()
