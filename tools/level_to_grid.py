#!/usr/bin/env python3
"""Read a Miso level prefab and print it as a `grid` block for grid_render.py.

Usage (from the repo root, or anywhere: paths resolve against the Unity project):
    python claude-handoff/tools/level_to_grid.py <level.prefab> [<level.prefab> ...]
        [--id <id>] [--no-shift] [--debug]

<level.prefab> is a path relative to miso/Assets/_Project (the form the GDD's Source
lines use, e.g. "Content/Levels/Level1/Level1-C2.prefab"), or an absolute path.

What it reads, from the prefab YAML only (no Unity needed):
  - every GridCell instance: its tile, from its position (0.5 units per tile), checked
    against its "GridCell - (x, y)" name;
  - every placed unit, hazard and obstacle with a component, and the tile it sits on, by following its
    transform parent to the GridCell it is placed under (or, failing that, its position);
  - big units' footprints (placementSize), drawn up and right from the anchor tile, as
    the game does (GridPluggableEntity.FootprintCoords);
  - the level's objective texts, enemy tier and "all enemies start alert" setting;
  - units kept out of play until a sequence reveals them (inactive, and listed by group on the
    level's HiddenLevelUnits), written back as `level hidden [group] x,y ...` lines.
Props with no script (Cave_Obstacle_Rock_01, BecStatue and other scenery) are listed but
not drawn: they block nothing, and the playable map is exactly the set of GridCells.

The block is shifted so the grid starts at 0,0, and the shift is printed in the title
("offset x-11, y+10": subtract 11 from the prefab's x, add 10 to its y). --no-shift keeps
the prefab's own coordinates. Anything it can't draw goes in as a `note` line (deploy
slots, the Goblin Queen, story units), and anything it can't place is listed after the
block. It never writes to the project.

Needs claude-handoff/reward-tools/guidmap.json (asset GUID -> path). If a GUID is
missing, rebuild the map: python claude-handoff/reward-tools/build_guidmap.py
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HANDOFF = os.path.dirname(HERE)
REPO = os.path.dirname(HANDOFF)
PROJECT = os.path.join(REPO, 'miso', 'Assets', '_Project')
GUIDMAP = os.path.join(HANDOFF, 'reward-tools', 'guidmap.json')

TILE = 0.5
GRIDCELL_PATH = 'Content/Levels/_Common/Prefabs/GridCell.prefab'
HIDDEN_UNITS_SCRIPT = 'Features/Onboarding/HiddenLevelUnits.cs'
HIDDEN_DEFAULT_GROUP = 'hidden'

# Source prefab file name -> grid character (see grid_render.py for the legend)
UNIT_CHARS = {
    'Unit_John': 'J', 'Unit_Linda': 'L', 'Unit_Lucy': 'U', 'Unit_Mark': 'M',
    'Unit_Toba': 'T', 'Unit_Dom': 'T',
    'Unit_DarkClaw': 'c', 'Unit_BlackClaw': 'b', 'Unit_ArcherGoblin': 'a',
    'Unit_DarkShaman': 's', 'Unit_DarkWorm': 'w',
    'Unit_MasherGoblin': 'O', 'Unit_Deev': 'D',
}
TERRAIN_CHARS = {
    'Spike': '^', 'CP_Spawner': 'P', 'CP_Poison': '&', 'CP_Poison Deev': '&',
    'SpiderWeb': '%', 'MushroomExplosion': '*', 'Trap_Hazard': '!',
}
# Named for a note rather than a character
NOTE_NAMES = {
    'Unit_Placeholder': 'deploy slot', 'Unit_GoblinQueen': 'Goblin Queen (1 x 2)',
    'Unit_TobaEnemy': 'Toba (as enemy)', 'Deevoted': 'Deevoted',
}


def load_map():
    if not os.path.exists(GUIDMAP):
        sys.exit(f'missing {GUIDMAP}: run claude-handoff/reward-tools/build_guidmap.py first')
    with open(GUIDMAP, encoding='utf-8') as f:
        return json.load(f)


def read(path):
    with open(path, encoding='utf-8', errors='ignore') as f:
        return f.read()


def split_docs(text):
    """{fileID: (header, body)} for every YAML document in a prefab."""
    docs = {}
    for part in re.split(r'\n--- ', text):
        m = re.match(r'!u!(\d+) &(-?\d+)( stripped)?', part)
        if m:
            docs[m.group(2)] = (m.group(1), part)
    return docs


def mods_of(body):
    """The instance's overrides. Position comes from the root transform only: Unity writes
    a full x, y, z position for an instance's root, while child overrides (a sprite's
    offset inside the prefab) usually carry x and y alone."""
    rows = re.findall(r'target: \{fileID: (-?\d+)[^}]*\}\s+propertyPath: (\S+)\s+value: (.*)\n', body)
    mods = {}
    pos_by_target = {}
    for target, prop, value in rows:
        if prop.startswith('m_LocalPosition.'):
            pos_by_target.setdefault(target, {})[prop] = value
        else:
            mods.setdefault(prop, value.strip())
    root = next((p for p in pos_by_target.values() if 'm_LocalPosition.z' in p), None)
    if root is None and pos_by_target:
        root = next(iter(pos_by_target.values()))
    if root:
        for k, v in root.items():
            mods[k] = v.strip()
    return mods


def tile_of(x, y):
    return math.floor(x / TILE + 1e-6), math.floor(y / TILE + 1e-6)


def has_script(path, cache={}):
    """True when the prefab carries any MonoBehaviour (so it might be a grid entity)."""
    if path not in cache:
        full = os.path.join(PROJECT, path)
        cache[path] = os.path.exists(full) and 'm_Script:' in read(full)
    return cache[path]


def base_placement_size(gmap, path, cache={}):
    """placementSize from the unit's own prefab (or its base prefab)."""
    if path in cache:
        return cache[path]
    size = (1, 1)
    full = os.path.join(PROJECT, path)
    if os.path.exists(full):
        t = read(full)
        m = re.search(r'placementSize: \{x: (\d+), y: (\d+)\}', t)
        if m:
            size = (int(m.group(1)), int(m.group(2)))
        else:
            mx = re.search(r'propertyPath: placementSize\.x\s+value: (\d+)', t)
            my = re.search(r'propertyPath: placementSize\.y\s+value: (\d+)', t)
            if mx or my:
                size = (int(mx.group(1)) if mx else 1, int(my.group(1)) if my else 1)
            src = re.search(r'm_SourcePrefab: \{fileID: \d+, guid: (\w+)', t)
            if not (mx or my) and src and gmap.get(src.group(1), '').startswith('Features/'):
                size = base_placement_size(gmap, gmap[src.group(1)])
    cache[path] = size
    return size


def script_guid(path):
    """The GUID of a script, from its .meta file (None if it isn't there)."""
    meta = os.path.join(PROJECT, path + '.meta')
    if not os.path.exists(meta):
        return None
    m = re.search(r'guid: (\w+)', read(meta))
    return m.group(1) if m else None


def hidden_groups(docs, guid):
    """[(group id, [unit fileID, ...])] from the level's HiddenLevelUnits, in order."""
    if not guid:
        return []
    for cls, body in docs.values():
        if cls != '114' or f'guid: {guid}' not in body:
            continue
        groups = []
        section = re.search(r'\n  groups:\n((?:  [- ].*\n?)*)', body)
        if not section:
            return []
        for chunk in re.split(r'\n  - ', '\n' + section.group(1)):
            m = re.match(r'id: ?(.*)', chunk)
            if not m:
                continue
            gid = m.group(1).strip().strip('"') or HIDDEN_DEFAULT_GROUP
            units = re.findall(r'\n    - \{fileID: (-?\d+)', '\n' + chunk)
            groups.append((gid, units))
        return groups
    return []


def parse_level(path, gmap, debug=False):
    text = read(path)
    docs = split_docs(text)
    instances = {}   # instance fileID -> dict
    stripped_to_instance = {}  # stripped object fileID -> instance fileID
    for fid, (cls, body) in docs.items():
        if cls == '1001':
            src = re.search(r'm_SourcePrefab: \{fileID: \d+, guid: (\w+)', body)
            parent = re.search(r'm_TransformParent: \{fileID: (-?\d+)', body)
            instances[fid] = {
                'src': gmap.get(src.group(1), '?' + src.group(1)) if src else '?',
                'parent': parent.group(1) if parent else '0',
                'mods': mods_of(body),
            }
        else:
            pi = re.search(r'm_PrefabInstance: \{fileID: (-?\d+)', body)
            if pi and pi.group(1) != '0':
                stripped_to_instance[fid] = pi.group(1)
    # plain (non-prefab) transforms: map their fileID -> their GameObject's parent transform
    plain_parent = {}
    for fid, (cls, body) in docs.items():
        if cls in ('4', '224'):
            fa = re.search(r'm_Father: \{fileID: (-?\d+)', body)
            if fa:
                plain_parent[fid] = fa.group(1)

    cells = {}       # tile -> instance fileID
    cell_of_instance = {}
    name_mismatch = []
    for fid, inst in instances.items():
        if inst['src'] != GRIDCELL_PATH:
            continue
        m = inst['mods']
        name = m.get('m_Name', '')
        nm = re.search(r'GridCell - \((-?\d+), ?(-?\d+)\)', name)
        if 'm_LocalPosition.x' in m and 'm_LocalPosition.y' in m:
            t = tile_of(float(m['m_LocalPosition.x']), float(m['m_LocalPosition.y']))
            if nm and (int(nm.group(1)), int(nm.group(2))) != t:
                name_mismatch.append((name, t))
        elif nm:
            t = (int(nm.group(1)), int(nm.group(2)))
        else:
            continue
        cells[t] = fid
        cell_of_instance[fid] = t

    def resolve_cell(parent_fid, depth=0):
        """Follow a transform parent up to a GridCell instance."""
        if depth > 8 or parent_fid in ('0', None):
            return None
        inst = stripped_to_instance.get(parent_fid)
        if inst and inst in cell_of_instance:
            return cell_of_instance[inst]
        if inst and inst in instances:
            return resolve_cell(instances[inst]['parent'], depth + 1)
        if parent_fid in plain_parent:
            return resolve_cell(plain_parent[parent_fid], depth + 1)
        return None

    placed, notes, unplaced, unknown = [], [], [], {}
    tile_of_instance = {}   # placed unit's instance fileID -> its tile
    inactive_instances = set()
    off_grid = 0
    decor = {}
    for fid, inst in instances.items():
        src = inst['src']
        if src == GRIDCELL_PATH:
            continue
        stem = os.path.splitext(os.path.basename(src))[0]
        kind = None
        if stem in UNIT_CHARS:
            kind = ('unit', UNIT_CHARS[stem])
        elif stem in TERRAIN_CHARS:
            kind = ('terrain', TERRAIN_CHARS[stem])
        elif '/Obstacles/' in src:
            if not has_script(src):
                decor[stem] = decor.get(stem, 0) + 1   # sprites only: scenery, blocks nothing
                continue
            kind = ('terrain', '#')
        elif stem in NOTE_NAMES:
            kind = ('note', NOTE_NAMES[stem])
        elif src.startswith('Features/Enemy') or src.startswith('Features/Player') or src.startswith('Features/Hazards') \
                or src.startswith('Features/NPC') or '/Units/' in src:
            kind = ('note', stem)
        else:
            unknown[src] = unknown.get(src, 0) + 1
            continue
        tile = resolve_cell(inst['parent'])
        how = 'parent'
        if tile is None:
            m = inst['mods']
            if 'm_LocalPosition.x' in m and 'm_LocalPosition.y' in m:
                tile = tile_of(float(m['m_LocalPosition.x']), float(m['m_LocalPosition.y']))
                how = 'position'
        if tile is None:
            unplaced.append(f'{stem} (parent {inst["parent"]})')
            continue
        if kind == ('terrain', '#') and tile not in cells:
            off_grid += 1   # scenery outside the playable grid
            continue
        size = (1, 1)
        if kind[0] == 'unit' and kind[1] in 'OD':
            size = base_placement_size(gmap, src)
            m = inst['mods']
            size = (int(m.get('placementSize.x', size[0])), int(m.get('placementSize.y', size[1])))
        placed.append((tile, kind, stem, size, how, inst['mods']))
        if kind[0] == 'unit':
            tile_of_instance[fid] = tile
            if inst['mods'].get('m_IsActive') == '0':
                inactive_instances.add(fid)

    # level settings
    texts = [v.strip() for k, v in re.findall(r'(displayTextTemplate): (.*)', text)]
    for inst in instances.values():
        texts += [v for k, v in inst['mods'].items() if k.endswith('displayTextTemplate')]
    texts = [t.strip('"') for t in dict.fromkeys(texts) if t.strip() not in ('', '""')]
    def setting(name, pattern=r'(-?\d+)'):
        """A level setting, written either on the level's own component or as an override
        on the nested LevelBase instance."""
        m = re.search(name + r': ' + pattern, text)
        if m:
            return m.group(1).strip()
        for inst in instances.values():
            for k, v in inst['mods'].items():
                if k == name or k.endswith('.' + name):
                    return v
        return None

    tier = setting('enemyTier')
    alert = setting('allEnemiesStartAlert')
    level_name = setting('levelName', r'(.*)')
    starts_alert = [p for p in placed if any(k.lower().endswith('startsalert') and v == '1' for k, v in p[5].items())]

    # Hidden units: listed on HiddenLevelUnits (a unit reference is a stripped component of its instance).
    hidden, listed = [], set()
    hidden_problems = []
    for gid, unit_fids in hidden_groups(docs, script_guid(HIDDEN_UNITS_SCRIPT)):
        tiles = []
        for ufid in unit_fids:
            inst = stripped_to_instance.get(ufid, ufid)
            if inst not in tile_of_instance:
                hidden_problems.append(f'group {gid}: a listed unit that is not a placed unit (fileID {ufid})')
                continue
            listed.add(inst)
            if inst not in inactive_instances:
                hidden_problems.append(f'group {gid}: the unit on {tile_of_instance[inst]} is listed but active, so it starts in play')
            tiles.append(tile_of_instance[inst])
        hidden.append((gid, tiles))
    for inst in sorted(inactive_instances - listed):
        hidden_problems.append(f'the unit on {tile_of_instance[inst]} is inactive but in no hidden group, so nothing ever brings it in')
    return {
        'cells': cells, 'placed': placed, 'unplaced': unplaced, 'unknown': unknown, 'off_grid': off_grid,
        'decor': decor,
        'mismatch': name_mismatch, 'texts': texts,
        'tier': tier,
        'alert': alert,
        'starts_alert': starts_alert,
        'hidden': hidden,
        'hidden_problems': hidden_problems,
        'name': level_name,
    }


TIER_NAMES = {'0': 'Standard', '1': 'Early', '2': 'Tutorial', '3': 'Late'}


def to_block(path, lv, block_id, shift=True):
    cells = lv['cells']
    if not cells:
        return None
    xs = [x for x, _ in cells]; ys = [y for _, y in cells]
    ox, oy = (-min(xs), -min(ys)) if shift else (0, 0)
    grid = {}
    for t in cells:
        grid[t] = ['.', '']
    notes = []
    for tile, kind, stem, size, how, _ in lv['placed']:
        if kind[0] == 'note':
            notes.append(f'note {tile[0] + ox},{tile[1] + oy} {kind[1]}')
            continue
        footprint = [(tile[0] + dx, tile[1] + dy) for dx in range(size[0]) for dy in range(size[1])]
        for t in footprint:
            if t not in grid:
                grid[t] = ['.', '']   # footprint over a tile the level lacks: draw it anyway
            if kind[0] == 'terrain':
                if grid[t][0] in '.' or kind[1] != '#':
                    grid[t][0] = kind[1]
            else:
                if grid[t][1]:
                    notes.append(f'note {t[0] + ox},{t[1] + oy} also {grid[t][1]}')
                grid[t][1] = kind[1]
    xs = [x for x, _ in grid]; ys = [y for _, y in grid]
    inside, outside = [], []
    for n in notes:
        nx, ny = map(int, n.split()[1].split(','))
        bx, by = nx - ox, ny - oy
        (inside if min(xs) <= bx <= max(xs) and min(ys) <= by <= max(ys) else outside).append(n)
    notes = inside
    lv['outside_notes'] = [' '.join(n.split()[2:]) + f' at {n.split()[1]}' for n in outside]
    rows = []
    for y in range(max(ys), min(ys) - 1, -1):
        row = []
        for x in range(min(xs), max(xs) + 1):
            if (x, y) not in grid:
                row.append('_')
            else:
                ter, unit = grid[(x, y)]
                row.append(unit if unit and ter == '.' else (ter + unit if unit else ter))
        rows.append(' '.join(row))
    stem = os.path.splitext(os.path.basename(path))[0]
    off = f'offset x{ox:+d}, y{oy:+d}' if shift else 'prefab coordinates'
    out = [f'```grid id={block_id or "src-" + stem.lower()} title="Source: {stem} ({off})"']
    out += rows
    level_lines = []
    for gid, tiles in lv.get('hidden', []):
        if not tiles:
            continue
        name = '' if gid == HIDDEN_DEFAULT_GROUP else gid + ' '
        level_lines.append('level hidden ' + name + ' '.join(f'{x + ox},{y + oy}' for x, y in tiles))
    if notes or level_lines:
        out.append('--')
        out += sorted(set(notes))
        out += level_lines
    out.append('```')
    return '\n'.join(out), (ox, oy)


def summary(path, lv, offset):
    lines = []
    tier = lv['tier']
    lines.append(f'- Level: {lv["name"] or os.path.basename(path)}; {len(lv["cells"])} tiles; '
                 f'enemy tier {TIER_NAMES.get(tier, tier) if tier else "not set (Standard)"}; '
                 f'all enemies start alert: {"yes" if lv["alert"] == "1" else "no" if lv["alert"] == "0" else "not set"}')
    for t in lv['texts']:
        lines.append(f'- Objective text: {t}')
    counts = {}
    for _, kind, stem, *_ in lv['placed']:
        counts[stem] = counts.get(stem, 0) + 1
    if counts:
        lines.append('- Placed: ' + ', '.join(f'{n} × {s}' for s, n in sorted(counts.items())))
    for problem in lv.get('hidden_problems', []):
        lines.append('- Hidden units: ' + problem)
    if lv['starts_alert']:
        lines.append('- Starts alert (per unit): ' + ', '.join(p[2] for p in lv['starts_alert']))
    by_pos = {}
    for p in lv['placed']:
        if p[4] == 'position' and p[1] != ('terrain', '#'):
            by_pos[p[2]] = by_pos.get(p[2], 0) + 1
    if by_pos:
        lines.append('- Placed by position, not under a cell (check them): '
                     + ', '.join(f'{n} × {s}' for s, n in by_pos.items()))
    if lv['decor']:
        lines.append('- Scenery props (sprites only, block nothing; the playable map is the GridCells): '
                     + ', '.join(f'{n} × {s}' for s, n in sorted(lv['decor'].items())))
    if lv['off_grid']:
        lines.append(f'- {lv["off_grid"]} obstacle props with a component sit outside the grid (not drawn)')
    if lv.get('outside_notes'):
        lines.append('- Off the grid (not drawn): ' + ', '.join(lv['outside_notes']))
    if lv['unplaced']:
        lines.append('- Could not place: ' + ', '.join(lv['unplaced']))
    if lv['mismatch']:
        lines.append(f'- {len(lv["mismatch"])} GridCell names disagree with their positions (positions used), e.g. '
                     + ', '.join(f'{n} at {t}' for n, t in lv['mismatch'][:3]))
    other = [s for s in lv['unknown'] if not s.startswith('?')]
    missing = [s for s in lv['unknown'] if s.startswith('?')]
    if other:
        lines.append('- Not drawn (decor, controllers, nested prefabs): ' + ', '.join(
            os.path.splitext(os.path.basename(s))[0] for s in sorted(other)[:12]) + (' …' if len(other) > 12 else ''))
    if missing:
        lines.append(f'- {len(missing)} prefab GUIDs not in guidmap.json: rebuild it (reward-tools/build_guidmap.py)')
    return '\n'.join(lines)


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__); return 0
    shift = '--no-shift' not in argv
    debug = '--debug' in argv
    block_id = None
    if '--id' in argv:
        block_id = argv[argv.index('--id') + 1]
    paths = [a for i, a in enumerate(argv) if not a.startswith('--') and (i == 0 or argv[i - 1] != '--id')]
    gmap = load_map()
    for p in paths:
        full = p if os.path.isabs(p) else os.path.join(PROJECT, p)
        if not os.path.exists(full):
            print(f'not found: {full}', file=sys.stderr); continue
        lv = parse_level(full, gmap, debug)
        res = to_block(full, lv, block_id if len(paths) == 1 else None, shift)
        if res is None:
            print(f'{p}: no GridCell instances in this prefab (it may nest another level prefab: '
                  f'run the tool on that one)', file=sys.stderr)
            print(summary(full, lv, (0, 0)))
            continue
        block, off = res
        print(block)
        print()
        print(summary(full, lv, off))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
