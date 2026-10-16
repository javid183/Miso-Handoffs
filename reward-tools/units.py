import json,re,os,glob
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import PROJECT, load_map
os.chdir(PROJECT)
m=load_map()
for g,p in sorted(m.items(),key=lambda x:x[1]):
    if not p.startswith('Features/') : continue
    t=open(p,errors='ignore').read()
    if 'abilityDamageXpReward' not in t and 'lethalDamageXpBonus' not in t: continue
    xp=re.findall(r'abilityDamageXpReward: (-?\d+)',t); lx=re.findall(r'lethalDamageXpBonus: (-?\d+)',t)
    rc=re.findall(r'resourceCollectionCount: (\d+)',t)
    res=re.findall(r'entityID: (MainResource_\w+)\s+amountRange:\s+min: (\d+)\s+max: (\d+)',t)
    nick=re.findall(r'nickname: (.*)',t)[:1]
    print(p.replace('Features/',''),'|',nick,'xp',xp,'lethal',lx,'rc',rc,res)
