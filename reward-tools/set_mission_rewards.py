# Writes completion XP, completion gold, resourceCollectionCount and the collectable list into the Mission assets.
# Edit the P table (file: (xp, gold, count, [(material, min, max), ...])) and run. Idempotent. Keeps bytes (LF/CRLF) as-is.
# Close Unity or let it reimport afterwards. Values here = state applied 2026-10-06.
import re,os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import PROJECT
os.chdir(os.path.join(PROJECT, 'Content/Levels'))
ENTRY='''  - resourceRef:
      entityID: MainResource_{id}
    amountRange:
      min: {mn}
      max: {mx}
    multiplier:
      factorReadMode: 0
      constantValue: 1
      baseFactor: 0
      attributeReference:
        entityID: Specs_Health
      bounded: 0
      bounds:
        minV:
          factorReadMode: 0
          constantValue: 0
          baseFactor: 0
          attributeReference:
            entityID: Specs_Health
        maxV:
          factorReadMode: 0
          constantValue: 0
          baseFactor: 0
          attributeReference:
            entityID: Specs_Health
'''
P={
 'M1 - Hidden Sanctuary - First Step.asset':(40,5,0,[]),
 'M2 - Ryler is Lost.asset':(40,5,1,[('Steel',1,1)]),
 'M5 - Hidden Sanctuary - Second Step.asset':(90,5,1,[('Timber',1,1)]),
 'M3 - Blood Trail of A Wolf.asset':(65,10,1,[('Timber',1,1)]),
 'M3 - Mark Intro.asset':(60,10,1,[('Fabric',1,1)]),
 'M4 - The White Mothers.asset':(120,20,4,[('Steel',1,1),('Timber',1,1),('Stone',1,1),('Fabric',1,1)]),
 'M6 - Hidden Sanctuary - Third Step.asset':(90,15,2,[('Steel',1,1),('Timber',1,1),('Stone',1,1),('Fabric',1,1)]),
 'M7 - Hidden Sanctuary - Finale.asset':(165,20,2,[('Steel',1,2),('Timber',1,2),('Stone',1,2),('Fabric',1,2)]),
}
for f,(xp,g,cnt,res) in P.items():
    b=open(f,'rb').read(); t=b.decode('utf-8')
    t,n1=re.subn(r'(\n  completionXPReward: )\d+',r'\g<1>%d'%xp,t)
    t,n2=re.subn(r'(\n  completionGoldReward: )\d+',r'\g<1>%d'%g,t)
    t,n3=re.subn(r'(\n  resourceCollectionCount: )\d+',r'\g<1>%d'%cnt,t)
    body=''.join(ENTRY.format(id=i,mn=a,mx=z) for i,a,z in res)
    new='\n  collectableGResources:'+(' []\n' if not res else '\n'+body)
    t,n4=re.subn(r'\n  collectableGResources:.*?\n(?=  initiationSequence:)',lambda m:new,t,flags=re.S)
    assert (n1,n2,n3,n4)==(1,1,1,1),(f,n1,n2,n3,n4)
    open(f,'wb').write(t.encode('utf-8'))
    print('ok',f)
