# Crop and compress the pro room photos for rooms.html: (folder, file, out, aspect w/h, width, crop centre x, y)
import os
from PIL import Image, ImageOps
D = os.path.expanduser('~/Downloads'); O = '/Users/akashingoley/nirvana/assets/img/rooms'
JOBS = [
  ('Moksh', '_AKS0527-1.jpg', 'moksh-arch', 3/4, 640, .45, .5),
  ('Moksh', '_AKS0536-5.jpg', 'moksh-1', 3/2, 1600, .5, .5),
  ('Moksh', '_AKS0430-2.jpg', 'moksh-2', 4/5, 800, .5, .5),
  ('Moksh', '_AKS0542-8.jpg', 'moksh-3', 4/5, 800, .32, .5),
  ('Moksh', '_AKS0533-3.jpg', 'moksh-4', 3/2, 1400, .45, .55),
  ('go goa gone', '_AKS0500-2.jpg', 'go-goa-gone-arch', 3/4, 640, .6, .5),
  ('go goa gone', '_AKS0500-2.jpg', 'go-goa-gone-1', 3/2, 1600, .5, .5),
  ('go goa gone', '_AKS0504-4.jpg', 'go-goa-gone-2', 4/5, 800, .5, .55),
  ('go goa gone', '_AKS0518-11.jpg', 'go-goa-gone-3', 4/5, 800, .5, .5),
  ('go goa gone', '_AKS0516-9.jpg', 'go-goa-gone-4', 3/2, 1400, .5, .5),
  ('Filmy chakkar', '_AKS0487.JPG', 'filmy-chakkar-arch', 3/4, 640, .45, .5),
  ('Filmy chakkar', '_AKS0488.JPG', 'filmy-chakkar-1', 3/2, 1600, .5, .5),
  ('Filmy chakkar', '_AKS0476.JPG', 'filmy-chakkar-2', 4/5, 800, .5, .5),
  ('Filmy chakkar', '_AKS0457.JPG', 'filmy-chakkar-3', 4/5, 800, .5, .6),
  ('Filmy chakkar', '_AKS0478.JPG', 'filmy-chakkar-4', 3/2, 1400, .5, .5),
]
import sys
only = sys.argv[1:]
for folder, f, out, ar, width, cx, cy in JOBS:
    if only and out not in only: continue
    im = ImageOps.exif_transpose(Image.open(f'{D}/{folder}/{f}')).convert('RGB')
    W, H = im.size
    cw, ch = (W, round(W / ar)) if W / H < ar else (round(H * ar), H)
    x = min(max(0, round(cx * W - cw / 2)), W - cw); y = min(max(0, round(cy * H - ch / 2)), H - ch)
    im = im.crop((x, y, x + cw, y + ch)).resize((width, round(width / ar)), Image.LANCZOS)
    im.save(f'{O}/{out}.jpg', quality=80, optimize=True, progressive=True)
    print(out, im.size, os.path.getsize(f'{O}/{out}.jpg') // 1024, 'KB')
