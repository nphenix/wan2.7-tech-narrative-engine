import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class SkillLayoutTest(unittest.TestCase):
    def test_skills_do_not_expose_run_scripts(self) -> None:
        skill_dirs = sorted(path.parent for path in (PROJECT_ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(6, len(skill_dirs))
        for skill_dir in skill_dirs:
            self.assertFalse((skill_dir / "scripts" / "run.py").exists(), str(skill_dir))
            self.assertFalse((skill_dir / "scripts" / "run.ps1").exists(), str(skill_dir))

    def test_skills_use_natural_language_entry_in_skill_md(self) -> None:
        for skill_md in sorted((PROJECT_ROOT / "skills").glob("*/SKILL.md")):
            content = skill_md.read_text(encoding="utf-8")
            self.assertIn("自然语言", content, str(skill_md))
            self.assertNotIn("entry_script", content, str(skill_md))
            self.assertNotIn("scripts/run.py", content, str(skill_md))


if __name__ == "__main__":
    unittest.main()
