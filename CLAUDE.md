# Nirvana Homestays website

Scroll-driven landing page for Nirvana Homestays, an Airbnb homestay in Siolim, North Goa. The layout and motion are modelled on https://www.era-residence.com.

## Stack
- Plain `index.html` + `style.css` + `main.js`. No build step, no framework.
- GSAP 3.13 (ScrollTrigger, SplitText) and Lenis 1.3, loaded from CDN.
- Fonts (Google): Big Shoulders Display for headings, Archivo (expanded width) for body text, Mrs Saint Delafield for one script accent word per headline (`.script`, written in by `[data-write]`). Its capital G reads like an S, so avoid G at small sizes.
- Local preview: `npx http-server . -p 5173 -c-1`. Needs a server that supports range requests so the hero video can seek; plain `python -m http.server` doesn't.

## Design
- Palette from the logo (`assets/img/logo.png`): peach `#f0c0a0`, forest green `#26331f`, dark frame `#1b2516`, and peacock blue `#1f6e8f` as the only accent, plus a pale peacock tint `--sky` (`#dce8ea`) as the colour block behind "Room to play". Dark mode via `prefers-color-scheme`.
- Buttons are pills; images have square corners. The hero and closing frames start as arch-topped windows (`inset(... round 999px 999px 0 0)`) echoing the peach arch.
- Flower cut-outs (`assets/img/flower-*.webp`, from Flow on white) spill over section edges and sway on scroll (`.flora`, `[data-drift]`). Make new ones with `tools/cutout.py <in> <out.webp> <width> global|edge <min-brightness> <max-chroma>` (needs Pillow + numpy): `global 228 22` for plants with no white in them, `edge 247 8` for white flowers like frangipani.
- All footage shares one warm grade (`GRADE` in `tools/build-room-clips.py`); the hero also gets `eq=gamma=1.12`.
- No em-dashes in copy. No section-number labels or scroll cues.
- Every animation is skipped under `prefers-reduced-motion`.

## Sections (in order)
1. Hero: a 16 s video (`assets/video/hero.mp4`) that plays in step with scrolling, framed by an arch-topped inset that opens to full screen. Two lines (`.hero-line`) fade in and out over the balcony part of the glide.
2. "Live simply": a peach arch rises over the hero; the "Live Simply" cushion photo sits in a smaller arch below the text.
3. Rooms (Moksh, Go Goa Gone, Filmy Chakkar): pinned horizontal pan on desktop, stacked on mobile. Each card is a landscape looping tour (door, room, a signature detail, bathroom, balcony) cut from the owner's walkthrough videos by `tools/build-room-clips.py` (`python3 tools/build-room-clips.py [name ...]`). Landscape clips are 1600×900; the tall lounge tile is a 864×1080 crop at the source's full height with a crop centre per shot, because upscaling a landscape clip into a tall tile is what made it pixelated; it plays only while on screen.
4. Balconies: full-bleed golden-hour photo (a Flow edit of the pro shot) that settles from a zoom.
5. "Room to play": 4-cell grid (lounge, foosball, darts, board games). Tiles drift at different speeds (`data-depth`). A small overhead balcony photo hangs over the edge from the Balconies section above. The lounge (tall) and game room (wide) cells are looping clips (`common-area.mp4`, `game-room.mp4`, also built by `tools/build-room-clips.py`); darts and board games are photos.
6. Siolim: drifting place names, plus a looping Chapora River clip (`assets/video/chapora-river.mp4`) and short text. Then "Around *the stay*": the coast as a wavy line with a stop per beach (Arambol, Mandrem, Ashwem, Morjim, Nirvana inland, Chapora Fort, Vagator, Anjuna) and an "Also nearby" list. Distances are OSRM driving routes from the pin; times are those routes x ~1.5 for Goa traffic, rounded up to 5 min. Then "Find *us here*": the address, "Get directions" and "Open in Google Maps" buttons, and a still map (`assets/img/map-siolim.jpg`, 1120×1400, stitched once from OpenStreetMap zoom-14 tiles covering Arambol to Anjuna and tinted in CSS; keep the OSM credit) with a pulsing logo pin and a dot per place (positions in % from web-mercator maths), linking to the Google Maps listing. On desktop both blocks sit in one `.around` grid: the list on the left, the map and address on the right; the map is sticky and sized to the screen height, and hovering a list item lights its map dot, draws a dashed route from the pin and adds the drive time to the label (`data-place`, `initPlaceLinks`). `.siolim` must use `overflow-x: clip`, not `overflow: hidden`, or the sticky map stops working. Phones stack them.
7. Book: the entrance doors (`assets/video/entrance-doors.mp4`) open as you scroll inside a frame that widens to full screen, then the logo and closing line appear.

## Rooms page (`rooms.html`)
Shares `style.css` and `main.js` (section effects in `init()` only run where their section exists). Dark intro with three arch thumbnails linking to `#moksh`, `#go-goa-gone`, `#filmy-chakkar`; then one section per room (paper, sky, peach backgrounds): title with a script tagline, the room's door motif (SVG line art from `tools/room-motifs.py`: Moksh mandala, Go Goa Gone sunset badge with the Dil Chahta Hai line, Filmy Chakkar reel and popcorn), description, feature pills, the room's tour clip, and a 4-photo collage (`assets/img/rooms/<room>-1..4.jpg`, cut from the pro photos by `tools/room-photos.py`). Ends on a dark "The rest of *the home*" band linking back to the home page. Home page room cards link here ("Explore Moksh"). Flowers sit at the top-left of each tour video; never over the text. Links into the home page (`index.html#spaces`) are re-scrolled after init, because the room pan's pin is added after the browser's own hash jump.

## Property facts (from the owner's videos)
- Address: House no 451/4, Tarchi Bhat, behind Babaji Cold Drinks, near Siolim Deck, Siolim, Goa 403517. Google Maps: https://maps.app.goo.gl/1t9dvzFMbX5N9JNp7 (pin 15.630169, 73.76685).
- Themed bedrooms: Moksh (zen, Buddha, rattan lamp, lapis-blue marble and Moroccan-tile bathroom), Go Goa Gone (Dil Chahta Hai poster on the door), Filmy Chakkar (Bollywood poster wall, green marble bathroom).
- Common area (cane chairs, board games) and a game room (foosball, darts, movie posters).
- Every room has a private balcony with white wicker chairs.
- **No pool of any kind.** Never show or mention one.
- No exterior photos yet; the owner will provide them.

## Assets
- Source videos: `~/Downloads/*.mp4` (full walkthrough plus one per room).
- Pro photos (6000×4000, some portrait via EXIF, so crop with ffmpeg, not sips): `~/Downloads/{Moksh,go goa gone,Filmy chakkar,Common room,Game room,Hall Room}/`. Hall Room is the gramophone lounge; its first two shots are the teak entrance door.
- Reference stills for Google Flow: `~/Downloads/flow-reference-frames/<space>/`, 16:9 crops of the pro photos.
- Flow prompt pack and status: `~/Downloads/flow-prompts.md`.
- Flow exports: `~/Downloads/flow-exports/`. `hero-scroll_master.mp4` is the full-quality hero: `hero-a.mp4` + `hero-b3.mp4` joined, with the Veo watermark removed (`delogo=x=1820:y=1025:w=90:h=45`). The earlier version is `hero-scroll_master_v1.mp4`.
- Scroll-scrubbed videos (hero, entrance doors) come in two sizes, picked by `<source media>`: desktop 1600 px crf 28 (doors 1920 px crf 25), phones `*-mobile.mp4` 1280 px crf 31. The phone doors clip is instead a tall 672×1080 crop (crf 25) whose x follows the seam between the door leaves (0.548 of the width while closed; the darkest column is a groove beside the right leaf, not the seam), then the middle of the doorway (0.545 → 0.54 → 0.49 → 0.50), so the doors stay centred on a portrait screen. Encode: `ffmpeg -i <master> -vf "<GRADE>[,eq=gamma=1.12 hero only],unsharp=5:5:0.5,scale=<w>:-2" -an -c:v libx264 -preset slow -g 10 -keyint_min 10 -sc_threshold 0 -pix_fmt yuv420p -movflags +faststart -crf <q> <out>`. Keep every option before the output file: options after it are silently ignored, which once left these videos with a keyframe only every 250 frames and made scrubbing lag. Check with `ffprobe -skip_frame nokey` that keyframes are 10 frames apart.
- `scrubVideo()` in `main.js` seeks only when the previous seek has finished; setting `currentTime` every tick queues seeks and the video falls behind the scroll. The hero's softness comes from Veo's 1080p output, not the encode.

## Working with Google Flow
- Use the agent chat, attach a still with "+", and say "use this image as the exact first frame".
- The video model ignores "static camera", so describe a camera move instead. To build a longer shot, start the next clip on the last frame of the previous one.
- It adds plunge pools to Goa balconies unless told "no pool, plunge pool, jacuzzi or water". Check every take. Even then it can turn the blue tarpaulin roof below the balconies into water; giving it a clean last frame as well as a first frame is what stops it.
- To join two takes, start the second from the first take's actual last frame (saved in the reference folder as `*_last-frame.jpg`), not from the original photo.
- Exports include a "Veo" watermark in the bottom-right corner. Crop or blur it out.

## TODO
- [x] Siolim image → Chapora River clip from Flow
- [x] Room clips replace the room photos (Moksh from Flow; Filmy Chakkar and Go Goa Gone cut from the owner's walkthroughs)
- [ ] Exterior photos → exterior hero / day-to-night clip
- [x] Smaller hero video for mobile
- [ ] Owner to confirm the drive times in "Around the stay"
- [ ] Owner to confirm the room descriptions and the feature pills on `rooms.html` (AC, TV, mini fridge and kettle, wardrobe were read off the walkthrough videos)
- [ ] Swap the Moksh and game-room photos on the site for the pro shots
