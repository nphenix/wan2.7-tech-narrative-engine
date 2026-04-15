import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT.parent.parent


class VisualBlueprintSkillContractTest(unittest.TestCase):
    def test_skill_md_thin_guardrails_and_designer(self) -> None:
        skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("设计师", skill_md)
        self.assertIn("硬边界", skill_md)
        self.assertIn("PAGE_DEFINITIONS", skill_md)
        self.assertIn("user-excalidraw", skill_md)
        self.assertIn("export_diagram", skill_md)
        self.assertIn("start_session", skill_md)
        self.assertIn("浏览器", skill_md)
        self.assertIn("add_elements", skill_md)
        self.assertIn("page_contracts.md", skill_md)
        self.assertIn("diagram_blueprints.md", skill_md)
        self.assertIn("page_visual_specs.md", skill_md)
        self.assertIn("runtime/runner.py", skill_md)
        self.assertIn("SKILL.md", skill_md)
        self.assertIn("startBinding", skill_md)
        self.assertIn("endBinding", skill_md)
        self.assertIn("label", skill_md)
        self.assertIn("不出框", skill_md)

    def test_visual_blueprint_skill_has_no_runtime_source(self) -> None:
        self.assertFalse((ROOT / "runtime" / "runner.py").exists())
        self.assertFalse((ROOT / "runtime" / "__init__.py").exists())

    def test_pipeline_page_ids_mentioned(self) -> None:
        skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("page_1_opening", skill_md)
        self.assertIn("pipeline.py", skill_md)
        self.assertIn("11", skill_md)

    def test_check_visual_blueprint_export_script_smoke(self) -> None:
        script = ENGINE_ROOT / "scripts" / "check_visual_blueprint_export.py"
        self.assertTrue(script.is_file(), msg=f"缺少校验脚本：{script}")

        if str(ENGINE_ROOT) not in sys.path:
            sys.path.insert(0, str(ENGINE_ROOT))
        from common.pipeline import PAGE_DEFINITIONS  # noqa: E402

        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp)
            images_dir = task_dir / "output" / "blueprints" / "images"
            images_dir.mkdir(parents=True, exist_ok=True)
            svg_body = (
                b'<?xml version="1.0" encoding="UTF-8"?>'
                b'<svg xmlns="http://www.w3.org/2000/svg">'
                + b"x" * 900
                + b"</svg>"
            )
            bundle_pages: list[dict[str, str]] = []
            for page in PAGE_DEFINITIONS:
                page_id = page["page_id"]
                (images_dir / f"{page_id}.svg").write_bytes(svg_body)
                bundle_pages.append(
                    {
                        "page_id": page_id,
                        "title": page["title"],
                        "svg_path": f"output/blueprints/images/{page_id}.svg",
                    }
                )

            bundle = {"page_count": len(bundle_pages), "pages": bundle_pages}
            bundle_path = task_dir / "output" / "blueprints" / "visual_blueprint_bundle.json"
            bundle_path.write_text(
                json.dumps(bundle, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [sys.executable, str(script), str(task_dir)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"stderr={proc.stderr!r} stdout={proc.stdout!r}",
            )


if __name__ == "__main__":
    unittest.main()
