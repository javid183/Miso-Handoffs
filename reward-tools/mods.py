# Usage: python3 mods.py <prefab> ...  Lists reward-related prefab overrides (lethal XP, drops) per nested prefab instance.
# Any line under a level prefab = a per-level override (should be none; see claude-handoff/design/reward-balance.md).
import json,re,os,sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import load_map
m=load_map()
KEYS=('abilityDamageXpReward','lethalDamageXpBonus','resourceCollectionCount','collectableGResources','nickname')
def mods(p):
    t=open(p,errors='ignore').read()
    out=[]
    # split by PrefabInstance docs
    for doc in re.split(r'\n--- ',t):
        if not doc.startswith('!u!1001'): continue
        src=re.search(r'm_SourcePrefab: \{fileID: \d+, guid: (\w+)',doc)
        srcp=m.get(src.group(1),src.group(1)) if src else '?'
        items=re.findall(r'propertyPath: (\S+)\s+value: (.*)\n',doc)
        rel=[(a,b.strip()) for a,b in items if any(k in a for k in KEYS)]
        out.append((srcp,rel))
    return out
for p in sys.argv[1:]:
    print('###',p)
    for s,r in mods(p):
        s2=s.split('/')[-1]
        print('  ',s2, '; '.join(f'{a.replace("collectableGResources","cGR")}={b}' for a,b in r))
