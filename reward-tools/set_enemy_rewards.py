# Writes lethalDamageXpBonus and gold amountRange (min/max) on the enemy prefab variants.
# E table: prefab: (lethal XP, gold min or None to keep, gold max or None). Only edits existing overrides (asserts exactly one match).
# Values here = state applied 2026-10-06.
import re,os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import PROJECT
os.chdir(os.path.join(PROJECT, 'Features/Enemy'))
E={'Archer Goblin/Prefabs/Unit_ArcherGoblin.prefab':(4,None,1),
 'Dark Claw/Prefabs/Unit_DarkClaw.prefab':(3,None,1),
 'Dark Claw/Prefabs/Unit_BlackClaw.prefab':(5,None,2),
 'Dark Shaman/Prefabs/Unit_DarkShaman.prefab':(4,1,2),
 'Dark Worm/Prefabs/Unit_DarkWorm.prefab':(3,None,None),
 'Masher Goblin/Prefabs/Unit_MasherGoblin.prefab':(10,1,3),
 'Mountain Deev/Prefabs/Unit_Deev.prefab':(10,1,3),
 'Goblin Queen/Prefab/Unit_GoblinQueen.prefab':(30,5,5)}
def setv(t,path,val):
    t2,n=re.subn(r'(propertyPath: %s\n\s+value: )\S+'%re.escape(path),r'\g<1>%d'%val,t)
    assert n==1,(path,n); return t2
for f,(xp,mn,mx) in E.items():
    t=open(f,'rb').read().decode('utf-8')
    t=setv(t,'lethalDamageXpBonus',xp)
    if mn is not None: t=setv(t,'collectableGResources.Array.data[0].amountRange.min',mn)
    if mx is not None: t=setv(t,'collectableGResources.Array.data[0].amountRange.max',mx)
    open(f,'wb').write(t.encode('utf-8')); print('ok',f)
