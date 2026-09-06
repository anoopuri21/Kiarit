"""
KIARIT PHARMACEUTICALS — Hero background video generator.
Procedurally renders an abstract 'liquid gold silk' loop on deep black.
No products, no people, no text — pure luxury texture.
Perfectly seamless loop (all time terms are integer harmonics of the loop).
"""
import numpy as np, subprocess, os, math
import imageio_ffmpeg

W, H = 960, 540          # render res (upscaled to 1920x1080 by ffmpeg)
FPS = 30
SECONDS = 12
N = FPS * SECONDS
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "video")
os.makedirs(OUT, exist_ok=True)

y, x = np.mgrid[0:H, 0:W].astype(np.float32)
x = (x / W - 0.5) * 2.0
y = (y / H - 0.5) * 2.0 * (H / W)

# ---- gold palette ramp (deep black -> bronze -> gold -> pale champagne) ----
stops = np.array([
    [0.000, 0.008, 0.008, 0.012],
    [0.220, 0.055, 0.036, 0.014],
    [0.420, 0.184, 0.114, 0.031],
    [0.600, 0.478, 0.310, 0.075],
    [0.760, 0.780, 0.573, 0.196],
    [0.885, 0.949, 0.796, 0.427],
    [1.000, 1.000, 0.949, 0.812],
], dtype=np.float32)
ramp_t = np.linspace(0, 1, 1024, dtype=np.float32)
LUT = np.stack([np.interp(ramp_t, stops[:, 0], stops[:, i + 1]) for i in range(3)], 1).astype(np.float32)


def silk(t):
    """t in [0,1). Returns float field ~[0,1] shaped like flowing silk folds."""
    T = 2 * math.pi * t
    # domain warp — two loops of circular drift
    w1 = np.sin(2.1 * x + 1.3 * y + T) * 0.55 + np.cos(1.7 * y - 1.1 * x + 2 * T) * 0.35
    w2 = np.cos(1.4 * x - 2.3 * y - T) * 0.45 + np.sin(2.6 * y + 0.9 * x + 3 * T) * 0.25

    xa = x + 0.55 * w1
    ya = y + 0.55 * w2

    f = np.zeros_like(x)
    f += 0.85 * np.sin(3.2 * xa + 1.9 * ya + 1.10 * np.sin(2.0 * ya - 1.2 * xa + T) + T)
    f += 0.55 * np.sin(5.4 * ya - 2.7 * xa + 0.90 * np.cos(3.1 * xa + 2 * T) + 2 * T)
    f += 0.38 * np.sin(8.1 * xa + 4.6 * ya + 0.70 * np.sin(4.4 * ya + 3 * T) - T)
    f += 0.22 * np.sin(13.0 * ya + 7.0 * xa + 4 * T)
    f /= 2.0
    return f


def frame(i):
    t = i / N
    f = silk(t)

    # sharp specular folds: fold the field so ridges become bright gold edges
    ridge = 1.0 - np.abs(f)
    ridge = np.clip(ridge, 0, 1) ** 7.0

    body = 0.5 + 0.5 * f
    v = 0.13 * body + 0.72 * ridge

    # broad diagonal light sweep travelling across the frame (loops once)
    T = 2 * math.pi * t
    sweep = np.exp(-((x * 0.75 + y * 0.55 - 0.85 * math.sin(T)) ** 2) / 0.34)
    v += 0.20 * sweep * (0.14 + 0.86 * ridge)

    # soft warm glow core, breathing
    glow = np.exp(-((x + 0.18) ** 2 * 0.75 + (y - 0.05) ** 2 * 1.5) / 1.05)
    v += 0.085 * glow * (0.75 + 0.25 * math.cos(T))

    # vignette + left-side darkening (keeps hero text readable)
    r2 = (x * 0.72) ** 2 + (y * 1.12) ** 2
    v *= np.clip(1.10 - 0.80 * r2, 0.02, 1.10)
    v *= np.clip(0.18 + 0.95 * (x + 1.0) / 2.0, 0.12, 1.05)

    v = np.clip(v, 0, 1)
    idx = (v * 1023).astype(np.int32)
    rgb = LUT[idx]

    # floating gold dust
    rng = np.random.default_rng(7)
    P = 90
    px = rng.uniform(-1, 1, P).astype(np.float32)
    py = rng.uniform(-0.62, 0.62, P).astype(np.float32)
    ph = rng.uniform(0, 2 * math.pi, P).astype(np.float32)
    sz = rng.uniform(0.6, 1.6, P).astype(np.float32)
    dx = px + 0.055 * np.sin(T + ph)
    dy = py + 0.045 * np.cos(T + ph * 1.7)
    ix = ((dx / 2.0 + 0.5) * W).astype(np.int32)
    iy = ((dy / (2.0 * H / W) + 0.5) * H).astype(np.int32)
    a = 0.16 + 0.20 * np.sin(2 * T + ph)
    for k in range(P):
        cx, cy, s = ix[k], iy[k], sz[k]
        r = max(1, int(s))
        x0, x1 = max(0, cx - r), min(W, cx + r + 1)
        y0, y1 = max(0, cy - r), min(H, cy + r + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        rgb[y0:y1, x0:x1] += np.float32(a[k] * 0.55) * np.array([1.0, 0.86, 0.58], np.float32)

    # fine film grain
    g = (np.random.default_rng(1000 + i).random((H, W, 1)).astype(np.float32) - 0.5) * 0.028
    rgb = np.clip(rgb + g, 0, 1)
    return (rgb ** 1.18 * 255).astype(np.uint8)


exe = imageio_ffmpeg.get_ffmpeg_exe()


def encode(args, path):
    p = subprocess.Popen([exe, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", "scale=1920:1080:flags=lanczos"] + args + [path],
                         stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for i in range(N):
        p.stdin.write(frame(i).tobytes())
        if i % 30 == 0:
            print(f"  frame {i}/{N}", flush=True)
    p.stdin.close()
    p.wait()
    print(" ->", path, os.path.getsize(path) // 1024, "KB")


print("Encoding MP4 (H.264)...")
encode(["-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p",
        "-crf", "26", "-preset", "slow", "-movflags", "+faststart", "-an"],
       os.path.join(OUT, "hero.mp4"))

print("Encoding WebM (VP9)...")
encode(["-c:v", "libvpx-vp9", "-pix_fmt", "yuv420p", "-crf", "36", "-b:v", "0",
        "-row-mt", "1", "-deadline", "good", "-cpu-used", "3", "-an"],
       os.path.join(OUT, "hero.webm"))

print("Poster frame...")
p = subprocess.Popen([exe, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                      "-i", "-", "-frames:v", "1", "-vf", "scale=1920:1080:flags=lanczos",
                      "-q:v", "3", os.path.join(OUT, "hero-poster.jpg")],
                     stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
p.stdin.write(frame(0).tobytes())
p.stdin.close()
p.wait()
print("Done.")
