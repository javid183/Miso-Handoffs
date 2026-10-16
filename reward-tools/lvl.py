# Usage: python3 lvl.py "Content/Levels/Level1/Level1-C2.prefab" ...  (paths relative to Assets/_Project)
# Prints goals, enemy counts and effective kill XP / gold per level (enemy prefab values + per-level overrides).
import json,re,os,sys,collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import PROJECT, load_map
os.chdir(PROJECT)
m=load_map()
inv={v:k for k,v in m.items()}
def parse_mods(doc):
    d={}
    for a,b in re.findall(r'propertyPath: (\S+)\s+value: (.*)\n',doc): d[a]=b.strip()
    return d
cache={}
def enemy_base(path):
    if path in cache: return cache[path]
    t=open(path,errors='ignore').read()
    base={'xp':0,'rc':0,'res':[]}
    for doc in re.split(r'\n--- ',t):
        if doc.startswith('!u!1001'):
            src=re.search(r'm_SourcePrefab: \{fileID: \d+, guid: (\w+)',doc)
            sp=m.get(src.group(1)) if src else None
            if sp and sp.startswith('Features/Enemy'): base=dict(enemy_base(sp)); base['res']=[dict(r) for r in base['res']]
            base=apply(base,parse_mods(doc)); break
    cache[path]=base; return base
def apply(b,md):
    b=dict(b); b['res']=[dict(r) for r in b['res']]
    if 'lethalDamageXpBonus' in md: b['xp']=int(md['lethalDamageXpBonus'])
    if 'resourceCollectionCount' in md: b['rc']=int(md['resourceCollectionCount'])
    if 'collectableGResources.Array.size' in md:
        n=int(md['collectableGResources.Array.size']); b['res']=(b['res']+[{'id':'?','min':0,'max':0} for _ in range(n)])[:n]
    for k,v in md.items():
        mm=re.match(r'collectableGResources\.Array\.data\[(\d+)\]\.(amountRange\.min|amountRange\.max|resourceRef\.entityID)',k)
        if mm:
            i=int(mm.group(1))
            while len(b['res'])<=i: b['res'].append({'id':'?','min':0,'max':0})
            key={'amountRange.min':'min','amountRange.max':'max','resourceRef.entityID':'id'}[mm.group(2)]
            b['res'][i][key]=v if key=='id' else int(v)
    return b
def level(path,depth=0):
    t=open(path,errors='ignore').read()
    out=[]; texts=re.findall(r'displayTextTemplate: (.*)',t); names=re.findall(r'levelName: (.*)',t)
    for doc in re.split(r'\n--- ',t):
        if not doc.startswith('!u!1001'): continue
        src=re.search(r'm_SourcePrefab: \{fileID: \d+, guid: (\w+)',doc)
        sp=m.get(src.group(1),'') if src else ''
        md=parse_mods(doc)
        texts+= [v for k,v in md.items() if k.endswith('displayTextTemplate')]
        names+= [v for k,v in md.items() if k.endswith('levelName')]
        if sp.startswith('Features/Enemy'):
            b=apply(enemy_base(sp),md); out.append((sp.split('/')[-1][5:-7],b))
        elif sp.startswith('Content/Levels') and 'Env' not in sp and depth<3:
            sub=level(sp,depth+1); out+=sub[0]; texts+=sub[1]; names+=sub[2]
    return out,texts,names
for p in sys.argv[1:]:
    u,tx,nm=level(p)
    print('##',p.split('/')[-1],'| name:',nm[:2])
    for x in dict.fromkeys(tx): 
        if x.strip() not in ('','""'): print('   goal:',x[:110])
    c=collections.Counter(); xp=0; gmin=gmax=0
    for n,b in u:
        g=[r for r in b['res'] if 'Gold' in str(r.get('id'))] if b['rc']>0 else []
        lo=sum(r['min'] for r in g); hi=sum(r['max'] for r in g)
        c[f"{n}(xp{b['xp']},g{lo}-{hi})"]+=1; xp+=b['xp']; gmin+=lo; gmax+=hi
    for k,v in c.items(): print('   ',v,'x',k)
    print(f'   TOTAL kill XP {xp}, gold {gmin}-{gmax}, enemies {len(u)}')
