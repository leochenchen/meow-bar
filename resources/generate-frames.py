#!/usr/bin/env python3
"""
MeowBar Pixel Cat Frame Generator
Generates 36x36 (@2x) colored pixel art cat PNGs for each state.
Each pixel in the design grid is 2x2 actual pixels (18x18 logical -> 36x36 @2x).

Usage: pip install Pillow && python generate-frames.py
Output: ../app/MeowBar/Resources/Frames/
"""

import os
from PIL import Image, ImageDraw

# Output directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "app", "MeowBar", "Resources", "Frames")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Canvas: 18x18 logical grid, each cell = 2px -> 36x36 output
GRID = 18
SCALE = 2
SIZE = GRID * SCALE


def create_frame(pixels, color, bg=(0, 0, 0, 0)):
    """Create a frame from a pixel map. pixels is list of (x, y) tuples to fill."""
    img = Image.new("RGBA", (SIZE, SIZE), bg)
    draw = ImageDraw.Draw(img)
    for x, y in pixels:
        draw.rectangle(
            [x * SCALE, y * SCALE, (x + 1) * SCALE - 1, (y + 1) * SCALE - 1],
            fill=color,
        )
    return img


def save_frame(img, name):
    path = os.path.join(OUTPUT_DIR, f"{name}.png")
    img.save(path)
    print(f"  Generated: {name}.png")


# ============================================================
# Cat pixel art definitions
# Each cat is drawn on an 18x18 grid
# ============================================================

# Common body parts for reuse
def cat_ears(x_off=0, y_off=0):
    """Pointed cat ears"""
    return [
        # Left ear
        (4 + x_off, 3 + y_off),
        (5 + x_off, 2 + y_off),
        (5 + x_off, 3 + y_off),
        (6 + x_off, 3 + y_off),
        # Right ear
        (11 + x_off, 3 + y_off),
        (12 + x_off, 2 + y_off),
        (12 + x_off, 3 + y_off),
        (13 + x_off, 3 + y_off),
    ]


def cat_head(x_off=0, y_off=0):
    """Round cat head"""
    pixels = []
    # Top of head
    for x in range(5, 13):
        pixels.append((x + x_off, 4 + y_off))
    # Sides of head
    for y in range(5, 8):
        pixels.append((4 + x_off, y + y_off))
        pixels.append((13 + x_off, y + y_off))
    # Eyes
    pixels.append((6 + x_off, 5 + y_off))
    pixels.append((11 + x_off, 5 + y_off))
    # Nose
    pixels.append((8 + x_off, 6 + y_off))
    pixels.append((9 + x_off, 6 + y_off))
    # Mouth
    pixels.append((7 + x_off, 7 + y_off))
    pixels.append((10 + x_off, 7 + y_off))
    # Bottom of head
    for x in range(5, 13):
        pixels.append((x + x_off, 7 + y_off))
    return pixels


def cat_body_sitting(x_off=0, y_off=0):
    """Sitting cat body"""
    pixels = []
    # Neck
    for x in range(6, 12):
        pixels.append((x + x_off, 8 + y_off))
    # Body
    for y in range(9, 13):
        pixels.append((5 + x_off, y + y_off))
        pixels.append((12 + x_off, y + y_off))
        for x in range(6, 12):
            pixels.append((x + x_off, y + y_off))
    # Bottom
    for x in range(5, 13):
        pixels.append((x + x_off, 13 + y_off))
    # Paws
    pixels.append((5 + x_off, 14 + y_off))
    pixels.append((6 + x_off, 14 + y_off))
    pixels.append((11 + x_off, 14 + y_off))
    pixels.append((12 + x_off, 14 + y_off))
    return pixels


# ============================================================
# State: idle (sleeping cat, gray-blue)
# ============================================================
def generate_idle():
    color = (120, 150, 180, 255)  # Gray-blue
    print("Generating: idle (sleeping cat)")

    # Sleeping curled up cat - base shape
    def sleeping_base():
        pixels = []
        # Curled body - oval shape
        for x in range(4, 14):
            pixels.append((x, 10))
            pixels.append((x, 14))
        for y in range(10, 15):
            pixels.append((4, y))
            pixels.append((13, y))
        for y in range(11, 14):
            for x in range(5, 13):
                pixels.append((x, y))
        # Head tucked in
        for x in range(5, 9):
            pixels.append((x, 9))
        pixels.append((5, 8))
        pixels.append((6, 8))
        # Ear
        pixels.append((5, 7))
        pixels.append((7, 8))
        # Closed eyes (line)
        pixels.append((6, 9))
        pixels.append((7, 9))
        return pixels

    def tail_left():
        return [(13, 13), (14, 12), (15, 11)]

    def tail_mid():
        return [(13, 13), (14, 13), (15, 12)]

    def tail_right():
        return [(13, 13), (14, 14), (15, 13)]

    base = sleeping_base()
    tails = [tail_left(), tail_mid(), tail_right(), tail_mid()]

    # Zzz indicators for sleeping
    zzz_frames = [
        [(10, 6)],
        [(10, 6), (11, 5)],
        [(10, 6), (11, 5), (12, 4)],
        [(11, 5), (12, 4)],
    ]

    for i, (tail, zzz) in enumerate(zip(tails, zzz_frames)):
        img = create_frame(base + tail, color)
        # Draw Zzz in lighter color
        zzz_img = create_frame(zzz, (160, 190, 220, 200))
        img = Image.alpha_composite(img, zzz_img)
        save_frame(img, f"idle-{i}")


# ============================================================
# State: starting (waking up cat, yellow)
# ============================================================
def generate_starting():
    color = (240, 200, 80, 255)  # Yellow
    print("Generating: starting (waking up)")

    # Frame 0: still curled up
    def curled():
        pixels = []
        for x in range(4, 14):
            pixels.append((x, 10))
            pixels.append((x, 14))
        for y in range(10, 15):
            pixels.append((4, y))
            pixels.append((13, y))
        for y in range(11, 14):
            for x in range(5, 13):
                pixels.append((x, y))
        for x in range(5, 9):
            pixels.append((x, 9))
        pixels.append((5, 8))
        pixels.append((6, 8))
        pixels.append((5, 7))
        return pixels

    # Frame 1: head lifting
    def head_lifting():
        pixels = []
        # Body still low
        for x in range(5, 13):
            for y in range(11, 15):
                pixels.append((x, y))
        pixels.append((4, 12))
        pixels.append((4, 13))
        pixels.append((13, 12))
        pixels.append((13, 13))
        # Head rising
        pixels += cat_ears(0, 1)
        pixels += cat_head(0, 1)
        return pixels

    # Frame 2: stretching up
    def stretching():
        pixels = cat_ears() + cat_head() + cat_body_sitting()
        # Stretch marks
        pixels.append((3, 10))
        pixels.append((14, 10))
        return pixels

    frames_data = [curled(), head_lifting(), stretching()]
    for i, px in enumerate(frames_data):
        save_frame(create_frame(px, color), f"wakeup-{i}")


# ============================================================
# State: thinking (typing cat, blue)
# ============================================================
def generate_thinking():
    color = (80, 140, 230, 255)  # Blue
    print("Generating: thinking (typing)")

    base = cat_ears() + cat_head() + cat_body_sitting()

    # Keyboard in front
    def keyboard():
        pixels = []
        for x in range(4, 14):
            pixels.append((x, 15))
            pixels.append((x, 16))
        return pixels

    kb = keyboard()

    # Paw positions for typing animation
    paw_frames = [
        # Left paw down
        [(5, 14), (6, 14), (6, 15)],
        # Both up
        [(5, 14), (6, 14), (11, 14), (12, 14)],
        # Right paw down
        [(11, 14), (12, 14), (11, 15)],
        # Both up
        [(5, 14), (6, 14), (11, 14), (12, 14)],
    ]

    for i, paws in enumerate(paw_frames):
        all_px = base + kb + paws
        save_frame(create_frame(all_px, color), f"typing-{i}")


# ============================================================
# State: working (running cat, green)
# ============================================================
def generate_working():
    color = (80, 200, 120, 255)  # Green
    print("Generating: working (running)")

    def running_frame(phase):
        pixels = []
        y_bob = -1 if phase in (2, 5) else 0  # Bounce up on leap frames

        # Head (slightly forward)
        for x in range(8, 15):
            pixels.append((x, 4 + y_bob))
        pixels.append((7, 5 + y_bob))
        pixels.append((14, 5 + y_bob))
        for x in range(7, 15):
            pixels.append((x, 5 + y_bob))
        pixels.append((7, 6 + y_bob))
        pixels.append((14, 6 + y_bob))
        for x in range(7, 15):
            pixels.append((x, 6 + y_bob))
        # Ears
        pixels.append((8, 3 + y_bob))
        pixels.append((9, 2 + y_bob))
        pixels.append((13, 3 + y_bob))
        pixels.append((14, 2 + y_bob))
        # Eyes
        pixels.append((9, 5 + y_bob))
        pixels.append((12, 5 + y_bob))

        # Body (horizontal, running posture)
        for x in range(3, 12):
            pixels.append((x, 7 + y_bob))
            pixels.append((x, 8 + y_bob))
        for x in range(2, 10):
            pixels.append((x, 9 + y_bob))

        # Tail
        pixels.append((2, 8 + y_bob))
        pixels.append((1, 7 + y_bob))
        pixels.append((0, 6 + y_bob))

        # Legs in different positions based on phase
        if phase == 0:  # Front legs forward, back legs back
            pixels += [(10, 10 + y_bob), (11, 11 + y_bob), (12, 12 + y_bob)]
            pixels += [(3, 10 + y_bob), (2, 11 + y_bob), (1, 12 + y_bob)]
        elif phase == 1:  # Front legs mid, back legs mid
            pixels += [(10, 10 + y_bob), (10, 11 + y_bob)]
            pixels += [(4, 10 + y_bob), (4, 11 + y_bob)]
        elif phase == 2:  # Front legs back, back legs forward (leap)
            pixels += [(8, 10 + y_bob), (7, 11 + y_bob)]
            pixels += [(5, 10 + y_bob), (6, 11 + y_bob)]
        elif phase == 3:  # All legs under
            pixels += [(9, 10 + y_bob), (9, 11 + y_bob)]
            pixels += [(5, 10 + y_bob), (5, 11 + y_bob)]
        elif phase == 4:  # Front forward, back back (opposite of 0)
            pixels += [(10, 10 + y_bob), (10, 11 + y_bob), (11, 12 + y_bob)]
            pixels += [(3, 10 + y_bob), (3, 11 + y_bob), (2, 12 + y_bob)]
        elif phase == 5:  # Leap frame
            pixels += [(9, 10 + y_bob), (10, 10 + y_bob)]
            pixels += [(4, 10 + y_bob), (5, 10 + y_bob)]

        return pixels

    for i in range(6):
        save_frame(create_frame(running_frame(i), color), f"running-{i}")


# ============================================================
# State: error (scared cat, red)
# ============================================================
def generate_error():
    color = (230, 80, 80, 255)  # Red
    print("Generating: error (scared)")

    def scared_base(arch_level):
        pixels = []
        # Ears (flattened / alert)
        pixels.append((4, 2))
        pixels.append((3, 1))
        pixels.append((5, 3))
        pixels.append((13, 2))
        pixels.append((14, 1))
        pixels.append((12, 3))

        # Head
        for x in range(5, 13):
            pixels.append((x, 3))
            pixels.append((x, 6))
        for y in range(3, 7):
            pixels.append((5, y))
            pixels.append((12, y))
        # Wide eyes (bigger = more scared)
        pixels.append((7, 4))
        pixels.append((7, 5))
        pixels.append((10, 4))
        pixels.append((10, 5))
        # Open mouth
        pixels.append((8, 6))
        pixels.append((9, 6))

        # Arched back body
        arch_y = 7 - arch_level
        for x in range(4, 14):
            pixels.append((x, arch_y))
        for x in range(5, 13):
            pixels.append((x, arch_y + 1))
            pixels.append((x, arch_y + 2))

        # Legs (stiff)
        pixels += [(5, arch_y + 3), (5, arch_y + 4)]
        pixels += [(12, arch_y + 3), (12, arch_y + 4)]

        # Puffed tail (going up)
        pixels.append((3, arch_y))
        pixels.append((2, arch_y - 1))
        pixels.append((1, arch_y - 2))
        pixels.append((2, arch_y - 2))
        pixels.append((1, arch_y - 1))

        # Fur standing on end
        if arch_level > 0:
            pixels.append((6, arch_y - 1))
            pixels.append((8, arch_y - 1))
            pixels.append((10, arch_y - 1))
            pixels.append((12, arch_y - 1))

        return pixels

    for i, arch in enumerate([0, 1, 1]):
        save_frame(create_frame(scared_base(arch), color), f"scared-{i}")


# ============================================================
# State: complete (happy cat waiting for praise, gold)
# ============================================================
def generate_complete():
    color = (240, 190, 50, 255)  # Gold
    sparkle_color = (255, 230, 100, 200)  # Light gold sparkle
    print("Generating: complete (waiting for praise)")

    base = cat_ears() + cat_head() + cat_body_sitting()

    # Happy eyes (^_^)
    happy_eyes = [(6, 5), (7, 5), (11, 5), (10, 5)]

    # Tail wagging positions
    tail_frames = [
        [(13, 12), (14, 11), (15, 10)],  # Tail up-right
        [(13, 13), (14, 12), (15, 11)],  # Tail mid
        [(13, 12), (14, 11), (15, 10), (16, 9)],  # Tail high
        [(13, 13), (14, 12), (15, 11)],  # Tail mid
    ]

    # Sparkle positions that cycle
    sparkle_frames = [
        [(2, 3), (15, 5)],
        [(3, 2), (16, 4)],
        [(1, 4), (14, 3)],
        [(2, 5), (16, 6)],
    ]

    for i, (tail, sparkles) in enumerate(zip(tail_frames, sparkle_frames)):
        img = create_frame(base + happy_eyes + tail, color)
        sparkle_img = create_frame(sparkles, sparkle_color)
        img = Image.alpha_composite(img, sparkle_img)
        save_frame(img, f"celebrate-{i}")


# ============================================================
# State: ending (waving cat, purple)
# ============================================================
def generate_ending():
    color = (160, 100, 220, 255)  # Purple
    print("Generating: ending (waving goodbye)")

    def waving_cat(paw_y):
        pixels = cat_ears() + cat_head()
        # Body
        for y in range(8, 14):
            for x in range(5, 12):  # Slightly asymmetric for wave
                pixels.append((x, y))
            pixels.append((12, y))
        for x in range(5, 13):
            pixels.append((x, 13))
        # Left paw (stationary)
        pixels.append((5, 14))
        pixels.append((6, 14))
        # Right paw (waving up)
        pixels.append((13, paw_y))
        pixels.append((14, paw_y))
        pixels.append((14, paw_y - 1))
        # Right arm
        for y in range(paw_y + 1, 10):
            pixels.append((13, y))
        # Tail
        pixels.append((4, 12))
        pixels.append((3, 11))
        pixels.append((2, 10))
        return pixels

    paw_positions = [7, 5, 4, 5]
    for i, py in enumerate(paw_positions):
        save_frame(create_frame(waving_cat(py), color), f"wave-{i}")


# ============================================================
# State: compacting (thinking cat, teal)
# ============================================================
def generate_compacting():
    color = (70, 190, 190, 255)  # Teal
    dot_color = (120, 220, 220, 200)
    print("Generating: compacting (thinking)")

    base = cat_ears() + cat_head() + cat_body_sitting()

    # Head tilted slightly (modify head pixels)
    tilt = [(14, 5)]  # Extra pixel on right for tilt effect

    # Thought bubble dots
    thought_frames = [
        [(15, 5)],
        [(15, 5), (16, 4)],
        [(15, 5), (16, 4), (16, 3)],
        [(16, 4), (16, 3), (15, 2)],
    ]

    # Tail slow sway
    tail_frames = [
        [(13, 13), (14, 12)],
        [(13, 13), (14, 13)],
        [(13, 13), (14, 14)],
        [(13, 13), (14, 13)],
    ]

    for i, (dots, tail) in enumerate(zip(thought_frames, tail_frames)):
        img = create_frame(base + tilt + tail, color)
        dot_img = create_frame(dots, dot_color)
        img = Image.alpha_composite(img, dot_img)
        save_frame(img, f"thinking-{i}")


# ============================================================
# Generate all frames
# ============================================================
if __name__ == "__main__":
    print(f"Generating pixel cat frames to: {OUTPUT_DIR}\n")
    generate_idle()
    generate_starting()
    generate_thinking()
    generate_working()
    generate_error()
    generate_complete()
    generate_ending()
    generate_compacting()
    print(f"\nDone! Generated all frames to {OUTPUT_DIR}")
