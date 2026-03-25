import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

random.seed(7)

FPS = 30
DURATION = 10
TOTAL_FRAMES = FPS * DURATION

MAX_DEPTH = 7
LENGTH_SHRINK = 0.74
BRANCH_ANGLE = math.radians(22)
ANGLE_JITTER = math.radians(7)
LENGTH_JITTER = 0.08
BRANCH_PROB = 0.88

START_LENGTH = 75
START_DEPTH = 0
BASE_Y = 0
CENTER_ANGLE = math.pi / 2

branches = []

def make_start_points(start, step=10, count=15):
    return [start + i * step for i in range(count)]

def generate_branch(x, y, angle, length, depth):
    branch_id = len(branches)

    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)

    branches.append({
        "id": branch_id,
        "x": x,
        "y": y,
        "end_x": end_x,
        "end_y": end_y,
        "angle": angle,
        "length": length,
        "depth": depth,
    })

    if depth >= MAX_DEPTH:
        return

    child_angles = [
        angle + BRANCH_ANGLE + random.uniform(-ANGLE_JITTER, ANGLE_JITTER),
        angle - BRANCH_ANGLE + random.uniform(-ANGLE_JITTER, ANGLE_JITTER),
    ]

    for child_angle in child_angles:
        if random.random() > BRANCH_PROB:
            continue

        child_length = length * LENGTH_SHRINK * random.uniform(
            1 - LENGTH_JITTER, 1 + LENGTH_JITTER
        )

        generate_branch(end_x, end_y, child_angle, child_length, depth + 1)

START_POINTS = make_start_points(-70)

for x in START_POINTS:
    angle = CENTER_ANGLE - math.radians(x * 1.2)
    generate_branch(x, BASE_Y, angle, START_LENGTH, START_DEPTH)

for b in branches:
    depth_ratio = b["depth"] / (MAX_DEPTH + 1)
    b["start_frame"] = int(depth_ratio * TOTAL_FRAMES * 0.55)
    b["end_frame"] = b["start_frame"] + int(TOTAL_FRAMES * 0.16)

xs = []
ys = []

for b in branches:
    xs.extend([b["x"], b["end_x"]])
    ys.extend([b["y"], b["end_y"]])

padding = 20
xmin, xmax = min(xs) - padding, max(xs) + padding
ymin, ymax = min(ys) - padding, max(ys) + padding

fig, ax = plt.subplots(figsize=(6, 9))
bg = "#0b1020"
line_color = "#dfe8ff"

fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)
ax.axis("off")
ax.set_aspect("equal")

ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

lines = []
for _ in branches:
    line, = ax.plot([], [], color=line_color, linewidth=1.0, alpha=0.0, solid_capstyle="round")
    lines.append(line)

def ease_out(t):
    return 1 - (1 - t) ** 3

def get_progress(branch, frame):
    if frame <= branch["start_frame"]:
        return 0.0
    if frame >= branch["end_frame"]:
        return 1.0
    raw = (frame - branch["start_frame"]) / (branch["end_frame"] - branch["start_frame"])
    return ease_out(raw)

def get_alpha(branch, frame, progress):
    fade_start = TOTAL_FRAMES * 0.72
    if frame < fade_start:
        return 0.85 * progress
    fade_ratio = 1 - min(1.0, (frame - fade_start) / (TOTAL_FRAMES - fade_start))
    return 0.85 * progress * fade_ratio

def get_linewidth(depth):
    return max(0.55, 2.2 * (0.82 ** depth))

def wind(branch, frame, progress):
    t = frame / FPS
    depth_factor = branch["depth"] / MAX_DEPTH
    amp = 0.15 + 1.4 * depth_factor
    phase = branch["id"] * 0.41
    return math.sin(t * 1.4 + phase) * amp * progress

def update(frame):
    loop_reset_frame = int(TOTAL_FRAMES * 0.94)

    if frame >= loop_reset_frame:
        for line in lines:
            line.set_alpha(0.0)
            line.set_data([], [])
        return lines

    for i, b in enumerate(branches):
        progress = get_progress(b, frame)

        if progress <= 0.001:
            lines[i].set_alpha(0.0)
            lines[i].set_data([], [])
            continue

        x0, y0 = b["x"], b["y"]
        x1 = x0 + b["length"] * progress * math.cos(b["angle"])
        y1 = y0 + b["length"] * progress * math.sin(b["angle"])

        x1 += wind(b, frame, progress)

        lines[i].set_data([x0, x1], [y0, y1])
        lines[i].set_linewidth(get_linewidth(b["depth"]))
        lines[i].set_alpha(get_alpha(b, frame, progress))

    return lines

ani = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=1000 / FPS,
    blit=True,
    repeat=True
)

plt.show()
