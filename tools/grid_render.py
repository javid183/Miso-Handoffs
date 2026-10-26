#!/usr/bin/env python3
"""Draw level chunks written as text grids.

Usage:
    python grid_render.py <doc.md> [--out <folder>]

Finds every fenced block whose info string starts with `grid`, for example

    ```grid id=bell title="The bell"
    # . c b c . #
    # . . . . . #
    # J U . . L #
    --
    arrow 1,0 4,2 john ring the bell
    zone 2,1 4,2 enemy pack range
    step 4,2 1
    ```

and writes <out>/<id>.svg for each one, plus <out>/index.html with all of them.
<out> defaults to a folder next to the doc, named after it.

Coordinates: x counts from 0 at the left, y from 0 at the BOTTOM row (as Unity's
grid does). Every tile shows its x,y; hovering a tile shows it too.

Cells are separated by spaces. A cell is one terrain character, one unit
character, or both (`c^` = a Dark Claw on spikes, `J@` = John on the key tile).

Terrain:  .  floor    #  rock    _  no tile (gap)    ^  spikes
          P  Corruption pool (spawner)    E  exit / goal    @  key tile    ~  Cyclone
          %  spider web    *  exploding mushroom    !  trap    &  poison pool
          ?  marked tile (the Deev's poison drops here next enemy turn)
Family:   J John   L Linda   U Lucy   M Mark   T Toba
Others:   c Dark Claw   b Black Claw   s Shaman   w Worm      (dark brood: diamonds)
          a Archer   O Masher (four O make its 2 x 2)          (goblins: other shapes)
          D Mountain Deev (six D make its 3 x 2)
          R protectee   d decoy

Annotations, one per line after a `--` line inside the block:
    arrow X,Y X,Y [X,Y ...] [colour] [dx=N dy=N] [label]
                                               a path through tile centres; dx/dy shift it
                                               by N pixels (to draw two arrows on one lane)
    zone  X1,Y1 X2,Y2 [colour] [label]         a tinted rectangle of tiles
    cells X,Y X,Y ... [colour] [label]         tinted single tiles
    range X,Y R [colour] [label]               tints every walkable tile within R steps
                                               (four-way, like most ranges in the game)
    step  X,Y N                                a numbered badge
    note  X,Y text                             a short label on a tile
Colours: john linda lucy mark toba enemy heal shaman note, or #rrggbb.

No dependencies beyond the Python standard library.
"""
import html
import os
import re
import sys

TILE = 46
PAD = 26  # room for the axis labels

FAMILY = {
    'J': ('John', '#5a3d1f'),
    'L': ('Linda', '#2f86b8'),
    'U': ('Lucy', '#b32424'),
    'M': ('Mark', '#1b1b1b'),
    'T': ('Toba', '#3f7f3a'),
}
OTHERS = {
    'c': ('Dark Claw', '#d9822b'),
    'b': ('Black Claw', '#6e2c00'),
    'a': ('Archer', '#c0532a'),
    's': ('Shaman', '#7d3c98'),
    'w': ('Worm', '#7f8c6d'),
    'R': ('Protectee', '#d4a017'),
    'd': ('Decoy', '#9aa0a6'),
}
TERRAIN = {
    '.': ('Floor', '#ece6d8'),
    '#': ('Rock', '#6f675c'),
    '_': ('Gap', None),
    '^': ('Spikes', '#ece6d8'),
    'P': ('Corruption pool', '#ece6d8'),
    'E': ('Exit / goal', '#bfe3a5'),
    '@': ('Key tile', '#ece6d8'),
    '~': ('Cyclone', '#ece6d8'),
    '%': ('Spider web', '#ece6d8'),
    '*': ('Exploding mushroom', '#ece6d8'),
    '!': ('Trap', '#ece6d8'),
    '&': ('Poison pool', '#ece6d8'),
    '?': ('Marked: poison drops next enemy turn', '#ece6d8'),
}
DARK_BROOD = set('cbsw')
BIG = {
    'O': ('Masher', '#7b241c'),
    'D': ('Deev', '#34495e'),
}
COLOURS = {
    'john': '#5a3d1f', 'linda': '#2f86b8', 'lucy': '#b32424', 'mark': '#1b1b1b',
    'toba': '#3f7f3a', 'enemy': '#d35400', 'note': '#6c4fc4', 'heal': '#2e9e4f',
    'shaman': '#7d3c98',
}
COORD = re.compile(r'^-?\d+,-?\d+$')


def colour_of(tok):
    if tok is None:
        return None
    if tok.lower() in COLOURS:
        return COLOURS[tok.lower()]
    if re.fullmatch(r'#[0-9a-fA-F]{6}', tok):
        return tok
    return None


def parse_blocks(text):
    blocks = []
    for m in re.finditer(r'^```grid([^\n]*)\n(.*?)^```', text, re.S | re.M):
        info, body = m.group(1), m.group(2)
        bid = re.search(r'id=(\S+)', info)
        title = re.search(r'title="([^"]*)"', info)
        if not bid:
            print('warning: a grid block has no id=, skipped', file=sys.stderr)
            continue
        parts = re.split(r'^--\s*$', body, maxsplit=1, flags=re.M)
        rows = [r.split() for r in parts[0].splitlines() if r.strip()]
        notes = [l.strip() for l in parts[1].splitlines() if l.strip()] if len(parts) > 1 else []
        blocks.append({'id': bid.group(1), 'title': title.group(1) if title else bid.group(1),
                       'rows': rows, 'notes': notes})
    return blocks


def split_cell(tok):
    terrain, unit = '.', None
    for ch in tok:
        if ch in TERRAIN:
            terrain = ch
        elif ch in FAMILY or ch in OTHERS or ch in BIG:
            unit = ch
        else:
            raise ValueError(f'unknown cell character {ch!r} in {tok!r}')
    return terrain, unit


class Grid:
    def __init__(self, block):
        self.id, self.title, self.notes = block['id'], block['title'], block['notes']
        rows = block['rows']
        self.h = len(rows)
        self.w = max(len(r) for r in rows)
        for i, r in enumerate(rows):
            if len(r) != self.w:
                print(f'warning: {self.id}: row {i} (y={self.h - 1 - i}) has {len(r)} cells, '
                      f'expected {self.w}', file=sys.stderr)
        self.cells = {}
        for i, r in enumerate(rows):
            y = self.h - 1 - i
            for x, tok in enumerate(r):
                self.cells[(x, y)] = split_cell(tok)

    # tile (x, y) -> top-left pixel
    def px(self, x, y):
        return PAD + x * TILE, PAD + (self.h - 1 - y) * TILE

    def centre(self, x, y):
        a, b = self.px(x, y)
        return a + TILE / 2, b + TILE / 2


def text(x, y, s, size=11, fill='#222', anchor='middle', weight='normal', halo=False):
    common = (f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" '
              f'font-family="Segoe UI, Helvetica, Arial, sans-serif"')
    body = html.escape(str(s))
    under = (f'<text {common} fill="#ffffff" stroke="#ffffff" stroke-width="3.5" stroke-linejoin="round">{body}</text>'
             if halo else '')
    return f'{under}<text {common} fill="{fill}">{body}</text>'


def render(g):
    W = g.w * TILE + 2 * PAD
    H = g.h * TILE + 2 * PAD
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" '
           'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker>'
           '<pattern id="gap" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<line x1="0" y1="0" x2="0" y2="8" stroke="#c9c2b4" stroke-width="2"/></pattern></defs>',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    # axis labels
    for x in range(g.w):
        cx = PAD + x * TILE + TILE / 2
        out.append(text(cx, PAD - 9, x, 11, '#777'))
        out.append(text(cx, H - PAD + 17, x, 11, '#777'))
    for y in range(g.h):
        cy = PAD + (g.h - 1 - y) * TILE + TILE / 2 + 4
        out.append(text(PAD - 10, cy, y, 11, '#777'))
        out.append(text(W - PAD + 10, cy, y, 11, '#777'))

    # terrain
    for (x, y), (ter, unit) in g.cells.items():
        a, b = g.px(x, y)
        name, fill = TERRAIN[ter]
        tip = f'<title>{x},{y}  {name}</title>'
        if ter == '_':
            out.append(f'<g><rect x="{a}" y="{b}" width="{TILE}" height="{TILE}" fill="url(#gap)" '
                       f'stroke="#e2dccf" stroke-width="1"/>{tip}</g>')
            continue
        out.append(f'<g><rect x="{a}" y="{b}" width="{TILE}" height="{TILE}" fill="{fill}" '
                   f'stroke="#cfc7b6" stroke-width="1"/>{tip}</g>')
        if ter == '^':
            for i in range(3):
                sx = a + 7 + i * 11
                out.append(f'<path d="M{sx},{b + TILE - 8} L{sx + 5.5},{b + TILE - 22} L{sx + 11},{b + TILE - 8} z" '
                           f'fill="#c0392b" opacity="0.85"/>')
        elif ter == 'P':
            out.append(f'<circle cx="{a + TILE / 2}" cy="{b + TILE / 2}" r="16" fill="#5b2c6f" opacity="0.85"/>')
            if not unit:
                out.append(text(a + TILE / 2, b + TILE / 2 + 4, 'P', 12, '#fff', weight='bold'))
        elif ter == '@':
            out.append(f'<rect x="{a + 2.5}" y="{b + 2.5}" width="{TILE - 5}" height="{TILE - 5}" fill="none" '
                       f'stroke="#e6b800" stroke-width="3" stroke-dasharray="5 3"/>')
        elif ter == '~':
            out.append(f'<circle cx="{a + TILE / 2}" cy="{b + TILE / 2}" r="17" fill="none" stroke="#e67e22" '
                       f'stroke-width="2.5" stroke-dasharray="14 5"/>')
            out.append(f'<circle cx="{a + TILE / 2}" cy="{b + TILE / 2}" r="9" fill="none" stroke="#e67e22" '
                       f'stroke-width="2" stroke-dasharray="8 4"/>')
        elif ter == 'E' and not unit:
            out.append(text(a + TILE / 2, b + TILE / 2 + 4, 'E', 12, '#2e6b14', weight='bold'))
        elif ter == '%':
            cx, cy = a + TILE / 2, b + TILE / 2
            for dx, dy in ((1, 0), (0, 1), (0.7, 0.7), (0.7, -0.7)):
                out.append(f'<line x1="{cx - dx * 19:.1f}" y1="{cy - dy * 19:.1f}" x2="{cx + dx * 19:.1f}" '
                           f'y2="{cy + dy * 19:.1f}" stroke="#8a8a8a" stroke-width="1"/>')
            for r in (6, 12, 18):
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#8a8a8a" stroke-width="1"/>')
        elif ter == '*':
            cx, cy = a + TILE / 2, b + TILE / 2
            out.append(f'<rect x="{cx - 4}" y="{cy}" width="8" height="12" rx="2" fill="#efe3c8" stroke="#8a6d3b"/>')
            out.append(f'<path d="M{cx - 15},{cy + 2} Q{cx},{cy - 22} {cx + 15},{cy + 2} z" fill="#c0392b" '
                       f'stroke="#7b1f16"/>')
            for ox, oy in ((-6, -6), (4, -9), (7, -2)):
                out.append(f'<circle cx="{cx + ox}" cy="{cy + oy}" r="2.2" fill="#fff"/>')
        elif ter == '!':
            cx, cy = a + TILE / 2, b + TILE / 2
            out.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="#5d6d7e" stroke-width="3"/>')
            teeth = ' '.join(f'M{cx - 12 + i * 6},{cy - 3} l3,6 l3,-6' for i in range(4))
            out.append(f'<path d="{teeth}" fill="none" stroke="#5d6d7e" stroke-width="2"/>')
        elif ter == '?':
            out.append(f'<rect x="{a + 3}" y="{b + 3}" width="{TILE - 6}" height="{TILE - 6}" fill="#f4d03f" '
                       f'fill-opacity="0.35" stroke="#b9770e" stroke-width="2.5" stroke-dasharray="3 3"/>')
            if not unit:
                out.append(text(a + TILE / 2, b + TILE / 2 + 5, '!', 15, '#b9770e', weight='bold'))
        elif ter == '&':
            cx, cy = a + TILE / 2, b + TILE / 2
            out.append(f'<ellipse cx="{cx}" cy="{cy + 2}" rx="18" ry="12" fill="#7dbb3a" opacity="0.75"/>')
            out.append(f'<circle cx="{cx - 6}" cy="{cy}" r="2.5" fill="#d9f0b8"/>'
                       f'<circle cx="{cx + 5}" cy="{cy + 4}" r="2" fill="#d9f0b8"/>')
        out.append(text(a + 3, b + TILE - 3, f'{x},{y}', 8, '#a39b8c', anchor='start'))

    # zones and cells (under units)
    for line in g.notes:
        p = line.split()
        if p[0] == 'range' and len(p) >= 3 and COORD.match(p[1]):
            ox, oy = map(int, p[1].split(','))
            rad = int(p[2])
            rest = p[3:]
            col = colour_of(rest[0]) if rest else None
            label = ' '.join(rest[1:] if col else rest)
            col = col or COLOURS['note']
            tiles = [(x, y) for (x, y), (ter, _) in g.cells.items()
                     if ter not in '#_' and 0 < abs(x - ox) + abs(y - oy) <= rad]
            for (x, y) in tiles:
                a, b = g.px(x, y)
                out.append(f'<rect x="{a + 1}" y="{b + 1}" width="{TILE - 2}" height="{TILE - 2}" fill="{col}" '
                           f'fill-opacity="0.13"/>')
            # outline the outer edge of the range
            tset = set(tiles) | {(ox, oy)}
            for (x, y) in tiles:
                a, b = g.px(x, y)
                for (nx, ny), seg in (((x, y + 1), (a, b, a + TILE, b)), ((x, y - 1), (a, b + TILE, a + TILE, b + TILE)),
                                      ((x - 1, y), (a, b, a, b + TILE)), ((x + 1, y), (a + TILE, b, a + TILE, b + TILE))):
                    if (nx, ny) not in tset:
                        out.append(f'<line x1="{seg[0]}" y1="{seg[1]}" x2="{seg[2]}" y2="{seg[3]}" stroke="{col}" '
                                   f'stroke-width="2" stroke-dasharray="4 3"/>')
            if label and tiles:
                lx, ly = max(tiles, key=lambda t: (t[1], -t[0]))
                a, b = g.px(lx, ly)
                out.append(text(a + 4, b + 12, label, 10, col, anchor='start', weight='bold', halo=True))
        elif p[0] in ('zone', 'cells'):
            coords = [tuple(map(int, t.split(','))) for t in p[1:] if COORD.match(t)]
            rest = [t for t in p[1:] if not COORD.match(t)]
            col = colour_of(rest[0]) if rest else None
            label = ' '.join(rest[1:] if col else rest)
            col = col or COLOURS['note']
            if p[0] == 'zone' and len(coords) == 2:
                (x1, y1), (x2, y2) = coords
                xa, xb = sorted((x1, x2)); ya, yb = sorted((y1, y2))
                a, _ = g.px(xa, yb); _, b = g.px(xa, yb)
                w = (xb - xa + 1) * TILE; h = (yb - ya + 1) * TILE
                out.append(f'<rect x="{a + 1}" y="{b + 1}" width="{w - 2}" height="{h - 2}" fill="{col}" '
                           f'fill-opacity="0.16" stroke="{col}" stroke-width="2" stroke-dasharray="6 4"/>')
                if label:
                    out.append(text(a + 4, b + 12, label, 10, col, anchor='start', weight='bold', halo=True))
            else:
                for (x, y) in coords:
                    a, b = g.px(x, y)
                    out.append(f'<rect x="{a + 1}" y="{b + 1}" width="{TILE - 2}" height="{TILE - 2}" fill="{col}" '
                               f'fill-opacity="0.22" stroke="{col}" stroke-width="1.5"/>')
                if label and coords:
                    a, b = g.px(*coords[0])
                    out.append(text(a + 4, b + 12, label, 10, col, anchor='start', weight='bold', halo=True))

    # big units (Masher 2 x 2, Mountain Deev 3 x 2): one block per connected group
    seen = set()
    for (x, y), (_, unit) in sorted(g.cells.items()):
        if unit not in BIG or (x, y) in seen:
            continue
        stack, group = [(x, y)], []
        while stack:
            c = stack.pop()
            if c in seen or g.cells.get(c, (None, None))[1] != unit:
                continue
            seen.add(c); group.append(c)
            stack += [(c[0] + 1, c[1]), (c[0] - 1, c[1]), (c[0], c[1] + 1), (c[0], c[1] - 1)]
        name, col = BIG[unit]
        xs = [c[0] for c in group]; ys = [c[1] for c in group]
        a, b = g.px(min(xs), max(ys))
        w = (max(xs) - min(xs) + 1) * TILE; h = (max(ys) - min(ys) + 1) * TILE
        out.append(f'<g><rect x="{a + 4}" y="{b + 4}" width="{w - 8}" height="{h - 8}" rx="10" fill="{col}"/>'
                   f'<title>{name}</title></g>')
        out.append(text(a + w / 2, b + h / 2 + 5, name.upper(), 13, '#fff', weight='bold'))

    # units
    for (x, y), (_, unit) in g.cells.items():
        if not unit or unit in BIG:
            continue
        cx, cy = g.centre(x, y)
        if unit in FAMILY:
            name, col = FAMILY[unit]
            out.append(f'<g><circle cx="{cx}" cy="{cy}" r="15" fill="{col}" stroke="#fff" stroke-width="2"/>'
                       f'<title>{x},{y}  {name}</title></g>')
            out.append(text(cx, cy + 4.5, unit, 13, '#fff', weight='bold'))
        else:
            name, col = OTHERS[unit]
            if unit == 'R':
                out.append(f'<g><path d="M{cx},{cy - 17} L{cx + 5},{cy - 5} L{cx + 17},{cy - 5} L{cx + 7},{cy + 3} '
                           f'L{cx + 11},{cy + 16} L{cx},{cy + 8} L{cx - 11},{cy + 16} L{cx - 7},{cy + 3} '
                           f'L{cx - 17},{cy - 5} L{cx - 5},{cy - 5} z" fill="{col}" stroke="#7a5c00" stroke-width="1.5"/>'
                           f'<title>{x},{y}  {name}</title></g>')
                continue
            r = 14
            if unit in DARK_BROOD:
                # the dark brood: diamonds (the Shaman can heal these)
                shape = (f'<path d="M{cx},{cy - r - 1} L{cx + r + 1},{cy} L{cx},{cy + r + 1} L{cx - r - 1},{cy} z" '
                         f'fill="{col}" stroke="#2b1035" stroke-width="1.5"/>')
            elif unit == 'a':
                # goblins: triangles
                shape = (f'<path d="M{cx},{cy - r - 2} L{cx + r + 2},{cy + r - 1} L{cx - r - 2},{cy + r - 1} z" '
                         f'fill="{col}" stroke="#fff" stroke-width="1.5"/>')
            else:
                shape = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="#fff" stroke-dasharray="3 2" '
                         f'stroke-width="1.5"/>')
            if unit == 'b':
                shape += (f'<path d="M{cx - 8},{cy - 12} L{cx - 8},{cy - 19} L{cx - 3},{cy - 15} L{cx},{cy - 21} '
                          f'L{cx + 3},{cy - 15} L{cx + 8},{cy - 19} L{cx + 8},{cy - 12} z" fill="#f1c40f"/>')
            out.append(f'<g>{shape}<title>{x},{y}  {name}</title></g>')
            out.append(text(cx, cy + 4.5, unit, 12, '#fff', weight='bold'))

    # arrows, steps, notes (on top)
    for line in g.notes:
        p = line.split()
        kind = p[0]
        if kind == 'arrow':
            coords = [tuple(map(int, t.split(','))) for t in p[1:] if COORD.match(t)]
            shift = {'dx': 0, 'dy': 0}
            rest = []
            for t in p[1:]:
                m = re.fullmatch(r'(dx|dy)=(-?\d+)', t)
                if m:
                    shift[m.group(1)] = int(m.group(2))
                elif not COORD.match(t):
                    rest.append(t)
            col = colour_of(rest[0]) if rest else None
            label = ' '.join(rest[1:] if col else rest)
            col = col or COLOURS['note']
            pts = [(cx + shift['dx'], cy + shift['dy']) for cx, cy in (g.centre(*c) for c in coords)]
            if len(pts) < 2:
                continue
            # pull the ends in a little so they don't cover the units
            (x0, y0), (x1, y1) = pts[0], pts[1]
            d0 = max(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5, 1)
            pts[0] = (x0 + (x1 - x0) / d0 * 13, y0 + (y1 - y0) / d0 * 13)
            (xa, ya), (xb, yb) = pts[-2], pts[-1]
            d1 = max(((xb - xa) ** 2 + (yb - ya) ** 2) ** 0.5, 1)
            pts[-1] = (xb - (xb - xa) / d1 * 14, yb - (yb - ya) / d1 * 14)
            path = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
            out.append(f'<polyline points="{path}" fill="none" stroke="{col}" stroke-width="3" '
                       f'stroke-linecap="round" stroke-linejoin="round" marker-end="url(#ah)" opacity="0.9"/>')
            if label:
                mx = (pts[-2][0] + pts[-1][0]) / 2; my = (pts[-2][1] + pts[-1][1]) / 2
                out.append(text(mx, my - 6, label, 10.5, col, weight='bold', halo=True))
        elif kind == 'step' and len(p) >= 3 and COORD.match(p[1]):
            x, y = map(int, p[1].split(','))
            a, b = g.px(x, y)
            out.append(f'<circle cx="{a + TILE - 9}" cy="{b + 9}" r="8" fill="#111"/>')
            out.append(text(a + TILE - 9, b + 12.5, p[2], 10, '#fff', weight='bold'))
        elif kind == 'note' and len(p) >= 3 and COORD.match(p[1]):
            x, y = map(int, p[1].split(','))
            cx, cy = g.centre(x, y)
            out.append(text(cx, cy - 17, ' '.join(p[2:]), 10, COLOURS['note'], weight='bold', halo=True))
    out.append('</svg>')
    return '\n'.join(out)


LEGEND = [
    ('.', 'floor'), ('#', 'rock'), ('_', 'gap (no tile)'), ('^', 'spikes'), ('P', 'Corruption pool'),
    ('E', 'exit / goal'), ('@', 'key tile'), ('~', 'Cyclone'), ('%', 'spider web'), ('*', 'exploding mushroom'),
    ('!', 'trap'), ('&', 'poison pool'), ('?', 'marked: poison drops next enemy turn'),
    ('J L U M T', 'John Linda Lucy Mark Toba'), ('D', 'Mountain Deev (3 × 2)'),
    ('c b s w', 'dark brood (diamonds): Dark Claw, Black Claw, Shaman, Worm'),
    ('a O', 'goblins: Archer (triangle), Masher (2 × 2)'), ('R', 'protectee'), ('d', 'decoy'),
]


def index_html(doc_name, items):
    cards = '\n'.join(
        f'<section id="{html.escape(i)}"><h2>{html.escape(t)} <span>{html.escape(i)}</span></h2>{svg}</section>'
        for i, t, svg in items)
    legend = ''.join(f'<li><code>{html.escape(k)}</code> {html.escape(v)}</li>' for k, v in LEGEND)
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Level chunks</title><style>
body{{font-family:Segoe UI,Helvetica,Arial,sans-serif;background:#f6f4ef;color:#222;margin:0;padding:16px}}
h1{{font-size:20px;margin:0 0 4px}} p{{margin:0 0 12px;color:#555;font-size:13px}}
ul{{display:flex;flex-wrap:wrap;gap:4px 16px;padding:0;margin:0 0 16px;list-style:none;font-size:12px;color:#444}}
code{{background:#e7e2d6;padding:1px 4px;border-radius:3px}}
main{{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}}
section{{background:#fff;border:1px solid #ddd6c8;border-radius:8px;padding:10px;max-width:100%;overflow-x:auto}}
h2{{font-size:14px;margin:0 0 6px}} h2 span{{font-weight:normal;color:#999;font-size:12px}}
svg{{display:block;max-width:100%;height:auto}}
</style></head><body><h1>Level chunks</h1><p>Drawn from {html.escape(doc_name)}. x from the left, y from the bottom; hover a tile for its coordinates.</p>
<ul>{legend}</ul><main>{cards}</main></body></html>'''


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__); return 0
    doc = argv[0]
    out = None
    if '--out' in argv:
        out = argv[argv.index('--out') + 1]
    if out is None:
        out = os.path.join(os.path.dirname(os.path.abspath(doc)), os.path.splitext(os.path.basename(doc))[0])
    os.makedirs(out, exist_ok=True)
    blocks = parse_blocks(open(doc, encoding='utf-8').read())
    items = []
    for blk in blocks:
        g = Grid(blk)
        svg = render(g)
        with open(os.path.join(out, g.id + '.svg'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(svg)
        items.append((g.id, g.title, svg))
    with open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(index_html(os.path.basename(doc), items))
    print(f'{len(items)} chunks drawn into {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
