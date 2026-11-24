# Builds narrative-sheet.xlsx from _extract.json (written by extract_lines.py). Run: python build_sheet.py
import json, re, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

R=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'_extract.json'),encoding='utf-8'))
P='miso/Assets/_Project/'
F=Font(name='Arial',size=10); FB=Font(name='Arial',size=10,bold=True); FH=Font(name='Arial',size=10,bold=True,color='FFFFFF')
FT=Font(name='Arial',size=14,bold=True); FG=Font(name='Arial',size=9,color='666666')
HDR=PatternFill('solid',fgColor='3B4A5A'); FILL=PatternFill('solid',fgColor='FFF2CC'); EX=PatternFill('solid',fgColor='E2EFDA'); HOLD=PatternFill('solid',fgColor='F2F2F2')
WR=Alignment(wrap_text=True,vertical='top'); thin=Side(style='thin',color='D0D0D0'); BD=Border(bottom=thin)

def stem(f): 
    s=os.path.basename(f).replace('.asset','')
    return re.sub(r'_?(DialogNodeSequence|DialogueSequence|DialogNode Sequence)$','',s).replace('DialogNodeSequence','')
def where(f):
    s=f.replace('Resources/Sequences/','')
    parts=s.split('/')
    return parts[0]
CONT={
 'Hearth':'Built','HomeVisits':'Built','Intro':'Built (intro screen)',
 'M1Ridge':'Hold: M1 is being redesigned (2026-11-24)','Search/Ridge':'Old Ridge (replaced by M1); reference only',
 'Search/River':'To be rebuilt as M2 (chunk 3.2); lines move to new sequences','Search/Trail':'To be rebuilt as M3 (chunk 3.3)',
 'Search/Shared':'Built','SistersTally':'Built; plays at M3\'s end (D-624)','Mission 4':'To be rebuilt: M4 becomes 3 levels (chunk 3.4); Toba\'s duel is cut',
}
def cont(f):
    s=f.replace('Resources/Sequences/','')
    if s.startswith('Hearth/Memory2Lucy'): return 'Hold: THJ is editing memory 2 (D-643)'
    for k,v in CONT.items():
        if s.startswith(k): return v
    return 'Built'
def task(f,text):
    s=f.replace('Resources/Sequences/','')
    if text.startswith('Margaret:'): return 'H-12'
    m={'Hearth/Hearth_':'H-12','Hearth/Memory1':'H-14','Hearth/Memory2':'H-15','Hearth/Memory3John_End':'H-17','Hearth/Memory3':'H-16',
       'Hearth/Memory4Mark_Hold_John':'H-20','Hearth/Memory4Mark/Memory4Mark_End':'E-01','Hearth/Memory4Mark/Memory4Mark_Hold_John':'H-20','Hearth/Memory4':'H-19',
       'HomeVisits/Hearth_Close':'E-01','HomeVisits/Yard':'M3-07','HomeVisits':'Home','M1Ridge':'M1-02','Search/Ridge':'M1 (old)','Search/River':'M2-02',
       'Search/Trail/Trail_Pile':'M2-04 / M3','Search/Trail':'M3','SistersTally':'M3','Mission 4/Level3C1':'M4-03','Mission 4':'M4','Intro':'Intro'}
    for k in sorted(m,key=len,reverse=True):
        if s.startswith(k) or ('/'+k.split('/')[-1]) in s and k.count('/')>1: return m[k]
    return ''

wb=Workbook()
# ---------- Read me
ws=wb.active; ws.title='Read me'
rm=[('Narrative sheet: the onboarding demo (Hearth to the end of M4)',FT),
('Snapshot of every line, tutorial page, name and bark the demo shows, with the file each one lives in. Taken from the project on 2026-11-24 (branch thj/onboarding-demo). Task IDs (H-, E-, M1- to M4-, X-, W-) come from the tweak doc: claude-handoff/design/demo-tweaks-snapshot.md.',F),
('',F),
('How to use it',FB),
('1. Start with the Tasks tab: it says what to write, where it plays, and which tab holds the lines.',F),
('2. Write only in the yellow columns: New speaker, New text, Status, Writer notes. Leave every other column as it is: Claude matches rows by Line ID and File.',F),
('3. Status: Draft (still working), Final (ready to import), Keep (no change), Cut (remove the line; Claude asks before deleting). Leave it empty if you haven\'t looked at a row.',F),
('4. New lines that have no container yet go in the New lines tab. Claude builds the container, then imports the text.',F),
('5. Rows whose Container says "Hold" or "To be rebuilt" belong to levels being redesigned: write for the moment, not the file. Claude places the text when the level is rebuilt.',F),
('6. Speaker "TextBox (narrator)" is the narrator box. A row with no speaker is set by the level (for example the picked hero).',F),
('7. Keep [PLACEHOLDER] out of final text. Names and terms follow claude-handoff/glossary.md.',F),
('',F),
('How Claude imports it',FB),
('Claude reads this file, takes every row marked Final, and writes New text (and New speaker) into the File at that Node. Before writing, it checks the file still holds Current text: if someone changed the line in Unity since this snapshot, that row is skipped and listed for you, so no hand edit is lost (D-526). Barks are written into their CSV files (same columns the bark system reads). Tutorial pages: title and text into the page.',F),
('',F),
('Legend',FB),
]
for i,(t,f) in enumerate(rm,1):
    c=ws.cell(i,1,t); c.font=f; c.alignment=Alignment(wrap_text=True,vertical='top')
PR=len(rm)+1
ws.cell(PR,1,'Yellow column: you write here').fill=FILL; ws.cell(PR,1).font=F
ws.cell(PR+1,1,'Green row: an example of a filled row').fill=EX; ws.cell(PR+1,1).font=F
ws.cell(PR+2,1,'Grey row: level on hold or being rebuilt').fill=HOLD; ws.cell(PR+2,1).font=F
PR+=4
ws.cell(PR,1,'Progress (counts update as you set Status)').font=FB
tabs=['Lines','New lines','Tutorial pages','Names and text','Barks']
ws.cell(PR+1,1,'Tab').font=FB; ws.cell(PR+1,2,'Rows').font=FB; ws.cell(PR+1,3,'Final').font=FB; ws.cell(PR+1,4,'Draft').font=FB
ws.column_dimensions['A'].width=110
for c in 'BCD': ws.column_dimensions[c].width=10

def sheet(name, headers, widths, rows, fillcols, hold_col=None, example=None, status_col=None):
    s=wb.create_sheet(name)
    for j,h in enumerate(headers,1):
        c=s.cell(1,j,h); c.font=FH; c.fill=HDR; c.alignment=WR
        s.column_dimensions[get_column_letter(j)].width=widths[j-1]
    s.freeze_panes='B2'
    rr=2
    allrows=([example] if example else [])+rows
    for k,row in enumerate(allrows):
        for j,v in enumerate(row,1):
            c=s.cell(rr,j,v); c.font=F; c.alignment=WR; c.border=BD
            if example and k==0: c.fill=EX
            elif headers[j-1] in fillcols: c.fill=FILL
            elif hold_col and isinstance(row[hold_col],str) and (row[hold_col].startswith('Hold') or row[hold_col].startswith('To be rebuilt') or row[hold_col].startswith('Old')): c.fill=HOLD
        rr+=1
    last=max(rr-1,2)+150
    if status_col:
        col=get_column_letter(headers.index(status_col)+1)
        dv=DataValidation(type='list',formula1='"Draft,Final,Keep,Cut"',allow_blank=True); s.add_data_validation(dv); dv.add(f'{col}2:{col}{last}')
    s.auto_filter.ref=f'A1:{get_column_letter(len(headers))}{rr-1}'
    return s, rr-1

# ---------- Tasks
T=[
('H-10','Tutorial page texts (final pass)','Start of each memory and search level','Resources/Sequences/**/*_Panels.asset (8 pages)','Built','Tutorial pages',''),
('H-12','Mary takes Margaret\'s lines: the hand-offs between tellers and her closing lines','The storytelling cutscene at the hearth','Hearth/Hearth_InitialDialogue.asset; Memory2Lucy_End_Cutaway (node 3); HomeVisits/Yard_BondReached (node 1)','Mary has no dialogue character yet (X-12): lines show in the narrator box until then','Lines (Task H-12), New lines',''),
('H-14','Memory 1 opens on Ryker','Memory 1, before control','Hearth/Memory1Linda/Memory1Linda_Start_DialogNodeSequence.asset','Built (the camera shot is new, chunk 2.2)','Lines',''),
('H-17','Mark interrupts at the end of memory 3, leading into his telling','Memory 3 end cutaway','Hearth/Memory3John/Memory3John_End_Cutaway_DialogNodeSequence.asset','Built (Mark already speaks there)','Lines',''),
('H-20','John\'s line or bark while he holds the den mouth','Memory 4, the Hold','Hearth/Memory4Mark/Memory4Mark_Hold_John_DialogNodeSequence.asset','Built','Lines',''),
('H-21','Cyclone steer page: how to steer it','Memory 2, right after Lucy\'s first Cyclone','(new page; Claude creates it)','Not built (needs chunk 2.1)','Tutorial pages (new rows)',''),
('H-22','Ryker by the fire; she slips out before the last memory (any line for when they notice)','Home, storytelling idle','HomeVisits/Hearth_Close_DialogNodeSequence.asset','Built (the idle change is chunk 2.4)','Lines, New lines',''),
('E-01 to E-04','The Hearth ending: they notice Ryker isn\'t there, Lucy goes out, "The day after", the morning worry','Home after memory 4','Hearth/Memory4Mark/Memory4Mark_End_*; HomeVisits/Hearth_Close; HomeVisits/Hearth_WorldMapRule','Lines built; the new order is chunk 2.4','Lines, New lines','Today "Ryker\'s gone!" is said at memory 4\'s end; in the new order they only notice she isn\'t there, and worry the next morning'),
('M1-02, M1-03','M1: the Masher setup, Catch & Return, Linda\'s and Mark\'s Family Roles','M1 (the Ridge reworked)','Resources/Sequences/M1Ridge/*','Hold: M1 is being redesigned','Lines','Write for the beats; wait for the redesign before final'),
('M2-02, M2-04, M2-06','M2: Shield Flare, the Pile (Ryker\'s clue only), Lucy\'s and John\'s Roles','M2 (the River reworked)','Search/River/* today; Search/Trail/Trail_Pile_* (moves to M2)','To be rebuilt (chunk 3.2)','Lines',''),
('M3-06, M3-07','M3: the defence, "Still counting?" at the end, Toba appears; at Home the house reacts to Toba, then the Linda–Lucy scene','M3 and the Home visit after it','Search/Trail/*, SistersTally/*, HomeVisits/Yard_*','To be rebuilt (chunk 3.3); Toba\'s appearance and the house\'s reaction are new','Lines, New lines',''),
('M4-03','M4: the cleanse fight, Mithra\'s Rest, the Goblin Queen and saving Ryker','M4 (3 levels)','Resources/Sequences/Mission 4/* (today\'s 7-level Rootwell)','To be rebuilt (chunk 3.4); the duel is cut, so most of today\'s lines change','Lines, New lines',''),
('X-02','Synergy barks: a line when a Synergy fires','Combat','Resources/BarkSystemData/Abilities/DuoAbilities/*.csv (same format)','The trigger is to check (chunk 4.2)','Barks (new rows at the bottom)',''),
('X-03','Fewer, more directed barks (spoken to someone)','Combat','Resources/BarkSystemData/**/*.csv','Built','Barks','Mark Cut on lines to drop; use Tag for who it\'s said to'),
('X-05','New names for every enemy except the Claws','Enemy introduction cards, logs, UI','(enemy data; Claude finds the fields)','Built','Names and text',''),
('X-08','A quiver item for Linda in the Workshop (name, description)','Workshop','(new item)','Not built (chunk 4.5)','Names and text',''),
('X-12','Lines for Kevin, Ben and Mary in story dialogue','Home scenes','(new dialogue characters)','Not built (chunk 4.1)','New lines',''),
('X-16','Every ability description in one voice: no first or third person','Ability tooltips','Resources/UnitSpecific/Player/<hero>/**/*.asset (title, description)','Built','Names and text','Example shape: "Fires an arrow that pierces every enemy in a line."'),
('X-18','Skill tree tutorial','Home, first time the skill tree opens','(new page)','Not built (chunk 4.3)','Tutorial pages (new rows)',''),
('W-01','Mission names and descriptions','World map','Content/Levels/*.asset (missionName, description)','Built','Names and text',''),
('W-07','Mark\'s character description','Character select','(Claude finds the field)','Built','Names and text',''),
]
s,_=sheet('Tasks',['Task','What to write','Where it plays','Files in the project (under '+P+')','Container','Tab','Notes'],[14,48,30,52,34,22,40],[list(t) for t in T],[])

# ---------- Lines
rows=[]
for r in R:
    if r['kind']!='dialogue': continue
    f=r['file']; lid=f"{stem(f)}#{r['index']:02d}"
    rows.append([lid, task(f,r['text']), where(f), cont(f), f, r['index'], r['speaker'] or '(set by the level)', r['text'], '', '', '', ''])
ex=['(example) Memory4Mark_Hold_John#00','H-20','Hearth','Built','Resources/Sequences/Hearth/Memory4Mark/Memory4Mark_Hold_John_DialogNodeSequence.asset',0,'John',"I'll hold them off. You save them.",'','Go. I\'ve got the mouth.','Draft','Shorter; he\'s already fighting']
s,nl=sheet('Lines',['Line ID','Task','Area','Container','File (under '+P+')','Node','Speaker','Current text','New speaker','New text','Status','Writer notes'],
          [34,10,12,30,48,6,16,52,14,52,10,30],rows,['New speaker','New text','Status','Writer notes'],hold_col=3,example=ex,status_col='Status')

# ---------- New lines
NL=[]
def add(task,moment,speaker,note=''): NL.append([f'NEW-{len(NL)+1:02d}',task,moment,'(Claude creates)',speaker,'',note,'',''])
add('H-12','Hearth: hand-off to Linda (first teller)','Mary','Was Margaret\'s "Eldest first. Linda."')
add('H-12','Hearth: hand-off to Lucy','Mary','Was Margaret\'s "Then you tell it, Lucy."')
add('H-12','Hearth: hand-off to Mark','Mary','Was Margaret\'s "Sit, Mark. Tell it."')
add('H-12','Hearth: closing line after the last memory','Mary','Was Margaret\'s "Every one of you saved her. That\'s the only version I believe."')
add('E-01','Home: they notice Ryker isn\'t by the fire (not worried yet)','Lucy / any','')
add('E-01','Home: Lucy goes out to look for her','Lucy','')
add('E-04','Card after the fade','(card)','"The day after" or your wording')
add('E-04','Home, next morning: the worry starts','any','"The door\'s open. Ryker\'s gone." stays here today')
add('M3-06','M3 end: Toba appears, shows the way to the Rootwell, says he knows where Ryker is','Toba, family','')
add('M3-07','Home after M3: the house reacts to Toba','family','Before the Linda–Lucy scene')
add('M4-03','M4 end: saving Ryker','family','')
add('X-12','Kevin: a line in a Home scene','Kevin','Where: your pick; Claude places it')
add('X-12','Ben: a line in a Home scene','Ben','')
add('X-12','Mary: a line in a Home scene','Mary','')
s,_=sheet('New lines',['Line ID','Task','Moment','File','Speaker','New text','Notes','Status','Writer notes'],[10,10,52,16,14,52,40,10,30],NL,['Speaker','New text','Status','Writer notes'],status_col='Status')

# ---------- Tutorial pages
TP=[]
for r in R:
    if r['kind']!='tutorial': continue
    TP.append([f"{stem(r['file'])}#p{r['index']}", '', r['file'], r['index'], r['title'], r['text'], 'yes' if r['image'] else 'no', 'yes' if r['video'] else 'no', '', '', '', ''])
for t,(task_,ttl) in enumerate([('H-21','Steering the Cyclone'),('X-18','The skill tree')]):
    TP.append([f'NEW-P{t+1}',task_,'(Claude creates)','',ttl,'','','','','','',''])
for row in TP:
    f=row[2]
    row[1]=row[1] or ('H-10' if 'Hearth' in f else 'H-10 / level rebuild')
s,_=sheet('Tutorial pages',['Page ID','Task','File (under '+P+')','Page','Current title','Current text','Image','Video','New title','New text','Status','Writer notes'],
          [26,12,48,6,22,56,7,7,22,56,10,30],TP,['New title','New text','Status','Writer notes'],status_col='Status')

# ---------- Names and text
NT=[]
for r in R:
    if r['kind']=='mission': NT.append(['W-01','Mission',r['file'],'missionName / description',r['name'],r['text'],'','','',''])
for r in R:
    if r['kind']=='ability':
        hero='Toba' if r['hero']=='Dom' else r['hero']
        NT.append(['X-16',f'Ability ({hero})',r['file'],'title / description',r['name'],r['text'],'','','',''])
for e in ['Archer Goblin','Masher Goblin','Dark Worm','Dark Shaman','Goblin Queen']:
    NT.append(['X-05','Enemy name','(Claude finds the fields)','name',e,'','','','',''])
NT.append(['W-07','Character description','(Claude finds the field)','description','Mark','','','','',''])
NT.append(['X-08','Workshop item','(new item)','name / description','Linda\'s quiver','','','','',''])
s,_=sheet('Names and text',['Task','Kind','File (under '+P+')','Field','Current name','Current text','New name','New text','Status','Writer notes'],
          [8,18,52,20,24,56,24,56,10,30],NT,['New name','New text','Status','Writer notes'],status_col='Status')

# ---------- Barks
B=[]
for r in R:
    if r['kind']!='bark': continue
    B.append([f"{os.path.basename(r['file']).replace('.csv','')}#{r['index']}", 'X-03', r['file'], r['index'], r['speaker'], r.get('tag',''), r['text'], '', '', '', ''])
for k in range(1,9):
    B.append([f'NEW-B{k}','X-02','Resources/BarkSystemData/Abilities/DuoAbilities/ (new Synergy file)','','','','','','','',''])
s,_=sheet('Barks',['Bark ID','Task','File (under '+P+')','CSV row','Unit','Tag (who it\'s said to)','Current line','New line','New tag','Status','Writer notes'],
          [34,8,52,7,10,14,52,52,12,10,30],B,['New line','New tag','Status','Writer notes'],status_col='Status')

# progress formulas on Read me
ws=wb['Read me']
base=PR+2
stcol={'Lines':'K','New lines':'H','Tutorial pages':'K','Names and text':'I','Barks':'J'}
for i,t in enumerate(tabs):
    row=base+i
    ws.cell(row,1,t).font=F
    s0=3 if t=='Lines' else 2
    ws.cell(row,2,f"=COUNTA('{t}'!A{s0}:A2000)").font=F
    ws.cell(row,3,f"=COUNTIF('{t}'!{stcol[t]}{s0}:{stcol[t]}2000,\"Final\")").font=F
    ws.cell(row,4,f"=COUNTIF('{t}'!{stcol[t]}{s0}:{stcol[t]}2000,\"Draft\")").font=F
wb.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),'narrative-sheet.xlsx'))
print('rows', len(rows), len(NL), len(TP), len(NT), len(B))
