#!/usr/bin/env python3
"""
MeowBar Pixel Cat Frame Generator v4
Totoro-inspired outline-only style. Transparent body, only edge lines.
44x44 (@2x for 22x22 logical).

States: idle (gray), working (green), complete (gold), error (red).
"""

import os
from PIL import Image, ImageDraw

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "app", "MeowBar", "Resources", "Frames")
os.makedirs(OUTPUT_DIR, exist_ok=True)

GRID = 22
SCALE = 2
SIZE = GRID * SCALE


def draw_pixels(draw, pixels, color):
    for x, y in pixels:
        if 0 <= x < GRID and 0 <= y < GRID:
            draw.rectangle(
                [x * SCALE, y * SCALE, (x + 1) * SCALE - 1, (y + 1) * SCALE - 1],
                fill=color,
            )


def save_frame(img, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    img.save(path)
    print(f"  {name}.png")


def make_outline_frame(pixels, color, extras=None):
    """Create frame with outline only - transparent interior."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_pixels(draw, pixels, color)
    if extras:
        for px_list, c in extras:
            draw_pixels(draw, px_list, c)
    return img


# ============================================================
# Totoro-style cat: round chubby body, small ears, big eyes
# ============================================================

def totoro_sitting(x_off=0, y_off=0):
    """Sitting Totoro-cat outline. Round body, pointy ears, big eyes."""
    px = []
    o = x_off
    v = y_off

    # Left ear
    px += [(5+o, 5+v), (5+o, 4+v), (6+o, 3+v), (7+o, 2+v)]
    # Right ear
    px += [(16+o, 5+v), (16+o, 4+v), (15+o, 3+v), (14+o, 2+v)]

    # Head top (round)
    px += [(8+o, 2+v), (9+o, 1+v), (10+o, 1+v), (11+o, 1+v), (12+o, 1+v), (13+o, 2+v)]

    # Head sides
    px += [(4+o, 6+v), (4+o, 7+v)]
    px += [(17+o, 6+v), (17+o, 7+v)]

    # Eyes (big round Totoro eyes)
    px += [(7+o, 6+v), (8+o, 6+v)]
    px += [(13+o, 6+v), (14+o, 6+v)]

    # Nose (tiny V)
    px += [(10+o, 7+v), (11+o, 7+v)]

    # Whiskers
    px += [(2+o, 7+v), (3+o, 7+v)]
    px += [(18+o, 7+v), (19+o, 7+v)]

    # Mouth / chin line
    px += [(6+o, 8+v), (7+o, 9+v), (8+o, 9+v), (9+o, 9+v), (10+o, 9+v),
           (11+o, 9+v), (12+o, 9+v), (13+o, 9+v), (14+o, 9+v), (15+o, 8+v)]

    # Body sides (chubby round)
    px += [(4+o, 8+v), (3+o, 9+v), (3+o, 10+v), (3+o, 11+v), (3+o, 12+v),
           (3+o, 13+v), (3+o, 14+v), (4+o, 15+v)]
    px += [(17+o, 8+v), (18+o, 9+v), (18+o, 10+v), (18+o, 11+v), (18+o, 12+v),
           (18+o, 13+v), (18+o, 14+v), (17+o, 15+v)]

    # Belly line (subtle curve inside)
    px += [(7+o, 10+v), (6+o, 11+v), (6+o, 12+v), (6+o, 13+v), (7+o, 14+v)]
    px += [(14+o, 10+v), (15+o, 11+v), (15+o, 12+v), (15+o, 13+v), (14+o, 14+v)]

    # Bottom
    px += [(5+o, 16+v), (6+o, 16+v), (7+o, 16+v), (8+o, 16+v), (9+o, 16+v),
           (10+o, 16+v), (11+o, 16+v), (12+o, 16+v), (13+o, 16+v), (14+o, 16+v),
           (15+o, 16+v), (16+o, 16+v)]

    # Feet
    px += [(5+o, 17+v), (6+o, 17+v), (7+o, 17+v)]
    px += [(14+o, 17+v), (15+o, 17+v), (16+o, 17+v)]

    return px


# ============================================================
# IDLE: Sleeping Totoro (gray)
# ============================================================
def generate_idle():
    color = (140, 140, 150, 255)  # Medium gray, visible on both light/dark
    zzz_color = (140, 140, 150, 160)
    print("idle (sleeping):")

    def sleeping_totoro():
        px = []
        # Ear (small, folded)
        px += [(5, 9), (6, 8), (7, 8)]

        # Head curve (tucked)
        px += [(5, 10), (6, 10), (7, 10), (8, 9), (9, 9)]

        # Closed eyes
        px += [(7, 10), (8, 10)]

        # Body (curled round blob)
        # Top curve
        for x in range(5, 18):
            px.append((x, 11))
        # Bottom
        for x in range(4, 19):
            px.append((x, 17))
        # Left side
        px += [(4, 12), (4, 13), (4, 14), (4, 15), (4, 16)]
        # Right side
        px += [(18, 12), (18, 13), (18, 14), (18, 15), (18, 16)]

        return px

    base = sleeping_totoro()

    tails = [
        [(18, 15), (19, 14), (20, 13)],
        [(18, 16), (19, 15), (20, 14)],
        [(18, 16), (19, 16), (20, 15)],
        [(18, 16), (19, 15), (20, 14)],
    ]

    zzz = [
        [(11, 7)],
        [(11, 7), (12, 6)],
        [(11, 7), (12, 6), (13, 5)],
        [(12, 6), (13, 5)],
    ]

    for i in range(4):
        img = make_outline_frame(base + tails[i], color,
                                  extras=[(zzz[i], zzz_color)])
        save_frame(img, f"idle-{i}")


# ============================================================
# WORKING: Running Totoro (green)
# ============================================================
def generate_working():
    color = (80, 190, 120, 255)  # Pleasant green
    print("working (running):")

    def run_frame(phase):
        px = []
        bob = -1 if phase in (2, 5) else 0

        # Ears
        px += [(13, 1+bob), (14, 0+bob)]
        px += [(18, 1+bob), (19, 0+bob)]

        # Head (round, facing right)
        px += [(14, 1+bob), (15, 1+bob), (16, 1+bob), (17, 1+bob)]
        px += [(12, 2+bob), (12, 3+bob), (12, 4+bob)]
        px += [(20, 2+bob), (20, 3+bob), (20, 4+bob)]
        # Head bottom
        px += [(13, 5+bob), (14, 5+bob), (15, 5+bob), (16, 5+bob),
               (17, 5+bob), (18, 5+bob), (19, 5+bob)]

        # Eyes
        px += [(15, 3+bob), (18, 3+bob)]

        # Body (horizontal, running)
        # Top
        for x in range(3, 14):
            px.append((x, 6+bob))
        # Bottom
        for x in range(2, 12):
            px.append((x, 10+bob))
        # Left side (butt)
        px += [(2, 7+bob), (2, 8+bob), (2, 9+bob)]
        # Connect body to head
        px += [(14, 6+bob)]

        # Tail (curvy up)
        px += [(1, 8+bob), (0, 7+bob), (0, 6+bob), (1, 5+bob)]

        # Legs
        if phase == 0:
            px += [(12, 11+bob), (13, 12+bob), (14, 13+bob)]
            px += [(4, 11+bob), (3, 12+bob), (2, 13+bob)]
        elif phase == 1:
            px += [(11, 11+bob), (11, 12+bob), (11, 13+bob)]
            px += [(5, 11+bob), (5, 12+bob), (5, 13+bob)]
        elif phase == 2:
            px += [(10, 11+bob), (9, 12+bob)]
            px += [(6, 11+bob), (7, 12+bob)]
        elif phase == 3:
            px += [(11, 11+bob), (11, 12+bob)]
            px += [(5, 11+bob), (5, 12+bob)]
        elif phase == 4:
            px += [(12, 11+bob), (12, 12+bob), (13, 13+bob)]
            px += [(4, 11+bob), (3, 12+bob), (3, 13+bob)]
        elif phase == 5:
            px += [(10, 11+bob), (11, 11+bob)]
            px += [(5, 11+bob), (6, 11+bob)]

        return px

    for i in range(6):
        save_frame(make_outline_frame(run_frame(i), color), f"running-{i}")


# ============================================================
# COMPLETE: Happy Totoro wagging tail (gold)
# ============================================================
def generate_complete():
    color = (220, 180, 50, 255)  # Warm gold
    sparkle_color = (220, 180, 50, 140)
    print("complete (celebrating):")

    base = totoro_sitting()

    # Happy eyes (^_^) replace normal eyes
    happy_eyes = [(7, 5), (8, 6), (6, 6),
                  (13, 5), (14, 6), (15, 6)]

    tails = [
        [(17, 13), (18, 12), (19, 11), (20, 10)],
        [(17, 14), (18, 13), (19, 12)],
        [(17, 13), (18, 12), (19, 11), (20, 10), (21, 9)],
        [(17, 14), (18, 13), (19, 12)],
    ]

    sparkles = [
        [(1, 3), (20, 5)],
        [(2, 2), (21, 4)],
        [(1, 4), (19, 3)],
        [(2, 5), (21, 6)],
    ]

    for i in range(4):
        img = make_outline_frame(
            base + tails[i], color,
            extras=[(happy_eyes, color), (sparkles[i], sparkle_color)]
        )
        save_frame(img, f"celebrate-{i}")


# ============================================================
# ERROR: Scared Totoro (red)
# ============================================================
def generate_error():
    color = (220, 80, 80, 255)  # Clear red
    print("error (scared):")

    def scared_totoro(fur):
        px = []

        # Ears (spread wide, alert)
        px += [(3, 3), (4, 2), (5, 1)]
        px += [(18, 3), (17, 2), (16, 1)]

        # Head (rounder, puffed)
        px += [(6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1),
               (12, 1), (13, 1), (14, 1), (15, 1)]
        px += [(3, 4), (3, 5), (3, 6), (3, 7)]
        px += [(18, 4), (18, 5), (18, 6), (18, 7)]

        # Big scared eyes (O_O)
        px += [(7, 4), (7, 5), (7, 6), (8, 4), (8, 6)]
        px += [(13, 4), (13, 5), (13, 6), (14, 4), (14, 6)]

        # Open mouth
        px += [(9, 7), (10, 8), (11, 8), (12, 7)]

        # Body (arched, tense)
        px += [(4, 8), (5, 9)]
        px += [(17, 8), (16, 9)]
        for x in range(5, 17):
            px.append((x, 9))

        # Belly (tense)
        for x in range(4, 18):
            px.append((x, 12))
        px += [(3, 10), (3, 11)]
        px += [(18, 10), (18, 11)]

        # Legs (stiff)
        px += [(5, 13), (5, 14), (5, 15), (4, 15), (6, 15)]
        px += [(16, 13), (16, 14), (16, 15), (15, 15), (17, 15)]

        # Puffed tail
        px += [(2, 9), (1, 8), (0, 7), (0, 6), (1, 6), (1, 5)]

        # Fur standing
        if fur > 0:
            px += [(7, 0), (10, 0), (13, 0)]
            px += [(8, 8), (10, 8), (12, 8)]

        return px

    for i, fur in enumerate([0, 1, 1]):
        save_frame(make_outline_frame(scared_totoro(fur), color), f"scared-{i}")


# ============================================================
if __name__ == "__main__":
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(OUTPUT_DIR, f))

    print(f"Output: {OUTPUT_DIR}\n")
    generate_idle()
    generate_working()
    generate_complete()
    generate_error()

    total = len([f for f in os.listdir(OUTPUT_DIR) if f.endswith(".png")])
    print(f"\nDone! {total} frames.")
