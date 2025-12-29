#!/usr/bin/env python3
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUT_FILE = BASE_DIR.parent / "owo.json"

# ===== 合并顺序控制 =====
# 为 None 时：合并 emotion 目录下所有 .json（按文件名排序）
# 为 list 时：严格按 list 顺序合并（按名字去找同名 .json）
ALLOW_LIST = [
    "颜文字",
    "Emoji",
    "qq",
    "贴吧",
    "bilibili动态小电视",
    "bilibili小电视",
    "2233娘",
    "bilibili热词",
    "微博",
    "钉钉",
    "Heybox",
    "Tsuri-me-ju_mimi",
    "Yurui-Neko",
    "Sweetie-Bunny",
    "Menhera-chan",
    "Snow-Miku",
    "Arcaea",
    "Mafumafu",
    "Marup",
    "酷安",
    "嗷大喵",
    "魔女之旅",
    "阿狸",
    "兔斯基",
    "滑稽",
    "罗小黑",
    "那兔"
]
# ALLOW_LIST = None

merged = {}

if ALLOW_LIST:
    files = [BASE_DIR / f"{name}.json" for name in ALLOW_LIST]
else:
    files = sorted(BASE_DIR.glob("*.json"))

for fp in files:
    if not fp.exists():
        raise SystemExit(f"❌ File not found: {fp}")

    try:
        with fp.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(f"❌ JSON 解析失败: {fp} (line {e.lineno}, col {e.colno})")
    except OSError as e:
        raise SystemExit(f"❌ 读取文件失败: {fp} - {e}")

    if not isinstance(data, dict):
        raise SystemExit(f"❌ JSON 顶层必须是 object/dict: {fp}")

    # 直接摊平合并：后面的文件会覆盖前面同名 key
    merged.update(data)

with OUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, separators=(",", ":"))

print(f"✅ merged {len(files)} files, total keys={len(merged)} -> {OUT_FILE}")
