"""
KIARIT PHARMACEUTICALS — Hero background video generator.

Builds an 18-second cinematic loop from the product still plates in
tools/hero_src/. Each plate gets a slow Ken Burns move (a scale and pan
that never reverses direction mid-shot), and shots cross-dissolve into
one another. The last shot dissolves back into the first, so the file
loops seamlessly with no visible cut.

The video is a background element: no text, no audio, nothing that has to
be read. Everything legible sits in the HTML on top of it.

    .venv/bin/python tools/make_hero_video.py

--------------------------------------------------------------------------
SOURCE PLATES ARE NOT IN THE REPOSITORY
--------------------------------------------------------------------------
tools/hero_src/ is gitignored. The rendered output (assets/video/hero.mp4,
hero.webm, hero-poster.jpg) is committed, so nothing here is needed to
build or serve the site — only to re-render the video.

To re-create the plates, produce four 16:9 images at roughly 1376x768 and
save them into tools/hero_src/ under the filenames listed in SHOTS below:

  grp-1.jpg  Ritclear, Ritshade and Ritglow cartons standing on pale
             marble, warm golden light raking from the right, deep warm
             brown near-black background.
  grp-2.jpg  Kiamild and KiaRestora bottles, same set and lighting.
  grp-3.jpg  Ritclear carton against flowing liquid-gold silk on near
             black, with suspended gold particles.
  grp-4.jpg  All five products in a staggered lineup on the marble set.

Composition matters: keep the product mass toward the right of frame and
leave the left roughly empty. The hero headline sits over the left side,
and while the renderer repositions each frame automatically (see
push_right), it can only slide what the plate actually gives it.

Packaging colours, printed text and proportions must match
assets/img/products/*.jpg exactly.
"""
import math
import os
import subprocess

import numpy as np
from PIL import Image
import imageio_ffmpeg

ROOT = os.path.join(os.path.dirname(__file__), "..")
SRC = os.path.join(os.path.dirname(__file__), "hero_src")
OUT = os.path.join(ROOT, "assets", "video")
os.makedirs(OUT, exist_ok=True)

W, H = 1600, 900           # output resolution — a backdrop, not a feature film
FPS = 25
SHOT = 5.8                 # seconds each shot holds
FADE = 1.3                 # seconds of cross-dissolve between shots

# Each shot: (file, start_zoom, end_zoom, start_centre, end_centre)
# Centres are fractions of the image; 0.5 is the middle. Moves are gentle —
# a hero background that pans hard fights the headline sitting on top of it.
# The hero copy occupies the left ~45% of the frame, so each shot declares
# where its product mass should land horizontally in the output (TARGET_X).
# Panning alone cannot reach those values without hitting the crop clamp, so
# the renderer also slides the whole plate sideways and extends the dark
# backdrop into the gap — see push_right() below.
#
# (file, zoom0, zoom1, centre0, centre1, target_x)
SHOTS = [
    ("grp-1.jpg", 1.08, 1.16, (0.50, 0.56), (0.50, 0.53), 0.70),   # three cartons
    ("grp-3.jpg", 1.16, 1.06, (0.62, 0.50), (0.58, 0.52), 0.72),   # serum in gold
    ("grp-4.jpg", 1.18, 1.08, (0.50, 0.56), (0.50, 0.52), 0.68),   # full lineup
    ("grp-2.jpg", 1.06, 1.14, (0.50, 0.56), (0.50, 0.53), 0.70),   # two bottles
]

N_SHOTS = len(SHOTS)
STEP = SHOT - FADE                      # new shot begins every STEP seconds
DURATION = STEP * N_SHOTS               # total loop length
N_FRAMES = int(round(DURATION * FPS))


def load(name):
    im = Image.open(os.path.join(SRC, name)).convert("RGB")
    # Pre-scale so the widest crop we ask for still has real pixels behind it.
    target_w = int(W * 1.25)
    if im.width < target_w:
        im = im.resize((target_w, round(im.height * target_w / im.width)), Image.LANCZOS)
    return im


PLATES = [load(s[0]) for s in SHOTS]


def ease(t):
    """Smootherstep. Keeps the pan from starting or stopping abruptly."""
    return t * t * t * (t * (t * 6 - 15) + 10)


def mass_centre(im):
    """Horizontal centre of the product mass, as a fraction of width.

    Products are the bright, saturated pixels; the backdrop is dark warm
    brown. Measuring this rather than hard-coding it means the framing stays
    correct if a plate is ever re-rendered with a different composition.
    """
    small = np.asarray(im.resize((160, 90)), dtype=np.float32) / 255.0
    mx = small.max(2)
    mn = small.min(2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    mask = ((mx > 0.35) & (sat > 0.12)) | (mx > 0.62)
    cols = mask.sum(0).astype(np.float32)
    if cols.sum() < 1:
        return 0.5
    return float((np.arange(160) * cols).sum() / cols.sum()) / 160.0


MASS = [mass_centre(p) for p in PLATES]


def push_right(arr, shift_px, plate):
    """Slide the frame right by shift_px and fill the exposed left strip.

    The gap is filled by stretching the plate's own left-edge column, which
    on these shots is unlit backdrop, so the join is invisible.
    """
    if shift_px <= 0:
        return arr
    shift_px = min(shift_px, W - 8)
    out = np.empty_like(arr)
    out[:, shift_px:] = arr[:, : W - shift_px]
    edge = arr[:, :1]                      # leftmost column of the real frame
    out[:, :shift_px] = edge               # broadcast it across the gap
    return out


def frame_for(shot_idx, local_t):
    """Render one shot at local_t in [0,1] as an HxWx3 uint8 array."""
    im = PLATES[shot_idx]
    _, z0, z1, c0, c1, target_x = SHOTS[shot_idx]
    e = ease(local_t)
    z = z0 + (z1 - z0) * e
    cx = c0[0] + (c1[0] - c0[0]) * e
    cy = c0[1] + (c1[1] - c0[1]) * e

    # Crop box: the visible window, sized by zoom, centred on (cx, cy).
    iw, ih = im.size
    # Fit the 16:9 window inside the plate at this zoom level.
    win_w = iw / z
    win_h = win_w * H / W
    if win_h > ih:
        win_h = ih / z
        win_w = win_h * W / H

    left = cx * iw - win_w / 2
    top = cy * ih - win_h / 2
    left = max(0.0, min(iw - win_w, left))
    top = max(0.0, min(ih - win_h, top))

    crop = im.resize((W, H), Image.LANCZOS,
                     box=(left, top, left + win_w, top + win_h))
    arr = np.asarray(crop, dtype=np.float32)

    # Where did the product mass actually land in this crop?
    landed = (MASS[shot_idx] * iw - left) / win_w
    shift = int(round((target_x - landed) * W))
    return push_right(arr, shift, im)


def main():
    exe = imageio_ffmpeg.get_ffmpeg_exe()

    # Vignette and a faint warm lift, baked in once. The hero copy sits on the
    # left, so the vignette is biased to darken that side a little more.
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    nx = (xx / W - 0.42) * 2.0
    ny = (yy / H - 0.5) * 2.0
    r = np.sqrt(nx * nx * 0.85 + ny * ny)
    vignette = np.clip(1.0 - 0.42 * np.clip(r - 0.35, 0, None) ** 1.6, 0.35, 1.0)
    vignette = vignette[:, :, None]

    cmd = [
        exe, "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{W}x{H}", "-r", str(FPS),
        "-i", "pipe:0",
        "-an",
        "-c:v", "libx264", "-profile:v", "high", "-preset", "slow",
        "-crf", "30", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-g", str(FPS * 2),
        os.path.join(OUT, "hero.mp4"),
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)

    for i in range(N_FRAMES):
        t = i / FPS                       # absolute time in the loop
        pos = t / STEP                    # which shot we are in, fractionally
        idx = int(math.floor(pos)) % N_SHOTS
        into = (pos - math.floor(pos)) * STEP   # seconds into this shot

        # Base shot. Its own progress spans the full SHOT window.
        a = frame_for(idx, min(1.0, into / SHOT))

        # Cross-dissolve into the next shot over the final FADE seconds.
        tail = into - (STEP - FADE)
        if tail > 0:
            nxt = (idx + 1) % N_SHOTS
            # The incoming shot has already been running for `tail` seconds.
            b = frame_for(nxt, min(1.0, tail / SHOT))
            k = ease(tail / FADE)
            a = a * (1.0 - k) + b * k

        out = np.clip(a * vignette, 0, 255).astype(np.uint8)
        proc.stdin.write(out.tobytes())

        if i % 25 == 0:
            print(f"  frame {i}/{N_FRAMES}", end="\r", flush=True)

    proc.stdin.close()
    proc.wait()
    print(f"\n  wrote hero.mp4 ({DURATION:.1f}s, {N_FRAMES} frames)")

    # WebM (VP9) — smaller, served first to browsers that take it.
    subprocess.run([
        exe, "-y", "-i", os.path.join(OUT, "hero.mp4"),
        "-an", "-c:v", "libvpx-vp9", "-crf", "42", "-b:v", "0",
        "-row-mt", "1", "-cpu-used", "2", "-pix_fmt", "yuv420p",
        os.path.join(OUT, "hero.webm"),
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print("  wrote hero.webm")

    # Poster: the first frame, so the still the user sees before playback
    # matches the video's opening exactly.
    first = np.clip(frame_for(0, 0.0) * vignette, 0, 255).astype(np.uint8)
    Image.fromarray(first).save(os.path.join(OUT, "hero-poster.jpg"),
                                quality=82, optimize=True, progressive=True)
    print("  wrote hero-poster.jpg")

    for f in ("hero.mp4", "hero.webm", "hero-poster.jpg"):
        kb = os.path.getsize(os.path.join(OUT, f)) / 1024
        print(f"    {f:18} {kb:8.0f} KB")


if __name__ == "__main__":
    main()
