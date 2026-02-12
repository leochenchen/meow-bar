#!/usr/bin/env python3
"""
MeowBar Pixel Cat Frame Generator v3
Clear outline + colored fill style, like ClashX cat.
44x44 (@2x for 22x22 logical).

4 states: idle (gray outline), working (green), complete (gold), error (red).
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


def make_frame(outline_px, fill_px, outline_color, fill_color, extras=None):
    """Create frame with outline + fill, like a proper pixel art sprite."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_pixels(draw, fill_px, fill_color)
    draw_pixels(draw, outline_px, outline_color)
    if extras:
        for px_list, color in extras:
            draw_pixels(draw, px_list, color)
    return img


# ============================================================
# Cat body part builders
# ============================================================

def sitting_cat_outline():
    """Clear cat silhouette - sitting pose, facing right."""
    px = []
    # Left ear
    px += [(5, 5), (6, 4), (6, 3), (7, 2), (7, 3), (8, 3)]
    # Right ear
    px += [(13, 5), (14, 4), (14, 3), (15, 2), (15, 3), (16, 3)]
    # Top of head
    px += [(8, 3), (9, 2), (10, 2), (11, 2), (12, 2), (13, 3), (14, 3)]
    # Left side of head
    px += [(5, 6), (5, 7), (5, 8)]
    # Right side of head
    px += [(16, 5), (16, 6), (16, 7), (16, 8)]
    # Chin
    px += [(6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9)]
    # Body left
    px += [(5, 10), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15)]
    # Body right
    px += [(16, 10), (16, 11), (16, 12), (16, 13), (16, 14), (16, 15)]
    # Bottom
    px += [(5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16)]
    # Paws
    px += [(5, 17), (6, 17), (7, 17)]
    px += [(14, 17), (15, 17), (16, 17)]
    return px


def sitting_cat_fill():
    """Fill for sitting cat."""
    px = []
    # Head fill
    for y in range(4, 9):
        for x in range(6, 16):
            px.append((x, y))
    # Ear fill
    px += [(7, 3), (7, 4), (8, 4)]
    px += [(14, 4), (15, 4), (14, 3)]
    # Body fill
    for y in range(10, 16):
        for x in range(6, 16):
            px.append((x, y))
    return px


def cat_face_normal():
    """Normal eyes and nose."""
    px = []
    # Eyes (2px dots)
    px += [(8, 6), (9, 6)]
    px += [(13, 6), (14, 6)]  # Fixed: removed (12, 6) which was too close
    # Nose
    px += [(10, 7), (11, 7)]
    # Whiskers
    px += [(7, 7), (4, 7)]
    px += [(14, 7), (17, 7)]  # Fixed: removed (15, 7) duplicate
    return px


def cat_face_happy():
    """Happy eyes ^_^ and smile."""
    px = []
    # Happy eyes (^)
    px += [(8, 5), (9, 6), (7, 6)]
    px += [(13, 5), (14, 6), (12, 6)]
    # Smile
    px += [(9, 8), (10, 8), (11, 8), (12, 8)]
    # Whiskers
    px += [(4, 7), (17, 7)]
    return px


def cat_face_scared():
    """Wide scared eyes, open mouth."""
    px = []
    # Big round eyes
    px += [(7, 5), (8, 5), (7, 6), (8, 6), (7, 7), (8, 7)]
    px += [(13, 5), (14, 5), (13, 6), (14, 6), (13, 7), (14, 7)]
    # Open mouth
    px += [(10, 8), (11, 8)]
    return px


def cat_face_sleeping():
    """Closed eyes - lines."""
    px = []
    # Closed eyes (horizontal lines)
    px += [(8, 6), (9, 6)]
    px += [(12, 6), (13, 6)]
    # Nose
    px += [(10, 7), (11, 7)]
    return px


# ============================================================
# IDLE: Sleeping cat (gray, visible outline)
# ============================================================
def generate_idle():
    outline_color = (100, 100, 110, 255)  # Dark gray outline (visible!)
    fill_color = (160, 165, 175, 255)      # Medium gray fill
    face_color = (60, 60, 70, 255)         # Dark face features
    zzz_color = (130, 130, 145, 200)
    print("idle (sleeping):")

    def curled_outline():
        px = []
        # Ear
        px += [(5, 8), (6, 7), (7, 7)]
        # Head top
        px += [(6, 8), (7, 8)]
        # Head left
        px += [(4, 9), (4, 10), (4, 11)]
        # Body top curve
        for x in range(5, 17):
            px.append((x, 11))
        # Body bottom
        for x in range(4, 18):
            px.append((x, 16))
        # Left side
        px += [(4, 12), (4, 13), (4, 14), (4, 15)]
        # Right side
        px += [(17, 12), (17, 13), (17, 14), (17, 15)]
        # Head bottom / body connection
        px += [(5, 11), (8, 10), (9, 10), (10, 10)]
        return px

    def curled_fill():
        px = []
        # Head
        for x in range(5, 10):
            px.append((x, 9))
            px.append((x, 10))
        px += [(5, 8), (6, 8)]
        # Body
        for y in range(12, 16):
            for x in range(5, 17):
                px.append((x, y))
        return px

    def face_sleeping():
        # Closed eyes
        return [(6, 9), (7, 9)]

    tails = [
        [(17, 14), (18, 13), (19, 12)],
        [(17, 15), (18, 14), (19, 13)],
        [(17, 15), (18, 15), (19, 14)],
        [(17, 15), (18, 14), (19, 13)],
    ]

    zzz_frames = [
        [(11, 7)],
        [(11, 7), (12, 6)],
        [(11, 7), (12, 6), (13, 5)],
        [(12, 6), (13, 5)],
    ]

    outline = curled_outline()
    fill = curled_fill()
    face = face_sleeping()

    for i in range(4):
        img = make_frame(
            outline + tails[i], fill, outline_color, fill_color,
            extras=[(face, face_color), (zzz_frames[i], zzz_color)]
        )
        save_frame(img, f"idle-{i}")


# ============================================================
# WORKING: Running cat (green)
# ============================================================
def generate_working():
    outline_color = (30, 120, 60, 255)     # Dark green outline
    fill_color = (70, 210, 120, 255)       # Bright green fill
    face_color = (20, 80, 40, 255)         # Dark green face
    print("working (running):")

    def run_frame(phase):
        outline = []
        fill = []
        bob = -1 if phase in (2, 5) else 0

        # Head outline
        # Ears
        outline += [(12, 2 + bob), (13, 1 + bob), (13, 2 + bob)]
        outline += [(17, 2 + bob), (18, 1 + bob), (18, 2 + bob)]
        # Head top
        for x in range(13, 18):
            outline.append((x, 2 + bob))
        # Head sides
        outline += [(11, 3 + bob), (11, 4 + bob), (11, 5 + bob)]
        outline += [(19, 3 + bob), (19, 4 + bob), (19, 5 + bob)]
        # Head bottom
        for x in range(12, 19):
            outline.append((x, 6 + bob))

        # Head fill
        for y in range(3, 6):
            for x in range(12, 19):
                fill.append((x, y + bob))
        fill += [(13, 2 + bob), (14, 2 + bob), (15, 2 + bob), (16, 2 + bob), (17, 2 + bob)]

        # Face
        face = [(14, 4 + bob), (17, 4 + bob)]  # Eyes
        face += [(15, 5 + bob), (16, 5 + bob)]  # Nose

        # Body outline
        for x in range(3, 15):
            outline.append((x, 7 + bob))  # Top
        for x in range(2, 13):
            outline.append((x, 10 + bob))  # Bottom
        outline += [(2, 8 + bob), (2, 9 + bob)]  # Left side
        outline += [(15, 8 + bob), (14, 8 + bob)]  # Right connect to head

        # Body fill
        for y in range(8, 10):
            for x in range(3, 14):
                fill.append((x, y + bob))

        # Tail outline
        outline += [(2, 8 + bob), (1, 7 + bob), (0, 6 + bob), (0, 5 + bob), (1, 4 + bob)]

        # Legs (vary by phase)
        if phase == 0:  # Front forward, back backward
            outline += [(13, 11 + bob), (14, 12 + bob), (15, 13 + bob), (15, 14 + bob)]
            outline += [(4, 11 + bob), (3, 12 + bob), (2, 13 + bob), (2, 14 + bob)]
        elif phase == 1:
            outline += [(13, 11 + bob), (13, 12 + bob), (13, 13 + bob), (13, 14 + bob)]
            outline += [(5, 11 + bob), (5, 12 + bob), (5, 13 + bob), (5, 14 + bob)]
        elif phase == 2:  # Leap
            outline += [(11, 11 + bob), (10, 12 + bob)]
            outline += [(6, 11 + bob), (7, 12 + bob)]
        elif phase == 3:
            outline += [(12, 11 + bob), (12, 12 + bob), (12, 13 + bob)]
            outline += [(6, 11 + bob), (6, 12 + bob), (6, 13 + bob)]
        elif phase == 4:
            outline += [(14, 11 + bob), (14, 12 + bob), (15, 13 + bob), (15, 14 + bob)]
            outline += [(4, 11 + bob), (3, 12 + bob), (3, 13 + bob), (3, 14 + bob)]
        elif phase == 5:  # Leap
            outline += [(12, 11 + bob), (13, 11 + bob)]
            outline += [(5, 11 + bob), (6, 11 + bob)]

        return outline, fill, face

    for i in range(6):
        o, f, face = run_frame(i)
        img = make_frame(o, f, outline_color, fill_color,
                         extras=[(face, face_color)])
        save_frame(img, f"running-{i}")


# ============================================================
# COMPLETE: Happy cat wagging tail (gold)
# ============================================================
def generate_complete():
    outline_color = (160, 120, 20, 255)    # Dark gold outline
    fill_color = (250, 200, 60, 255)       # Bright gold fill
    face_color = (120, 80, 10, 255)        # Dark gold face
    sparkle_color = (255, 240, 130, 220)
    print("complete (celebrating):")

    outline = sitting_cat_outline()
    fill = sitting_cat_fill()
    face = cat_face_happy()

    tails = [
        [(16, 13), (17, 12), (18, 11), (19, 10)],
        [(16, 14), (17, 13), (18, 12)],
        [(16, 13), (17, 12), (18, 11), (19, 10), (20, 9)],
        [(16, 14), (17, 13), (18, 12)],
    ]

    sparkles = [
        [(3, 3), (19, 5)],
        [(4, 2), (20, 4)],
        [(2, 4), (18, 3)],
        [(3, 5), (20, 6)],
    ]

    for i in range(4):
        img = make_frame(
            outline + tails[i], fill, outline_color, fill_color,
            extras=[(face, face_color), (sparkles[i], sparkle_color)]
        )
        save_frame(img, f"celebrate-{i}")


# ============================================================
# ERROR: Scared cat (red)
# ============================================================
def generate_error():
    outline_color = (150, 30, 30, 255)     # Dark red outline
    fill_color = (235, 80, 80, 255)        # Bright red fill
    face_color = (100, 20, 20, 255)        # Dark red face
    print("error (scared):")

    def scared_outline(fur):
        px = []
        # Ears (spread wide, alert)
        px += [(4, 3), (3, 2), (3, 1), (5, 4)]
        px += [(17, 3), (18, 2), (18, 1), (16, 4)]
        # Head top
        for x in range(5, 17):
            px.append((x, 3))
        # Head sides
        px += [(4, 4), (4, 5), (4, 6), (4, 7)]
        px += [(17, 4), (17, 5), (17, 6), (17, 7)]
        # Head bottom / arch top
        for x in range(4, 18):
            px.append((x, 8))
        # Arch body
        for x in range(4, 18):
            px.append((x, 11))
        px += [(3, 9), (3, 10)]
        px += [(18, 9), (18, 10)]
        # Legs
        px += [(5, 12), (5, 13), (5, 14), (5, 15), (4, 15), (6, 15)]
        px += [(16, 12), (16, 13), (16, 14), (16, 15), (15, 15), (17, 15)]
        # Puffed tail
        px += [(2, 8), (1, 7), (0, 6), (1, 6), (0, 5), (2, 7), (1, 5)]
        # Fur spikes
        if fur > 0:
            px += [(7, 7), (9, 7), (11, 7), (13, 7), (15, 7)]
        return px

    def scared_fill(fur):
        px = []
        # Head
        for y in range(4, 8):
            for x in range(5, 17):
                px.append((x, y))
        # Body
        for y in range(9, 11):
            for x in range(4, 18):
                px.append((x, y))
        return px

    face = cat_face_scared()

    for i, fur in enumerate([0, 1, 1]):
        img = make_frame(
            scared_outline(fur), scared_fill(fur), outline_color, fill_color,
            extras=[(face, face_color)]
        )
        save_frame(img, f"scared-{i}")


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
