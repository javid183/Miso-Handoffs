# Read-only summary of every Mission asset's rewards: completion XP/gold, collection count and resource list.
# Usage: python3 mission_rewards.py
import os, re, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import PROJECT
os.chdir(os.path.join(PROJECT, 'Content', 'Levels'))
for f in sorted(glob.glob('M*.asset')):
    t = open(f, encoding='utf-8').read()
    g = lambda k: (re.search(r'\n  %s: (\d+)' % k, t) or [None, '?'])[1]
    res = re.findall(r'entityID: MainResource_(\w+)\s+amountRange:\s+min: (\d+)\s+max: (\d+)', t)
    print(f'{f:48s} XP {g("completionXPReward"):>4} Gold {g("completionGoldReward"):>3} pick {g("resourceCollectionCount")} of',
          ', '.join(f'{r} {a}-{b}' for r, a, b in res) or '-')
