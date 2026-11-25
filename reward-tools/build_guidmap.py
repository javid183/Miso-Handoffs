# Builds guidmap.json: prefab GUID -> path (relative to Assets/_Project) for Content/ and Features/.
# Run again after adding or moving prefabs. Takes ~30 s over the device bridge.
import os, json
from _paths import PROJECT, GUIDMAP
m = {}
os.chdir(PROJECT)
for root in ['Content', 'Features']:
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.endswith('.prefab.meta'):
                p = os.path.join(dp, f)
                with open(p) as fh:
                    for line in fh:
                        if line.startswith('guid:'):
                            m[line.split()[1]] = p[:-5].replace(os.sep, '/'); break  # forward slashes on Windows too
json.dump(m, open(GUIDMAP, 'w'), indent=0)
print(len(m), 'prefabs mapped')
