# Shared paths for the reward tools. Resolves the Unity project from this file's location:
# <repo>/claude-handoff/reward-tools/ -> <repo>/miso/Assets/_Project
import os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PROJECT = os.path.join(REPO, 'miso', 'Assets', '_Project')
GUIDMAP = os.path.join(os.path.dirname(__file__), 'guidmap.json')
def load_map():
    if not os.path.exists(GUIDMAP):
        raise SystemExit('guidmap.json missing: run build_guidmap.py first')
    return json.load(open(GUIDMAP))
