#!/usr/bin/env python3
"""
MeowBar Pixel Cat Frame Generator
Generates 44x44 (@2x for 22x22 logical) colored pixel art cat PNGs.
4 states: idle (white), working (green), complete (gold), error (red).

Usage: pip install Pillow && python generate-frames.py
"""

import os
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "app", "MeowBar", "Resources", "Frames")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 22x22 logical grid, each cell = 2px -> 44x44 output
GRID = 22
SCALE = 2
SIZE = GRID * SCALE


def create_frame(pixels, color, bg=(0, 0, 0, 0)):
    img = Image.new("RGBA", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(img)
    for x, y in pixels:
        if 0 <= x < GRID and 0 <= y < GRID:
            draw.rectangle(
                [x * SCALE, y * SCALE, (x + 1) * SCALE - 1, (y + 1) * SCALE - 1],
                fill=color,
            )
    return img


def save_frame(img, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    img.save(path)
    print(f"  {name}.png")


# ============================================================
# IDLE: Sleeping curled-up cat (white)
# ============================================================
def generate_idle():
    color = (230, 230, 235, 255)  # Clean white
    zzz_color = (180, 180, 190, 180)
    print("idle (sleeping):")

    def sleeping_body():
        px = []
        # Curled body - round oval
        for x in range(5, 17):
            px.append((x, 12))
            px.append((x, 17))
        for y in range(12, 18):
            px.append((5, y))
            px.append((16, y))
        for y in range(13, 17):
            for x in range(6, 16):
                px.append((x, y))
        # Head tucked
        for x in range(6, 11):
            px.append((x, 11))
        px += [(6, 10), (7, 10), (8, 10)]
        # Ear
        px += [(6, 9), (7, 9), (6, 8)]
        # Closed eye (line)
        px += [(8, 11), (9, 11)]
        return px

    tails = [
        [(16, 16), (17, 15), (18, 14)],
        [(16, 16), (17, 16), (18, 15)],
        [(16, 16), (17, 17), (18, 16)],
        [(16, 16), (17, 16), (18, 15)],
    ]

    zzz = [
        [(12, 7)],
        [(12, 7), (13, 6)],
        [(12, 7), (13, 6), (14, 5)],
        [(13, 6), (14, 5)],
    ]

    base = sleeping_body()
    for i in range(4):
        img = create_frame(base + tails[i], color)
        img = Image.alpha_composite(img, create_frame(zzz[i], zzz_color))
        save_frame(img, f"idle-{i}")


# ============================================================
# WORKING: Running cat (green)
# ============================================================
def generate_working():
    color = (60, 200, 110, 255)  # Bright green
    print("working (running):")

    def run_frame(phase):
        px = []
        bob = -1 if phase in (2, 5) else 0

        # Head
        for x in range(10, 18):
            px.append((x, 5 + bob))
        for x in range(9, 18):
            px.append((x, 6 + bob))
            px.append((x, 7 + bob))
        px.append((9, 6 + bob))
        px.append((18, 6 + bob))
        # Ears
        px += [(10, 4 + bob), (11, 3 + bob), (11, 4 + bob)]
        px += [(16, 4 + bob), (17, 3 + bob), (17, 4 + bob)]
        # Eyes
        px += [(12, 6 + bob), (15, 6 + bob)]
        # Nose
        px += [(13, 7 + bob), (14, 7 + bob)]

        # Body (horizontal running)
        for x in range(4, 14):
            px.append((x, 8 + bob))
            px.append((x, 9 + bob))
        for x in range(3, 12):
            px.append((x, 10 + bob))

        # Tail
        px += [(3, 9 + bob), (2, 8 + bob), (1, 7 + bob), (1, 6 + bob)]

        # Legs
        if phase == 0:
            px += [(12, 11 + bob), (13, 12 + bob), (14, 13 + bob)]
            px += [(5, 11 + bob), (4, 12 + bob), (3, 13 + bob)]
        elif phase == 1:
            px += [(12, 11 + bob), (12, 12 + bob), (12, 13 + bob)]
            px += [(5, 11 + bob), (5, 12 + bob), (5, 13 + bob)]
        elif phase == 2:
            px += [(10, 11 + bob), (9, 12 + bob)]
            px += [(6, 11 + bob), (7, 12 + bob)]
        elif phase == 3:
            px += [(11, 11 + bob), (11, 12 + bob)]
            px += [(6, 11 + bob), (6, 12 + bob)]
        elif phase == 4:
            px += [(12, 11 + bob), (13, 12 + bob), (13, 13 + bob)]
            px += [(4, 11 + bob), (4, 12 + bob), (3, 13 + bob)]
        elif phase == 5:
            px += [(11, 11 + bob), (12, 11 + bob)]
            px += [(5, 11 + bob), (6, 11 + bob)]

        return px

    for i in range(6):
        save_frame(create_frame(run_frame(i), color), f"running-{i}")


# ============================================================
# COMPLETE: Happy cat wagging tail, waiting for praise (gold)
# ============================================================
def generate_complete():
    color = (245, 195, 50, 255)  # Gold
    sparkle_color = (255, 235, 120, 200)
    print("complete (celebrating):")

    def sitting_cat():
        px = []
        # Ears
        px += [(6, 4), (7, 3), (7, 4), (8, 4)]
        px += [(14, 4), (15, 3), (15, 4), (16, 4)]
        # Head
        for x in range(7, 16):
            px.append((x, 5))
            px.append((x, 9))
        for y in range(5, 10):
            px.append((6, y))
            px.append((16, y))
        for y in range(6, 9):
            for x in range(7, 16):
                px.append((x, y))
        # Happy eyes (^_^)
        px += [(9, 6), (10, 7), (8, 7)]
        px += [(13, 6), (14, 7), (12, 7)]
        # Smile
        px += [(10, 8), (11, 9), (12, 9), (13, 8)]
        # Body
        for y in range(10, 16):
            for x in range(7, 16):
                px.append((x, y))
            px.append((6, y))
            px.append((16, y))
        # Bottom + paws
        for x in range(6, 17):
            px.append((x, 16))
        px += [(6, 17), (7, 17), (15, 17), (16, 17)]
        return px

    tail_frames = [
        [(16, 14), (17, 13), (18, 12), (19, 11)],
        [(16, 15), (17, 14), (18, 13)],
        [(16, 14), (17, 13), (18, 12), (19, 11), (20, 10)],
        [(16, 15), (17, 14), (18, 13)],
    ]

    sparkle_frames = [
        [(3, 4), (19, 6)],
        [(4, 3), (20, 5)],
        [(2, 5), (18, 4)],
        [(3, 6), (20, 7)],
    ]

    base = sitting_cat()
    for i in range(4):
        img = create_frame(base + tail_frames[i], color)
        img = Image.alpha_composite(img, create_frame(sparkle_frames[i], sparkle_color))
        save_frame(img, f"celebrate-{i}")


# ============================================================
# ERROR: Scared cat with arched back (red)
# ============================================================
def generate_error():
    color = (230, 70, 70, 255)  # Red
    print("error (scared):")

    def scared_cat(fur_level):
        px = []
        # Ears (alert, spread wide)
        px += [(5, 3), (4, 2), (6, 4)]
        px += [(17, 3), (18, 2), (16, 4)]
        # Head
        for x in range(6, 17):
            px.append((x, 4))
            px.append((x, 8))
        for y in range(4, 9):
            px.append((6, y))
            px.append((16, y))
        for y in range(5, 8):
            for x in range(7, 16):
                px.append((x, y))
        # Wide scared eyes (big circles)
        px += [(9, 5), (9, 6), (9, 7), (10, 5), (10, 7)]
        px += [(13, 5), (13, 6), (13, 7), (12, 5), (12, 7)]
        # Open mouth
        px += [(10, 8), (11, 8), (12, 8)]

        # Arched back
        arch = 8
        for x in range(5, 18):
            px.append((x, arch))
        for x in range(6, 17):
            px.append((x, arch + 1))
            px.append((x, arch + 2))

        # Legs (stiff, spread)
        px += [(6, 11), (6, 12), (6, 13), (6, 14)]
        px += [(16, 11), (16, 12), (16, 13), (16, 14)]

        # Puffed tail
        px += [(4, 8), (3, 7), (2, 6), (3, 6), (2, 5), (4, 7)]

        # Fur standing on end
        if fur_level > 0:
            px += [(8, 7), (10, 7), (12, 7), (14, 7)]
            px += [(7, 7), (9, 7), (11, 7), (13, 7), (15, 7)]

        return px

    for i, fur in enumerate([0, 1, 1]):
        save_frame(create_frame(scared_cat(fur), color), f"scared-{i}")


# ============================================================
if __name__ == "__main__":
    # Clean old frames
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(OUTPUT_DIR, f))

    print(f"Generating frames to: {OUTPUT_DIR}\n")
    generate_idle()
    generate_working()
    generate_complete()
    generate_error()

    total = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")])
    print(f"\nDone! {total} frames generated.")
