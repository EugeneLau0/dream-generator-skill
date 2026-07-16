#!/usr/bin/env python3
"""Heuristic evaluator for dream-generator outputs.

This script intentionally checks stable, automatable signals only. Use it with
the rubric in references/evaluation.md for fuller review.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PREFACE_PATTERNS = [
    "根据你提供",
    "以下是",
    "这个梦",
    "梦境解析",
    "象征",
    "寓意",
    "Here is",
    "Based on",
]

EXPLICIT_FRAME_PATTERNS = [
    "我梦见",
    "在梦里",
    "醒来前",
    "醒来时",
    "醒来后",
    "I dreamed",
    "in the dream",
    "before I woke",
    "when I woke",
]

SAFETY_PATTERNS = [
    "自杀方法",
    "割腕",
    "上吊",
    "强奸",
    "性侵",
    "未成年色情",
    "详细肢解",
    "suicide method",
    "how to kill",
    "rape",
]

DREAM_LOGIC_MARKERS = [
    "忽然",
    "突然",
    "却",
    "不是",
    "变成",
    "像",
    "仿佛",
    "没有影子",
    "漂",
    "浮",
    "下沉",
    "倒着",
    "重复",
    "不认识",
    "impossible",
    "suddenly",
    "floating",
    "became",
]

SENSORY_MARKERS = [
    "光",
    "雨",
    "声音",
    "气味",
    "冷",
    "热",
    "暖",
    "湿",
    "风",
    "颜色",
    "蓝",
    "红",
    "黑",
    "白",
    "透明",
    "玻璃",
    "沉",
    "轻",
    "light",
    "sound",
    "smell",
    "cold",
    "warm",
    "rain",
    "blue",
]


def read_text(value: str | None, path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return value or ""


def extract_motifs(prompt: str) -> list[str]:
    tail = re.split(r"[:：]", prompt, maxsplit=1)[-1]
    pieces = re.split(r"[、,，;；\n]+", tail)
    motifs = []
    for piece in pieces:
        cleaned = re.sub(r"[\s。.!！?？]+", "", piece)
        cleaned = re.sub(r"^(用|写一个|写|生成|只写梦|不要解释|Generate|from)", "", cleaned, flags=re.I)
        if 1 <= len(cleaned) <= 20:
            motifs.append(cleaned)
    return motifs[:8]


def contains_motif(output: str, motif: str) -> bool:
    if motif in output:
        return True
    if len(motif) >= 3:
        chars = [ch for ch in motif if "\u4e00" <= ch <= "\u9fff"]
        if chars and sum(1 for ch in chars if ch in output) >= max(2, len(chars) - 1):
            return True
    return False


def score_motifs(prompt: str, output: str) -> tuple[int, dict]:
    motifs = extract_motifs(prompt)
    if not motifs:
        return 20, {"motifs": [], "covered": []}
    covered = [motif for motif in motifs if contains_motif(output, motif)]
    return round(20 * len(covered) / len(motifs)), {"motifs": motifs, "covered": covered}


def capped_marker_score(output: str, markers: list[str], max_points: int, needed: int) -> int:
    hits = sum(1 for marker in markers if marker.lower() in output.lower())
    return min(max_points, round(max_points * hits / needed))


def score_output_contract(prompt: str, output: str) -> tuple[int, list[str]]:
    issues = []
    stripped = output.strip()
    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", stripped))

    if not ("我" in stripped or re.search(r"\bI\b", stripped)):
        issues.append("missing first-person signal")
    if any(pattern.lower() in stripped.lower() for pattern in PREFACE_PATTERNS):
        issues.append("contains preface or interpretation")
    if any(pattern.lower() in stripped.lower() for pattern in EXPLICIT_FRAME_PATTERNS):
        issues.append("uses explicit dream/waking frame")
    if re.search(r"^\s*[-*]|\n\s*[-*]", stripped):
        issues.append("uses bullet formatting")

    if "200" in prompt and chinese_chars > 240:
        issues.append("likely exceeds requested short length")
    elif "English" not in prompt and chinese_chars and not (120 <= chinese_chars <= 900):
        issues.append("outside default Chinese length band")

    score = max(0, 15 - 4 * len(issues))
    return score, issues


def score_safety(output: str) -> tuple[int, list[str]]:
    hits = [pattern for pattern in SAFETY_PATTERNS if pattern.lower() in output.lower()]
    return (0 if hits else 15), hits


def evaluate(prompt: str, output: str) -> dict:
    motif_score, motif_detail = score_motifs(prompt, output)
    dream_logic = capped_marker_score(output, DREAM_LOGIC_MARKERS, 20, 5)
    sensory = capped_marker_score(output, SENSORY_MARKERS, 15, 5)
    contract, contract_issues = score_output_contract(prompt, output)
    safety, safety_hits = score_safety(output)

    emotional_arc = 12
    if len(output.strip()) < 80:
        emotional_arc = 6
    elif any(word in output for word in ["最后", "后来", "渐渐", "终于", "只剩", "停在", "remained", "finally"]):
        emotional_arc = 15

    total = motif_score + dream_logic + emotional_arc + sensory + contract + safety
    return {
        "score": total,
        "pass": total >= 80 and safety == 15 and contract >= 12,
        "breakdown": {
            "motif_coverage": motif_score,
            "dream_logic": dream_logic,
            "emotional_arc": emotional_arc,
            "sensory_vividness": sensory,
            "output_contract": contract,
            "safety": safety,
        },
        "details": {
            **motif_detail,
            "contract_issues": contract_issues,
            "safety_hits": safety_hits,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--output")
    parser.add_argument("--output-file")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    prompt = read_text(args.prompt, args.prompt_file)
    output = read_text(args.output, args.output_file)
    if not prompt or not output:
        parser.error("provide prompt/output text or files")

    result = evaluate(prompt, output)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write("\n")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
