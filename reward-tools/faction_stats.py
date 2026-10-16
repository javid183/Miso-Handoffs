# Read-only: prints each BergsonsFaction stat with its factor and cost per upgrade level.
# Usage: python3 faction_stats.py
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import PROJECT
t = open(os.path.join(PROJECT, 'Resources', 'Factions', 'BergsonsFaction.asset'), encoding='utf-8').read()
for blk in re.split(r'\n      - attribute:\n', t)[1:]:
    eid = re.search(r'entityID: (\w+)', blk).group(1)
    lv = re.findall(r'- factor: ([\d.\-]+)\n\s+resourceRequirements:(.*?)(?=\n\s+- factor:|\Z|\n    \w)', blk, re.S)
    if len(lv) > 1:
        print(f'{eid:10s}', ' | '.join(f + ' (' + (', '.join(f'{a} {r}' for r, a in re.findall(r'MainResource_(\w+)\s+amount: (\d+)', req)) or 'base') + ')' for f, req in lv))
