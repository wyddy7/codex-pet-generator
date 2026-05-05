#!/usr/bin/env python3
"""Validate the mechanical parts of a Codex pet spritesheet.

This cannot prove anatomy is correct. It catches the boring failures that make
the Codex UI drift: wrong dimensions, empty frames, missing alpha, edge contact,
and row-scale instability.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


SHEET_WIDTH = 1536
SHEET_HEIGHT = 1872
COLS = 8
ROWS = 9
FRAME_WIDTH = SHEET_WIDTH // COLS
FRAME_HEIGHT = SHEET_HEIGHT // ROWS


def alpha_bbox(frame: Image.Image) -> tuple[int, int, int, int] | None:
    return frame.getchannel("A").getbbox()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spritesheet", type=Path)
    parser.add_argument("--edge-padding", type=int, default=6)
    parser.add_argument("--max-row-height-drift", type=float, default=0.28)
    args = parser.parse_args()

    image = Image.open(args.spritesheet).convert("RGBA")
    errors: list[str] = []
    warnings: list[str] = []

    if image.size != (SHEET_WIDTH, SHEET_HEIGHT):
        errors.append(
            f"expected {SHEET_WIDTH}x{SHEET_HEIGHT}, got {image.width}x{image.height}"
        )

    for row in range(ROWS):
        heights: list[int] = []
        widths: list[int] = []
        for col in range(COLS):
            left = col * FRAME_WIDTH
            top = row * FRAME_HEIGHT
            frame = image.crop((left, top, left + FRAME_WIDTH, top + FRAME_HEIGHT))
            bbox = alpha_bbox(frame)
            label = f"row {row + 1}, col {col + 1}"
            if bbox is None:
                errors.append(f"{label}: empty frame")
                continue

            x0, y0, x1, y1 = bbox
            widths.append(x1 - x0)
            heights.append(y1 - y0)

            if (
                x0 < args.edge_padding
                or y0 < args.edge_padding
                or FRAME_WIDTH - x1 < args.edge_padding
                or FRAME_HEIGHT - y1 < args.edge_padding
            ):
                warnings.append(f"{label}: sprite is close to the cell edge {bbox}")

        if heights:
            min_h = min(heights)
            max_h = max(heights)
            if min_h > 0 and (max_h - min_h) / min_h > args.max_row_height_drift:
                warnings.append(
                    f"row {row + 1}: frame height drift is high "
                    f"(min={min_h}, max={max_h})"
                )

        if widths:
            min_w = min(widths)
            max_w = max(widths)
            if min_w > 0 and (max_w - min_w) / min_w > 0.5:
                warnings.append(
                    f"row {row + 1}: frame width drift is high "
                    f"(min={min_w}, max={max_w})"
                )

    if errors:
        print("ERRORS")
        for error in errors:
            print(f"- {error}")
    if warnings:
        print("WARNINGS")
        for warning in warnings:
            print(f"- {warning}")

    if not errors and not warnings:
        print("OK")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

