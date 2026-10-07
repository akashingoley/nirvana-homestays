# Nirvana Homestays

Website for [Nirvana Homestays](https://maps.app.goo.gl/1t9dvzFMbX5N9JNp7), a homestay with three themed rooms in Siolim, North Goa. The layout and scroll motion are modelled on [era-residence.com](https://www.era-residence.com).

## Pages

- **`index.html`**, the home page:
  - A hero video that plays as you scroll, starting in an arch-shaped frame.
  - "Live simply" under a peach arch.
  - The three rooms in a sideways pan.
  - The balconies.
  - "Room to play": the lounge and game room.
  - Siolim and the Chapora River, nearby beaches with drive times, and a map.
  - The entrance doors opening to "Welcome to our home".
- **`rooms.html`**, the rooms page. Each room (Moksh, Go Goa Gone, Filmy Chakkar) has:
  - Its own section and background colour.
  - A motif based on its door.
  - A short description and a list of features.
  - A video tour and a photo collage.

## Stack

- Plain HTML, CSS and JavaScript. No framework, no build step.
- [GSAP](https://gsap.com) 3.13 (ScrollTrigger, SplitText) and [Lenis](https://lenis.darkroom.engineering) 1.3 for smooth scrolling, both loaded from a CDN.
- Fonts from Google Fonts:
  - Big Shoulders Display for headings.
  - Archivo for body text.
  - Mrs Saint Delafield for the script accent words.
- Every animation is turned off for visitors who have reduced motion enabled.

## Run it locally

```sh
npx http-server . -p 5173 -c-1
```

Then open http://localhost:5173.

Use a server that supports range requests, like `http-server`. The hero and doors videos jump to a new frame on every scroll step, and that needs range requests. Python's `http.server` doesn't support them.

## Project layout

```
index.html, rooms.html   the two pages
style.css, main.js       shared by both pages
assets/img/              photos, posters, flower cut-outs, map, room motifs (assets/img/rooms/)
assets/video/            hero, doors, river, room tours, lounge and game room clips
tools/                   scripts that build the assets
```

## Tools

The scripts in `tools/` rebuild the assets from the source photos and videos. The sources aren't stored in this repo. They need `ffmpeg`; `cutout.py` and `room-photos.py` also need Pillow and NumPy.

| Script | What it does |
|---|---|
| `build-room-clips.py` | Cuts the owner's walkthrough videos into looping room, lounge and game-room tours, with a shared colour grade |
| `room-photos.py` | Crops and compresses the room-page photos |
| `room-motifs.py` | Draws the three room motifs as SVG line art |
| `cutout.py` | Removes the white background from the flower images |

`CLAUDE.md` holds the working notes: the design rules, the exact encode settings for the scroll videos, and the open TODO list.

## Credits

- Map data &copy; [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors.
- Drive times were worked out from [OSRM](https://project-osrm.org) routes and are approximate.
- The hero, entrance-doors and river clips were generated with Google Flow (Veo). The room, lounge and game-room tours are cut from the owner's own walkthrough videos.
- The photos and video of the property belong to Nirvana Homestays and may not be reused without permission.
