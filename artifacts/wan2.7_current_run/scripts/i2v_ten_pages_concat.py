"""
Generate short wan2.7-i2v clips from local PNGs (base64 data URI), then concat with ffmpeg.
Requires: DASHSCOPE_API_KEY, ffmpeg in PATH, requests.

Does not embed secrets; pass key via environment only.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests

BEIJING_SYNTH = "https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis"
BEIJING_TASK = "https://dashscope.aliyuncs.com/api/v1/tasks/{}"

# Text-first prompts: subtle global motion only; discourage text warping
PROMPT = (
    "技术演示幻灯片风格，整体轻微运镜：可缓慢微推镜头或极轻微的景深呼吸感，"
    "保持画面稳定。画面内所有中文标题、正文、英文术语、框线与箭头必须保持清晰静止，"
    "不得变形、涂抹、替换或生成新文字。光线可有细微变化。"
)

NEGATIVE = (
    "文字变形, 乱码, 错别字, 笔画断裂, 字幕抖动, 替换原有文字, 涂抹文字, "
    "严重手持抖动, 画面撕裂, 多余水印, 无关物体"
)


def png_to_data_uri(png_path: Path) -> str:
    raw = png_path.read_bytes()
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:image/png;base64,{b64}"


def create_task(
    api_key: str,
    data_uri: str,
    duration: int,
    seed: int | None,
    *,
    prompt: str | None = None,
    negative_prompt: str | None = None,
) -> str:
    inp: dict = {
        "prompt": PROMPT if prompt is None else prompt,
        "media": [{"type": "first_frame", "url": data_uri}],
    }
    if negative_prompt is None:
        inp["negative_prompt"] = NEGATIVE
    elif negative_prompt != "":
        inp["negative_prompt"] = negative_prompt
    body: dict = {
        "model": "wan2.7-i2v",
        "input": inp,
        "parameters": {
            "resolution": "1080P",
            "duration": duration,
            "prompt_extend": False,
            "watermark": False,
        },
    }
    if seed is not None:
        body["parameters"]["seed"] = seed

    r = requests.post(
        BEIJING_SYNTH,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        },
        json=body,
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"create_task HTTP {r.status_code}: {r.text[:2000]}")
    out = r.json()
    if out.get("code"):
        raise RuntimeError(f"create_task API error: {json.dumps(out, ensure_ascii=False)[:2000]}")
    task_id = out.get("output", {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"no task_id: {out}")
    return task_id


def poll_task(api_key: str, task_id: str, timeout_s: int = 900) -> dict:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        r = requests.get(
            BEIJING_TASK.format(task_id),
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60,
        )
        r.raise_for_status()
        data = r.json()
        out = data.get("output", {})
        st = out.get("task_status")
        if st == "SUCCEEDED":
            return out
        if st == "FAILED":
            raise RuntimeError(f"task failed: {json.dumps(out, ensure_ascii=False)}")
        if st == "UNKNOWN":
            raise RuntimeError(f"task unknown: {out}")
        time.sleep(15)
    raise TimeoutError(f"poll timeout for {task_id}")


def download(url: str, dest: Path) -> None:
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    dest.write_bytes(r.content)


MINIMAL_PROMPT = "缓慢微推镜头，画面稳定，光线轻微变化，保持幻灯片内容清晰。"


def run_one_i2v(
    api_key: str, index: int, name: str, png_path: Path, duration: int, out_dir: Path
) -> tuple[Path, dict]:
    data_uri = png_to_data_uri(png_path)
    task_id = create_task(api_key, data_uri, duration, 10000 + index)
    out = poll_task(api_key, task_id)
    vurl = out.get("video_url")
    if not vurl:
        raise RuntimeError(f"no video_url: {out}")
    clip_path = out_dir / f"clip_{index:02d}_{Path(name).stem}.mp4"
    download(vurl, clip_path)
    return clip_path, {
        "page": name,
        "mode": "wan2.7-i2v",
        "task_id": task_id,
        "video_url": vurl,
    }


def run_one_i2v_minimal(
    api_key: str, index: int, name: str, png_path: Path, duration: int, out_dir: Path
) -> tuple[Path, dict]:
    data_uri = png_to_data_uri(png_path)
    task_id = create_task(
        api_key,
        data_uri,
        duration,
        20000 + index,
        prompt=MINIMAL_PROMPT,
        negative_prompt="",
    )
    out = poll_task(api_key, task_id)
    vurl = out.get("video_url")
    if not vurl:
        raise RuntimeError(f"no video_url: {out}")
    clip_path = out_dir / f"clip_{index:02d}_{Path(name).stem}_minimal.mp4"
    download(vurl, clip_path)
    return clip_path, {
        "page": name,
        "mode": "wan2.7-i2v-minimal",
        "task_id": task_id,
        "video_url": vurl,
    }


def run_one_static(
    index: int, name: str, png_path: Path, duration: int, out_dir: Path
) -> tuple[Path, dict]:
    clip_path = out_dir / f"clip_{index:02d}_{Path(name).stem}_static.mp4"
    ffmpeg_static_from_png(png_path, duration, clip_path)
    return clip_path, {
        "page": name,
        "mode": "ffmpeg_static_fallback",
        "reason": "i2v_failed_or_moderation",
    }


def ffmpeg_static_from_png(png_path: Path, duration: int, out_mp4: Path) -> None:
    """Fallback: lossless text — no model motion, 2s still clip."""
    cmd = [
        "ffmpeg",
        "-y",
        "-loop",
        "1",
        "-i",
        str(png_path),
        "-t",
        str(duration),
        "-vf",
        "format=yuv420p",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True)


def ffmpeg_concat(parts: list[Path], out_mp4: Path) -> None:
    lst = out_mp4.with_suffix(".ffconcat")
    lines = ["ffconcat version 1.0"]
    for p in parts:
        # ffmpeg on Windows accepts forward slashes in concat file
        lines.append(f"file '{p.resolve().as_posix()}'")
    lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # Re-encode so i2v clips and static PNG clips always merge (avoid -c copy size/params mismatch).
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(lst),
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        str(out_mp4),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    api_key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not api_key:
        print("Set DASHSCOPE_API_KEY", file=sys.stderr)
        return 1

    root = Path(__file__).resolve().parents[1]
    img_dir = root / "output" / "visuals" / "images"
    order = [
        "page_1_opening.png",
        "page_2_wan27_lead.png",
        "page_3_copaw_orchestrator.png",
        "page_4_business_pain.png",
        "page_5_capability_response.png",
        "page_6_layering.png",
        "page_7_main_proof.png",
        "page_8_execution_flow.png",
        "page_9_agentscope_ecosystem_reuse.png",
        "page_10_closing.png",
    ]
    for name in order:
        p = img_dir / name
        if not p.exists():
            print(f"missing: {p}", file=sys.stderr)
            return 1

    out_dir = root / "output" / "videos" / "i2v_ten_concat"
    out_dir.mkdir(parents=True, exist_ok=True)
    clips: list[Path] = []

    # Short duration per clip to limit cumulative text drift; min API duration is 2
    duration = 2
    meta_log = []

    for i, name in enumerate(order, start=1):
        png_path = img_dir / name
        print(f"[{i}/10] encoding {name} ...", flush=True)
        print(f"[{i}/10] creating task (duration={duration}s) ...", flush=True)
        clip_path: Path | None = None
        meta: dict = {}
        try:
            clip_path, meta = run_one_i2v(api_key, i, name, png_path, duration, out_dir)
            print(f"[{i}/10] i2v ok", flush=True)
        except Exception as e1:
            print(f"[{i}/10] i2v failed ({e1}); retry minimal prompt ...", flush=True)
            try:
                clip_path, meta = run_one_i2v_minimal(api_key, i, name, png_path, duration, out_dir)
                print(f"[{i}/10] i2v minimal ok", flush=True)
            except Exception as e2:
                print(f"[{i}/10] minimal i2v failed ({e2}); ffmpeg static fallback ...", flush=True)
                clip_path, meta = run_one_static(i, name, png_path, duration, out_dir)
        clips.append(clip_path)
        meta["clip"] = str(clip_path)
        meta_log.append(meta)

    (out_dir / "clips_meta.json").write_text(
        json.dumps(meta_log, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    final = out_dir / "wan27_i2v_10pages_concat.mp4"
    print("concat with ffmpeg ...", flush=True)
    ffmpeg_concat(clips, final)
    print("done:", final)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
