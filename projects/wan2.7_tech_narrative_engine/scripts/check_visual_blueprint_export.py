#!/usr/bin/env python3
"""校验任务目录下 visual_blueprint_bundle 与每页 SVG 落盘（不调用 MCP）。

从仓库根执行示例：
  python projects/wan2.7_tech_narrative_engine/scripts/check_visual_blueprint_export.py <任务目录>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _engine_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_pipeline_page_ids() -> list[str]:
    root = _engine_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from common import pipeline  # noqa: E402

    return [page["page_id"] for page in pipeline.PAGE_DEFINITIONS]


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 visual_blueprint_bundle 与 SVG 导出")
    parser.add_argument(
        "task_dir",
        type=Path,
        help="任务根目录（含 output/blueprints/visual_blueprint_bundle.json）",
    )
    args = parser.parse_args()
    task_dir: Path = args.task_dir.resolve()

    bundle_path = task_dir / "output" / "blueprints" / "visual_blueprint_bundle.json"
    if not bundle_path.is_file():
        _fail(f"缺少 bundle 文件：{bundle_path}")
        return 1

    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _fail(f"bundle JSON 解析失败：{bundle_path}\n{exc}")
        return 1

    pages = bundle.get("pages")
    if not isinstance(pages, list) or not pages:
        _fail("bundle 中缺少非空 pages 数组")
        return 1

    expected_ids = _load_pipeline_page_ids()
    got_ids = [p.get("page_id") for p in pages if isinstance(p, dict)]
    if len(got_ids) != len(expected_ids):
        _fail(
            f"页数量不一致：pipeline 为 {len(expected_ids)}，bundle 为 {len(got_ids)}"
        )
        return 1

    missing = [pid for pid in expected_ids if pid not in got_ids]
    extra = [pid for pid in got_ids if pid not in expected_ids]
    if missing or extra:
        _fail(f"page_id 集合与 pipeline 不一致。缺失：{missing}；多余：{extra}")
        return 1

    if got_ids != expected_ids:
        print(
            "提示：bundle 中 pages 顺序与 pipeline PAGE_DEFINITIONS 不一致（集合正确）。",
            file=sys.stderr,
        )

    min_svg_bytes = 800
    rc = 0
    for entry in pages:
        if not isinstance(entry, dict):
            _fail("pages 中存在非对象项")
            return 1
        page_id = entry.get("page_id")
        svg_rel = entry.get("svg_path")
        if not svg_rel:
            _fail(f"{page_id}: 缺少 svg_path")
            return 1
        svg_path = (task_dir / svg_rel).resolve()
        if not svg_path.is_file():
            _fail(f"{page_id}: SVG 不存在：{svg_path}")
            return 1
        size = svg_path.stat().st_size
        if size < min_svg_bytes:
            print(
                f"警告：{page_id} SVG 仅 {size} 字节，可能为占位或未完整导出（阈值 {min_svg_bytes}）。",
                file=sys.stderr,
            )
            rc = rc or 0
        head = svg_path.read_bytes()[:8000]
        if b"<svg" not in head and b"<SVG" not in head:
            _fail(f"{page_id}: 文件不像 SVG（前 8KB 内缺少 <svg 标记）")
            return 1

    return rc


if __name__ == "__main__":
    raise SystemExit(main())
