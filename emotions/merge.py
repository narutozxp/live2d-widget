#!/usr/bin/env python3
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUT_FILE = BASE_DIR.parent / "owo.json"

# ===== 合并顺序控制 =====
# 为None的时候，emotions目录下的json都会被合并
# ALLOW_LIST = None
ALLOW_LIST = [
    "颜文字", 
    "Emoji"
]

merged = {}

if ALLOW_LIST:
    # 严格按照 ALLOW_LIST 顺序
    files = [BASE_DIR / f"{name}.json" for name in ALLOW_LIST]
else:
    # 默认：按文件名排序
    files = sorted(BASE_DIR.glob("*.json"))

for fp in files:
    if not fp.exists():
        raise SystemExit(f"❌ File not found: {fp}")

    try:
        with fp.open("r", encoding="utf-8") as f:
            merged[fp.stem] = json.load(f)
    except json.JSONDecodeError as e:
        raise SystemExit(f"❌ JSON 解析失败: {fp} (line {e.lineno}, col {e.colno})")
    except OSError as e:
        raise SystemExit(f"❌ 读取文件失败: {fp} - {e}")

with OUT_FILE.open("w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, separators=(",", ":"))

print(f"✅ merged {len(merged)} files -> {OUT_FILE}")
