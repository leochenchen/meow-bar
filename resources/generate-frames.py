#!/usr/bin/env python3
"""
MeowBar Line Art Cat Frame Generator v5
Clean line-drawing style using PIL drawing primitives.
44x44 (@2x for 22x22 logical).

States: idle (white), working (green), complete (gold), error (red).
"""

import os
import math
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "app", "MeowBar", "Resources", "Frames")
os.makedirs(OUTPUT_DIR, exist_ok=True)

SIZE = 44  # 44x44 @2x for 22x22 logical
LINE_WIDTH = 2


def new_frame():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    return img, draw


def save_frame(img, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    img.save(path)
    print(f"  {name}.png")


# ============================================================
# Common cat parts
# ============================================================

def draw_ear_left(draw, x, y, color, w=LINE_WIDTH):
    """Triangular left ear."""
    draw.line([(x, y+8), (x+4, y), (x+8, y+8)], fill=color, width=w)


def draw_ear_right(draw, x, y, color, w=LINE_WIDTH):
    """Triangular right ear."""
    draw.line([(x, y+8), (x+4, y), (x+8, y+8)], fill=color, width=w)


def draw_head(draw, cx, cy, rx, ry, color, w=LINE_WIDTH):
    """Oval head outline."""
    draw.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], outline=color, width=w)


def draw_eye(draw, x, y, r, color, w=LINE_WIDTH):
    """Small circle eye."""
    draw.ellipse([x-r, y-r, x+r, y+r], fill=color)


def draw_closed_eye(draw, x, y, color, w=LINE_WIDTH):
    """Happy closed eye (arc)."""
    draw.arc([x-3, y-3, x+3, y+3], 0, 180, fill=color, width=w)


def draw_whiskers(draw, cx, cy, color, flip=False, w=1):
    """Three whiskers on one side."""
    d = -1 if flip else 1
    draw.line([(cx, cy), (cx + d*10, cy - 3)], fill=color, width=w)
    draw.line([(cx, cy), (cx + d*10, cy + 1)], fill=color, width=w)
    draw.line([(cx, cy), (cx + d*9, cy + 4)], fill=color, width=w)


def draw_nose(draw, x, y, color, w=LINE_WIDTH):
    """Tiny triangle nose."""
    draw.polygon([(x, y-1), (x-2, y+2), (x+2, y+2)], outline=color)


# ============================================================
# Shared: head-tilting cat (used for idle + waiting)
# ============================================================
def draw_tilting_cat(draw, tilt, color):
    """Front-facing cat tilting head. tilt: -1=left, 0=center, 1=right."""
    hx = tilt * 3
    hy = abs(tilt) * 1

    # Ears
    draw.line([(8+hx, 16+hy), (12+hx, 5+hy), (17+hx, 14+hy)],
              fill=color, width=LINE_WIDTH)
    draw.line([(27+hx, 14+hy), (32+hx, 5+hy), (36+hx, 16+hy)],
              fill=color, width=LINE_WIDTH)

    # Head
    draw.ellipse([9+hx, 12+hy, 35+hx, 29+hy], outline=color, width=LINE_WIDTH)

    # Eyes
    draw_eye(draw, 17+hx, 20+hy, 2, color)
    draw_eye(draw, 27+hx, 20+hy, 2, color)

    # Nose
    draw_nose(draw, 22+hx, 23+hy, color)

    # Mouth
    draw.arc([18+hx, 24+hy, 22+hx, 27+hy], 0, 180, fill=color, width=1)
    draw.arc([22+hx, 24+hy, 26+hx, 27+hy], 0, 180, fill=color, width=1)

    # Whiskers
    draw_whiskers(draw, 13+hx, 23+hy, color, flip=True, w=1)
    draw_whiskers(draw, 31+hx, 23+hy, color, flip=False, w=1)

    # Body
    draw.arc([8, 26, 36, 42], 0, 180, fill=color, width=LINE_WIDTH)
    draw.line([(8, 34), (8, 28)], fill=color, width=LINE_WIDTH)
    draw.line([(36, 34), (36, 28)], fill=color, width=LINE_WIDTH)

    # Paws
    draw.line([(15, 37), (15, 42)], fill=color, width=LINE_WIDTH)
    draw.line([(15, 42), (18, 42)], fill=color, width=LINE_WIDTH)
    draw.line([(29, 37), (29, 42)], fill=color, width=LINE_WIDTH)
    draw.line([(29, 42), (26, 42)], fill=color, width=LINE_WIDTH)

    # Tail
    draw.arc([33, 28, 43, 38], 270, 360, fill=color, width=LINE_WIDTH)


# ============================================================
# IDLE: White cat, head tilting
# ============================================================
def generate_idle():
    color = (255, 255, 255, 255)
    print("idle (white head tilt):")
    tilts = [0, 1, 0, -1]
    for i, t in enumerate(tilts):
        img, draw = new_frame()
        draw_tilting_cat(draw, t, color)
        save_frame(img, f"idle-{i}")


# ============================================================
# WAITING: Yellow cat, head tilting (waiting for user input)
# ============================================================
def generate_waiting():
    color = (220, 190, 60, 255)  # Yellow/gold
    print("waiting (yellow head tilt):")
    tilts = [0, 1, 0, -1]
    for i, t in enumerate(tilts):
        img, draw = new_frame()
        draw_tilting_cat(draw, t, color)
        save_frame(img, f"waiting-{i}")


# ============================================================
# WORKING: Cat with green solid ball (green)
# ============================================================
def generate_working():
    color = (80, 200, 120, 255)
    ball_color = (80, 200, 120, 255)
    print("working (green ball):")

    def draw_working_cat(draw, ball_phase):
        """Front-facing cat with a green ball floating nearby."""

        # Ears
        draw.line([(8, 18), (12, 8), (17, 16)], fill=color, width=LINE_WIDTH)
        draw.line([(27, 16), (32, 8), (36, 18)], fill=color, width=LINE_WIDTH)

        # Head
        draw.ellipse([9, 14, 35, 30], outline=color, width=LINE_WIDTH)

        # Eyes (open, looking at ball)
        draw_eye(draw, 17, 22, 2, color)
        draw_eye(draw, 27, 22, 2, color)

        # Nose
        draw_nose(draw, 22, 25, color)

        # Mouth (tiny w)
        draw.arc([18, 26, 22, 29], 0, 180, fill=color, width=1)
        draw.arc([22, 26, 26, 29], 0, 180, fill=color, width=1)

        # Whiskers
        draw_whiskers(draw, 13, 25, color, flip=True, w=1)
        draw_whiskers(draw, 31, 25, color, flip=False, w=1)

        # Body
        draw.arc([8, 28, 36, 43], 0, 180, fill=color, width=LINE_WIDTH)
        draw.line([(8, 36), (8, 30)], fill=color, width=LINE_WIDTH)
        draw.line([(36, 36), (36, 30)], fill=color, width=LINE_WIDTH)

        # Paws
        draw.line([(15, 37), (15, 42)], fill=color, width=LINE_WIDTH)
        draw.line([(15, 42), (13, 42)], fill=color, width=LINE_WIDTH)
        draw.line([(29, 37), (29, 42)], fill=color, width=LINE_WIDTH)
        draw.line([(29, 42), (31, 42)], fill=color, width=LINE_WIDTH)

        # Tail
        draw.arc([33, 28, 43, 38], 270, 360, fill=color, width=LINE_WIDTH)

        # Green solid ball - bobbing around top-right
        ball_positions = [
            (39, 6), (38, 4), (39, 3), (40, 4), (39, 6), (38, 5),
        ]
        bx, by = ball_positions[ball_phase]
        draw.ellipse([bx-3, by-3, bx+3, by+3], fill=ball_color)

    for i in range(6):
        img, draw = new_frame()
        draw_working_cat(draw, i)
        save_frame(img, f"running-{i}")


# ============================================================
# COMPLETE: Happy cat (green, same as working)
# ============================================================
def generate_complete():
    color = (80, 200, 120, 255)
    sparkle_color = (80, 200, 120, 140)
    print("complete (celebrating):")

    def draw_happy_cat(draw, tail_phase, sparkle_set):
        # Ears
        draw.line([(10, 16), (14, 6), (18, 14)], fill=color, width=LINE_WIDTH)
        draw.line([(26, 14), (30, 6), (34, 16)], fill=color, width=LINE_WIDTH)

        # Head
        draw.ellipse([10, 12, 34, 28], outline=color, width=LINE_WIDTH)

        # Happy eyes (^_^)
        draw_closed_eye(draw, 17, 20, color, w=LINE_WIDTH)
        draw_closed_eye(draw, 27, 20, color, w=LINE_WIDTH)

        # Smile
        draw.arc([16, 22, 28, 28], 0, 180, fill=color, width=LINE_WIDTH)

        # Whiskers
        draw_whiskers(draw, 14, 23, color, flip=True, w=1)
        draw_whiskers(draw, 30, 23, color, flip=False, w=1)

        # Body
        draw.arc([8, 24, 36, 42], 0, 180, fill=color, width=LINE_WIDTH)
        draw.line([(8, 33), (8, 28)], fill=color, width=LINE_WIDTH)
        draw.line([(36, 33), (36, 28)], fill=color, width=LINE_WIDTH)

        # Legs
        draw.line([(15, 36), (15, 41)], fill=color, width=LINE_WIDTH)
        draw.line([(15, 41), (18, 41)], fill=color, width=LINE_WIDTH)
        draw.line([(29, 36), (29, 41)], fill=color, width=LINE_WIDTH)
        draw.line([(29, 41), (32, 41)], fill=color, width=LINE_WIDTH)

        # Wagging tail
        if tail_phase == 0:
            draw.arc([32, 22, 44, 34], 270, 350, fill=color, width=LINE_WIDTH)
        elif tail_phase == 1:
            draw.arc([34, 20, 44, 32], 260, 340, fill=color, width=LINE_WIDTH)
        elif tail_phase == 2:
            draw.arc([32, 18, 44, 30], 250, 330, fill=color, width=LINE_WIDTH)
        else:
            draw.arc([34, 20, 44, 32], 260, 340, fill=color, width=LINE_WIDTH)

        # Sparkles
        for sx, sy in sparkle_set:
            draw.line([(sx-3, sy), (sx+3, sy)], fill=sparkle_color, width=1)
            draw.line([(sx, sy-3), (sx, sy+3)], fill=sparkle_color, width=1)

    sparkles = [
        [(5, 8), (39, 10)],
        [(3, 12), (41, 6)],
        [(6, 6), (38, 14)],
        [(4, 10), (40, 8)],
    ]

    for i in range(4):
        img, draw = new_frame()
        draw_happy_cat(draw, i, sparkles[i])
        save_frame(img, f"celebrate-{i}")


# ============================================================
# ERROR: Big O_O eyes looking right (red)
# ============================================================
def generate_error():
    color = (220, 80, 80, 255)
    print("error (big eyes):")

    def draw_error_cat(draw, look):
        """Front-facing cat with big O_O eyes, looking right. look=eye shift."""

        # Ears
        draw.line([(8, 18), (12, 8), (17, 16)], fill=color, width=LINE_WIDTH)
        draw.line([(27, 16), (32, 8), (36, 18)], fill=color, width=LINE_WIDTH)

        # Head
        draw.ellipse([9, 14, 35, 30], outline=color, width=LINE_WIDTH)

        # Big O_O eyes (large circles, pupils looking right)
        # Left eye
        draw.ellipse([13, 17, 21, 25], outline=color, width=LINE_WIDTH)
        draw_eye(draw, 18 + look, 21, 2, color)  # pupil shifted right
        # Right eye
        draw.ellipse([23, 17, 31, 25], outline=color, width=LINE_WIDTH)
        draw_eye(draw, 28 + look, 21, 2, color)  # pupil shifted right

        # Nose
        draw_nose(draw, 22, 26, color)

        # Mouth (small o)
        draw.ellipse([20, 27, 24, 30], outline=color, width=1)

        # Body
        draw.arc([8, 28, 36, 43], 0, 180, fill=color, width=LINE_WIDTH)
        draw.line([(8, 36), (8, 30)], fill=color, width=LINE_WIDTH)
        draw.line([(36, 36), (36, 30)], fill=color, width=LINE_WIDTH)

        # Paws
        draw.line([(15, 37), (15, 42)], fill=color, width=LINE_WIDTH)
        draw.line([(15, 42), (13, 42)], fill=color, width=LINE_WIDTH)
        draw.line([(29, 37), (29, 42)], fill=color, width=LINE_WIDTH)
        draw.line([(29, 42), (31, 42)], fill=color, width=LINE_WIDTH)

        # Tail
        draw.arc([33, 28, 43, 38], 270, 360, fill=color, width=LINE_WIDTH)

    # 3 frames: pupils shift right slightly
    looks = [1, 2, 1]
    for i, lk in enumerate(looks):
        img, draw = new_frame()
        draw_error_cat(draw, lk)
        save_frame(img, f"scared-{i}")


# ============================================================
if __name__ == "__main__":
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(OUTPUT_DIR, f))

    print(f"Output: {OUTPUT_DIR}\n")
    generate_idle()
    generate_waiting()
    generate_working()
    generate_complete()
    generate_error()

    total = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")])
    print(f"\nDone! {total} frames.")
