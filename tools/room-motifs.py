# Draws the three room motifs for rooms.html as SVG line art, each taken from the room's own door:
# Moksh's mandala sign, Go Goa Gone's Dil Chahta Hai poster, Filmy Chakkar's popcorn-and-reel poster.
# Colours work on both the light and dark themes. Run: python3 tools/room-motifs.py
import math, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'img', 'rooms')
GOLD, TERRA, ORANGE, BLUE, GREEN, CREAM, RED = '#b39a72', '#c75b3f', '#e8743b', '#3b8db0', '#7a9a5a', '#f6e7c4', '#c84b3c'

def pol(r, deg, cx=200, cy=200):
    a = math.radians(deg - 90)
    return f'{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}'

def svg(name, body, vb='0 0 400 400'):
    with open(f'{OUT}/{name}.svg', 'w') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="none" stroke-linecap="round" stroke-linejoin="round">\n{body}\n</svg>\n')
    print(name)

# Moksh: two overlapping petal rings around a double circle, dotted lobes, a terracotta lotus in the corner
n, d = 16, 360 / 16 / 2
parts = []
for i in range(n):
    a = i * 360 / n
    parts.append(f'<path d="M{pol(118, a - d)} C{pol(178, a - d * 1.15)} {pol(178, a + d * 1.15)} {pol(118, a + d)}"/>')   # rounded outer lobe
    b = a + d
    parts.append(f'<path d="M{pol(80, b - d)} C{pol(112, b - d * 1.25)} {pol(128, b - d * .45)} {pol(150, b)} C{pol(128, b + d * .45)} {pol(112, b + d * 1.25)} {pol(80, b + d)}"/>')   # pointed inner petal
    for r, off in [(152, 0), (140, -.42), (140, .42)]:
        x, y = pol(r, a + off * d).split(',')
        parts.append(f'<circle cx="{x}" cy="{y}" r="2.3" fill="{GOLD}" stroke="none"/>')
lotus = []
for k, ang in enumerate([6, 26, 46, 66, 84]):   # petals fan down and right from the top-left corner, as on the door
    lotus.append(f'<path transform="translate(22 18) rotate({ang})" d="M0,0 C20,-16 72,-14 112,0 C72,14 20,16 0,0Z" fill="{TERRA}" fill-opacity="{.5 + k * .1:.2f}" stroke="{TERRA}" stroke-width="1.5"/>')
svg('motif-moksh', f'<g stroke="{GOLD}" stroke-width="2.4">\n' + '\n'.join(parts) +
    f'\n<circle cx="200" cy="200" r="80"/><circle cx="200" cy="200" r="72"/></g>\n'
    f'<text x="200" y="209" text-anchor="middle" font-family="Helvetica Neue, Arial, sans-serif" font-size="25" letter-spacing="5" fill="{GOLD}">MOKSH</text>\n<g>' + ''.join(lotus) + '</g>')

# Go Goa Gone: a round "trip to Goa" badge with the poster's line running round the rim, an orange sun setting over the sea, palms
quote = 'HUM LOGO KO SAL ME EK BAR GOA JAROOR JANA CHAIYE  •  DIL CHAHTA HAI  •  '
fronds = lambda x, y, s, flip=1: ''.join(
    f'<path d="M{x},{y} q{flip * dx * s:.0f},{dy * s:.0f} {flip * ex * s:.0f},{ey * s:.0f}"/>'
    for dx, dy, ex, ey in [(30, -22, 62, 4), (24, -30, 44, -38), (-6, -34, -30, -40), (-28, -18, -58, 6), (-14, -8, -38, 26), (16, -6, 40, 28)])
body = f'''<defs><path id="rim" d="M200,200 m-168,0 a168,168 0 1,1 336,0 a168,168 0 1,1 -336,0"/>
<clipPath id="inside"><circle cx="200" cy="200" r="146"/></clipPath><clipPath id="sky"><rect x="0" y="0" width="400" height="240"/></clipPath></defs>
<text font-family="Arial Narrow, Helvetica Neue, Arial, sans-serif" font-size="15.5" font-weight="700" fill="{GOLD}"><textPath href="#rim" textLength="1040" lengthAdjust="spacing">{quote}</textPath></text>
<circle cx="200" cy="200" r="150" stroke="{GOLD}" stroke-width="2.4"/>
<g clip-path="url(#inside)">
  <circle cx="200" cy="238" r="74" fill="{ORANGE}" clip-path="url(#sky)"/>   <!-- half a sun, setting -->
  <rect x="40" y="238" width="320" height="140" fill="{BLUE}" fill-opacity=".28"/>
  <path d="M176,252 h48 M184,262 h32 M192,272 h16" stroke="{ORANGE}" stroke-width="3"/>   <!-- its reflection -->
  <g stroke="{BLUE}" stroke-width="3">
    <path d="M40,244 q20,-8 40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0"/>
    <path d="M60,270 q20,-8 40,0 t40,0 t40,0 t40,0 t40,0 t40,0 t40,0"/>
    <path d="M80,296 q20,-8 40,0 t40,0 t40,0 t40,0 t40,0 t40,0"/>
  </g>
  <g stroke="{GREEN}" stroke-width="3.2">
    <path d="M104,352 C110,300 108,250 122,186"/>{fronds(122, 186, 1)}
    <path d="M300,352 C296,312 300,280 290,232"/>{fronds(290, 232, .75, -1)}
  </g>
</g>'''
svg('motif-go-goa-gone', body)

# Filmy Chakkar: a film reel with a strip of film, and a striped popcorn bucket in front, as on the door poster
holes = ''.join(f'<circle cx="{pol(66, a, 180, 165).split(",")[0]}" cy="{pol(66, a, 180, 165).split(",")[1]}" r="25"/>' for a in range(0, 360, 60))
sprockets = ''.join(f'<rect x="{x}" y="-15" width="11" height="7" rx="1.5"/><rect x="{x}" y="8" width="11" height="7" rx="1.5"/>' for x in range(-150, 150, 22))
stripes = ''.join(f'<rect x="{252 + i * 18}" y="230" width="18" height="150" fill="{RED if i % 2 == 0 else CREAM}"/>' for i in range(7))
kernels = [(268, 228, 15), (290, 214, 17), (316, 210, 16), (342, 220, 15), (360, 236, 13), (254, 244, 12), (304, 230, 14), (330, 236, 13), (282, 238, 12)]
pop = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in kernels)
body = f'''<defs><clipPath id="bucket"><path d="M250,244 L370,244 L352,382 L268,382Z"/></clipPath></defs>
<g transform="translate(190 330) rotate(-14)" stroke="{GOLD}" stroke-width="2.4">
  <rect x="-170" y="-24" width="340" height="48" rx="4"/><g fill="{GOLD}" fill-opacity=".35">{sprockets}</g>
  <path d="M-58,-24 V24 M58,-24 V24"/>
</g>
<g stroke="{GOLD}" stroke-width="3">
  <circle cx="180" cy="165" r="122"/><circle cx="180" cy="165" r="112" stroke-width="1.6"/>
  {holes}<circle cx="180" cy="165" r="14"/><circle cx="180" cy="165" r="4" fill="{GOLD}"/>
</g>
<g stroke="{GOLD}" stroke-width="2">{pop.replace('/>', f' fill="{CREAM}"/>')}</g>
<g clip-path="url(#bucket)">{stripes}</g>
<path d="M250,244 L370,244 L352,382 L268,382Z" stroke="{GOLD}" stroke-width="2.4"/>
<path d="M246,244 H374" stroke="{GOLD}" stroke-width="5"/>'''
svg('motif-filmy-chakkar', body, '0 0 400 400')
