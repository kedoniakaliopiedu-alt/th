#!/usr/bin/env python3
"""Третий OCR-движок: Thai-TrOCR — модель уровня СТРОКИ для тайского рукописного.

В отличие от Vision и Typhoon, эта модель принимает одну вырезанную строку и выдаёт
её текст. Идеально ложится на вывод `thaiocr lines`. Маленькая (~103M), идёт на CPU/MPS
без GPU. Работает офлайн после первой загрузки весов (кэш ~/.cache/huggingface).

    scripts/.venv/bin/python trocr.py строка.png          # одна строка
    scripts/.venv/bin/python trocr.py --dir /tmp/th       # все line-*.png
    scripts/.venv/bin/python trocr.py --compare /tmp/th   # Vision (lines.json) vs TrOCR

Запускать интерпретатором из scripts/.venv — там стоят torch/transformers.
"""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

MODEL = "suchut/thaitrocr-base-handwritten-beta2"

_cache = {}


def load():
    if "model" not in _cache:
        import torch
        from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        dev = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"trocr: загрузка модели на {dev}…", file=sys.stderr)
        _cache["proc"] = TrOCRProcessor.from_pretrained(MODEL)
        _cache["model"] = VisionEncoderDecoderModel.from_pretrained(MODEL).to(dev).eval()
        _cache["torch"] = torch
        _cache["dev"] = dev
    return _cache


def to_png(path: Path) -> Path:
    if path.suffix.lower() in {".png", ".jpg", ".jpeg"}:
        return path
    out = Path(tempfile.gettempdir()) / (path.stem + "_trocr.png")
    subprocess.run(["sips", "-s", "format", "png", str(path), "--out", str(out)],
                   check=True, capture_output=True)
    return out


def ocr(path: Path) -> str:
    from PIL import Image
    c = load()
    img = Image.open(to_png(path)).convert("RGB")
    pix = c["proc"](images=img, return_tensors="pt").pixel_values.to(c["dev"])
    with c["torch"].no_grad():
        ids = c["model"].generate(pix, max_new_tokens=128)
    return c["proc"].batch_decode(ids, skip_special_tokens=True)[0].strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image", nargs="?")
    ap.add_argument("--dir")
    ap.add_argument("--compare")
    args = ap.parse_args()

    if args.compare:
        d = Path(args.compare)
        vision = {l["index"]: l.get("vision_text")
                  for l in json.loads((d / "lines.json").read_text())["lines"]}
        for f in sorted(d.glob("line-*.png")):
            idx = int(f.stem.split("-")[1])
            print(f"=== {f.name} ===")
            print(f"  vision: {vision.get(idx)}")
            print(f"  trocr : {ocr(f)}")
        return
    if args.dir:
        for f in sorted(Path(args.dir).glob("line-*.png")):
            print(f"{f.name}: {ocr(f)}")
        return
    if not args.image:
        ap.error("нужен файл, --dir или --compare")
    print(ocr(Path(args.image)))


if __name__ == "__main__":
    main()
