# Remove the white studio background from Flow's flower images: only white connected to the image edge
# counts as background (so white frangipani petals stay), with softened, de-haloed edges.
import sys, numpy as np
from PIL import Image, ImageDraw, ImageFilter
src, dst, width = sys.argv[1], sys.argv[2], int(sys.argv[3])
# mode 'global': every white pixel is background (subjects with no white in them);
# mode 'edge': only white connected to the border, for white flowers like frangipani
mode, lo, chroma = sys.argv[4], float(sys.argv[5]), float(sys.argv[6])
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(np.float32)
mn, mx = a.min(2), a.max(2)
whiteish = (mn > lo) & (mx - mn < chroma)                     # bright and nearly colourless
m = Image.fromarray((whiteish * 255).astype(np.uint8)).copy()   # copy: an array-backed image ignores flood fill
h, w = whiteish.shape
for x in list(range(0, w, 8)):                                # flood from every white edge pixel
    for y in (0, h - 1):
        if m.getpixel((x, y)) == 255: ImageDraw.floodfill(m, (x, y), 128)
for y in list(range(0, h, 8)):
    for x in (0, w - 1):
        if m.getpixel((x, y)) == 255: ImageDraw.floodfill(m, (x, y), 128)
bg = (np.asarray(m) == 128) if mode == 'edge' else whiteish
near = np.asarray(Image.fromarray((bg * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))) > 0
alpha = np.where(bg, 0.0, 1.0)
edge = near & ~bg                                             # anti-aliased rim: fade by how white it is
alpha[edge] = np.clip((250 - mn[edge]) / 70, 0, 1)
alpha = np.asarray(Image.fromarray((alpha * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))) / 255.0
safe = np.maximum(alpha, 1e-3)[..., None]                     # un-mix the white from semi-transparent edges
rgb = np.clip((a - (1 - alpha[..., None]) * 255) / safe, 0, 255)
out = Image.fromarray(np.dstack([rgb, alpha * 255]).astype(np.uint8), 'RGBA')
out = out.crop(out.getbbox())
out = out.resize((width, round(out.height * width / out.width)), Image.LANCZOS)
out.save(dst, 'WEBP', quality=82, method=6)
print(dst, out.size)
