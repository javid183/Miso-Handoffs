# Reads the demo's dialogue, tutorial pages, mission and ability text and barks from the Unity project into _extract.json. Run: python extract_lines.py [path to miso/Assets/_Project]
import os, re, json, yaml, glob, csv
import sys
root=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','miso','Assets','_Project')
G={'f76dd1e5358d3d74db102c9e3dc8e0d3':'John','bf88a3ed10afb8a4fa03dc001dd47e61':'Linda','296967754ef7fa34aa494926831c0afd':'Lucy',
   'ace6f7ab51fe3764fbdc7c0f9182012c':'Mark','9d4bf4aef5924ab4c88f2585db678fe9':'Toba (Dom asset)','a9447429e4528dd42a788972c7b66aa2':'Family',
   '83141b4b4a7f1451f80ff5439fba0c62':'TextBox (narrator)','a0ea695f2ffb41f4aa38e865e374cceb':'Top notification',
   'c321b44dd9e5c154aa7266daa2a84044':'Generic 1','4c187ec29899c92418b19dfbe55fd34e':'Generic 2','56f2f894bb5052f40bc468362d14f882':'Generic 3','77a92c1d1f20d324e9f2f2895c79aabb':'Generic 4'}
def load(p):
    t=open(p,encoding='utf-8').read()
    t=re.sub(r'^%.*\n','',t,flags=re.M)
    t=re.sub(r'^--- !u!\d+ &\d+.*$','---',t,flags=re.M)
    docs=[d for d in yaml.safe_load_all(t) if d]
    return docs
rows=[]
def rel(p): return os.path.relpath(p,root).replace('\\','/')
scope=['Hearth','HomeVisits','M1Ridge','Search','SistersTally','Mission 4','Intro']
for s in scope:
    for p in sorted(glob.glob(os.path.join(root,'Resources/Sequences',s,'**','*.asset'),recursive=True)):
        raw=open(p,encoding='utf-8').read()
        if 'sequenceNodes:' not in raw and 'pageText' not in raw: continue
        try: docs=load(p)
        except Exception as e: rows.append({'kind':'error','file':rel(p),'text':str(e)[:200]}); continue
        for d in docs:
            mb=d.get('MonoBehaviour',{})
            for i,n in enumerate(mb.get('sequenceNodes') or []):
                if not isinstance(n,dict): continue
                txt=n.get('Text')
                if txt is None: continue
                g=(n.get('characterData') or {}).get('guid')
                rows.append({'kind':'dialogue','area':s,'file':rel(p),'index':i,'nodeType':n.get('nodeType'),'speaker':G.get(g, g or ''),'text':str(txt)})
            for i,pg in enumerate(mb.get('pages') or []):
                rows.append({'kind':'tutorial','area':s,'file':rel(p),'index':i,'title':pg.get('pageTitle',''),'text':str(pg.get('pageText','')),
                             'image': bool((pg.get('image') or {}).get('guid')), 'video': bool((pg.get('videoClip') or {}).get('guid'))})
for m in ['M0 - The Hearth','MS1 - The River','MS2 - The Ridge','M2 - The Trail','M4 - The White Mothers']:
    p=os.path.join(root,'Content/Levels',m+'.asset')
    try:
        mb=load(p)[0]['MonoBehaviour']
        rows.append({'kind':'mission','file':rel(p),'name':mb.get('missionName',''),'text':str(mb.get('missionDescription', mb.get('description','')))})
    except Exception as e: rows.append({'kind':'error','file':rel(p),'text':str(e)[:200]})
for hero in ['John','Linda','Lucy','Mark','Dom','Toba']:
    for p in sorted(glob.glob(os.path.join(root,'Resources/UnitSpecific/Player',hero,'**','*.asset'),recursive=True)):
        raw=open(p,encoding='utf-8').read()
        if '\n  title:' not in raw or '\n  description:' not in raw: continue
        try: mb=load(p)[0].get('MonoBehaviour',{})
        except Exception as e: continue
        if mb.get('title') is None: continue
        rows.append({'kind':'ability','hero':hero,'file':rel(p),'name':str(mb.get('title','')),'text':str(mb.get('description',''))})
for p in sorted(glob.glob(os.path.join(root,'Resources/BarkSystemData','**','*.csv'),recursive=True)):
    with open(p,encoding='utf-8-sig',newline='') as f:
        for i,r in enumerate(csv.DictReader(f)):
            rows.append({'kind':'bark','file':rel(p),'index':i+2,'speaker':r.get('Unit',''),'tag':r.get('Tag',''),'text':r.get('Dialogue','')})
json.dump(rows,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'_extract.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
from collections import Counter
print(Counter(r['kind'] for r in rows)); print([r for r in rows if r['kind']=='error'][:5])
print(Counter(r.get('nodeType') for r in rows if r['kind']=='dialogue'))
