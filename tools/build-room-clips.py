# Cut the owner's walkthrough videos into short multi-shot loops (rooms, lounge and game room): shots joined by 0.4 s dissolves,
# and the end dissolves back into the start so the loop has no visible seam.
# Usage: python3 build-room-clips.py [name ...]   (no names = rebuild all)
import subprocess, os, sys
D = os.path.expanduser("~/Downloads")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
FADE, LOOP = 0.4, 0.8
# Shared warm grade (also used for the hero and doors clips): warmer mids, softer highlights, a little more colour
GRADE = "colorbalance=rs=0.03:bs=-0.04:rm=0.04:bm=-0.03:rh=0.02:bh=-0.02,curves=all='0/0.02 0.5/0.52 0.85/0.82 1/0.93',eq=saturation=1.1"
WIDE = (1600, 900)      # landscape tiles (room cards, game room); sharp enough for 2x screens at card size
TALL = (864, 1080)      # the tall lounge tile: a 4:5 crop at the source's full 1080 px height, never upscaled
# Each shot is (start, end) or (start, end, x) where x is the crop centre as a fraction of the width (TALL clips only)
CLIPS = {
    "room-moksh": ("Moksh.mp4", WIDE, [(0.1, 1.8), (2.0, 5.0), (6.1, 7.4), (35.2, 38.2), (12.0, 13.9), (54.0, 57.5)]),
    "room-go-goa-gone": ("Go goa gone.mp4", WIDE, [(0.5, 3.5), (5.6, 8.2), (44.1, 45.9), (33.6, 35.9), (48.1, 49.9), (36.1, 38.9)]),
    "room-filmy-chakkar": ("Filmy chakkar.mp4", WIDE, [(0.05, 2.1), (9.3, 12.3), (39.1, 41.4), (21.2, 22.9), (35.1, 37.4), (30.1, 31.9), (48.5, 50.8)]),
    "common-area": ("common area.mp4", TALL, [(2.1, 3.8, 0.42), (26.0, 28.1, 0.55), (18.3, 20.1, 0.42), (20.3, 22.1, 0.6), (32.0, 35.5, 0.62)]),
    "game-room": ("game room.mp4", WIDE, [(0.1, 2.1), (2.3, 4.1), (4.3, 6.1), (18.7, 20.6), (23.5, 25.9)]),
}

def frame(size, shot):
    w, h = size
    if w / h >= 16 / 9:
        return f"scale={w}:{h}"
    x = shot[2] if len(shot) > 2 else 0.5
    cw = round(1080 * w / h)   # crop the tall shape straight from the 1080p source
    return f"crop={cw}:1080:'min(max(0,{x}*iw-{cw / 2}),iw-{cw})':0,scale={w}:{h}"

for name in sys.argv[1:] or CLIPS:
    src, size, shots = CLIPS[name]
    parts = [f"[0]trim={s[0]}:{s[1]},setpts=PTS-STARTPTS,{GRADE},{frame(size, s)},fps=24,format=yuv420p[s{i}]" for i, s in enumerate(shots)]
    cur, length = "s0", shots[0][1] - shots[0][0]
    for i in range(1, len(shots)):
        parts.append(f"[{cur}][s{i}]xfade=transition=fade:duration={FADE}:offset={length - FADE:.3f}[j{i}]")
        cur, length = f"j{i}", length - FADE + shots[i][1] - shots[i][0]
    parts.append(f"[{cur}]split[x][y];[x]trim=0:{LOOP},setpts=PTS-STARTPTS[a];[y]trim={LOOP},setpts=PTS-STARTPTS[b];"
                 f"[b][a]xfade=transition=fade:duration={LOOP}:offset={length - 2 * LOOP:.3f},format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{D}/{src}", "-filter_complex", ";".join(parts),
                    "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "slow", "-crf", "25" if size == TALL else "27", "-movflags", "+faststart",
                    f"{OUT}/video/{name}.mp4"], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{OUT}/video/{name}.mp4", "-frames:v", "1", "-q:v", "3", f"{OUT}/img/{name}.jpg"], check=True)
    dur = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{OUT}/video/{name}.mp4"]).decode().strip()
    print(name, f"{size[0]}x{size[1]}", dur, os.path.getsize(f"{OUT}/video/{name}.mp4") // 1024, "KB")
