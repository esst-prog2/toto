from pathlib import Path
from html import escape
import shutil,json
p=Path('homework10/last-box'); (p/'assets').mkdir(exist_ok=True); (p/'compositions').mkdir(exist_ok=True)
shutil.copyfile('homework9/assets/the-pick-sheet-logo.png',p/'assets/logo.png')
shutil.copyfile('.hw9-tools/hw10/render-smoke/assets/gsap.min.js',p/'assets/gsap.min.js')
gsap_asset=p/'assets/gsap.min.js'
gsap_asset.write_text('\n'.join(line.rstrip() for line in gsap_asset.read_text().splitlines()).rstrip()+'\n')
G='#005239';Y='#ffcc00';P='#faf9f3';I='#142d24';M='#506459';L='#b6c7bb'
def text(x,y,s,size=40,fill=I,weight=400,extra=''):
 return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" {extra}>{escape(s)}</text>'
def rect(x,y,w,h,fill='none',stroke='none',extra=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" {extra}/>'
def line(x,y,x2,y2,c=L,w=2,extra=''):
 return f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}" {extra}/>'
def group(id,body,extra=''):return f'<g id="{id}" {extra}>{body}</g>'
def heading(id,s):return group(id,text(192,154,s,76,G,700))
def scene(name,body,script):
 s=f'''<template><style>#root{{position:absolute;inset:0}}svg{{font-family:Inter,Arial,sans-serif}}</style>
 <div id="root" data-composition-id="{name}" data-width="1920" data-height="1080"><svg viewBox="0 0 1920 1080" width="1920" height="1080" role="img" aria-label="Concept preview of The Pick Sheet: {name}">{body}</svg></div>
 <script>const tl=gsap.timeline({{paused:true}});{script}\nwindow.__timelines=window.__timelines||{{}};window.__timelines['{name}']=tl;</script></template>'''
 (p/f'compositions/{name}.html').write_text(s)
# A tactile ticket whose actual row lines expand into the new sheet.
ticket=rect(0,0,490,600,'#ffffff',G,'stroke-width="2" id="ticket-paper"')
ticket+=text(28,50,'13 + 1',32,G,700)
ticket+=group('ticket-toto-head',text(252,50,'1',32,G,700)+text(334,50,'X',32,G,700)+text(414,50,'2',32,G,700))
newhead=text(180,50,'Competition',36,G,700)+text(640,50,'Home team',32,G,700)+text(1130,50,'Away team',32,G,700)
ticket+=group('ticket-new-head',newhead)
for r in range(14):
 y=80+r*35
 ticket+=line(20,y,470,y,L,1,extra='class="ticket-rule"')
 if r==13:ticket+=rect(20,y+2,450,33,Y,'none','id="ticket-focus"')
 ticket+=text(28,y+27,'14 (+1)' if r==13 else str(r+1),29,G,700 if r==13 else 400)
 ticket+=group(f'ticket-boxes-{r}', ''.join(rect(x,y+8,20,20,'none',G,'stroke-width="1.5"') for x in [250,332,414]))
 ticket+=group(f'ticket-strokes-{r}',line(180,y+19,450,y+19,L,2)+line(640,y+19,940,y+19,L,2)+line(1130,y+19,1430,y+19,L,2))
body=group('ticket-carrier',ticket,'transform="translate(1050 230)"')
body+=group('ticket-title1',text(192,368,'Fourteen',88,G,700)+text(192,470,'matches',88,G,700))
body+=group('ticket-title2',text(192,368,'Which',88,G,700)+text(192,470,'outcome?',88,G,700))
body+=heading('ticket-title3','A clearer way to choose')
pencil=rect(0,-14,220,28,Y)+rect(0,-14,220,5,'#e6b400')+'<polygon points="220,-14 258,0 220,14" fill="#d4b48a"/><polygon points="250,-3 258,0 250,3" fill="#142d24"/>'+rect(-12,-14,12,28,G)
body+=group('ticket-pencil',pencil,'transform="translate(1600 636) rotate(145)"')
script="""
gsap.set('#ticket-title2,#ticket-title3,#ticket-new-head,[id^=ticket-strokes-]',{opacity:0});
tl.to('#ticket-pencil',{x:1582,y:653,duration:.45,ease:'power2.inOut'},.45);
tl.to('#ticket-pencil',{x:1595,y:641,duration:.4,ease:'power2.inOut'},1.4);
tl.to('#ticket-title1',{opacity:0,duration:.12},1.1);tl.to('#ticket-title2',{opacity:1,duration:.12},1.22);
tl.to('#ticket-title2',{opacity:0,duration:.2},2.8);tl.to('#ticket-pencil',{opacity:0,y:541,duration:.3,ease:'power3.in'},2.75);
tl.to('#ticket-carrier',{x:192,duration:.65,ease:'power2.inOut'},3);
tl.to('#ticket-paper',{attr:{width:1536},duration:.65,ease:'power2.inOut'},3);
tl.to('.ticket-rule',{attr:{x2:1516},duration:.65,ease:'power2.inOut'},3);
tl.to('#ticket-focus',{attr:{width:1496},duration:.65,ease:'power2.inOut'},3);
tl.to('#ticket-toto-head,[id^=ticket-boxes-]',{opacity:0,duration:.15},3);
tl.to('#ticket-title3,#ticket-new-head,[id^=ticket-strokes-]',{opacity:1,duration:.25},3.3);
tl.to('#ticket-focus',{attr:{y:100,height:104},duration:.55,ease:'power2.inOut'},5.45);
"""
scene('ticket',body,script)
# Manual selection. Empty-to-selected text swaps are openly illustrated, not real UI.
body=heading('entry-title','Choose competitions and teams')
fields=[('Competition','Example competition'),('Home team','Home team A'),('Away team','Away team B')]
for j,(label,value) in enumerate(fields):
 x=192+j*522
 field=text(x,300,label,42,M)+rect(x,330,492,104,'#fff',G,'stroke-width="2"')
 field+=group(f'entry-empty-{j}',text(x+24,396,'Choose…',40,M))
 field+=group(f'entry-value-{j}',text(x+24,396,value,38,G,700))
 field+=f'<path d="M{x+446} 375 l10 12 10 -12" fill="none" stroke="{G}" stroke-width="3"/>'
 body+=group(f'entry-field-{j}',field)
 body+=group(f'entry-option-{j}',rect(x,455,492,84,Y)+text(x+24,510,value,38,I,700))
body+=line(192,640,1728,640,G,2)
for r in range(14):
 x=192+r*111
 body+=rect(x,688,90,70,Y if r==13 else 'none',G,'stroke-width="1.5"')+text(x+45,733,str(r+1),30,G,700,extra='text-anchor="middle"')
body+=text(192,840,'14 matches · entered manually',40,M)
body+=group('entry-cursor','<path d="M0 0 L0 64 L17 48 L31 78 L45 71 L31 42 L58 42 Z" fill="#005239" stroke="#faf9f3" stroke-width="3"/>','transform="translate(455 420)"')
script="gsap.set('[id^=entry-option-],[id^=entry-value-]',{opacity:0});"
for j in range(3):
 t=.25+j*1.25
 script+=f"tl.to('#entry-cursor',{{x:{j*522},duration:.3,ease:'power2.inOut'}},{t});tl.to('#entry-option-{j}',{{opacity:1,duration:.14}},{t+.3});tl.set('#entry-empty-{j}',{{opacity:0}},{t+1.05});tl.set('#entry-value-{j}',{{opacity:1}},{t+1.05});tl.to('#entry-option-{j}',{{opacity:0,duration:.12}},{t+1.5});"
script+="tl.fromTo('[id^=entry-field-] > rect',{fill:'#ffcc00'},{fill:'#ffffff',duration:.4,ease:'power2.inOut'},0);tl.to('#entry-cursor',{opacity:0,duration:.2},4.2);tl.fromTo('#entry-title',{opacity:0},{opacity:1,duration:.15},0);"
scene('entry',body,script)
# Three equal estimate rails, no numerical prediction. The same grid returns as one table.
body=heading('compare-title1','Compare all three outcomes')+heading('compare-title2','Suggest the most likely')+heading('compare-title3','One table. Every match.')
compare=text(192,282,'Estimated probabilities',52,G,700)
for j,label in enumerate(['1 · Home win','X · Draw','2 · Away win']):
 x=192+j*522
 compare+=group(f'compare-col-{j}',text(x,382,label,44,G,700)+line(x,414,x+492,414,G,2)+text(x+246,532,'—',100,G,400,'text-anchor="middle"')+rect(x,570,492,14,'none',G,'stroke-width="2"'))
compare+=text(192,658,'Historical results → statistical model',36,M)
compare+=line(192,694,1728,694,Y,6,extra='id="compare-guide"')
compare+=group('compare-recommendation',text(192,784,'Recommended outcome —',50,G,700))
body+=group('compare-detail',compare)
table=rect(192,230,1536,600,'#fff',G,'stroke-width="2"')
for x,label in [(216,'Match'),(358,'Competition / teams'),(1060,'1'),(1180,'X'),(1300,'2'),(1450,'Pick')]:table+=text(x,278,label,30,G,700)
for r in range(14):
 y=306+r*35
 table+=line(212,y,1708,y,L,1)+text(216,y+27,str(r+1),30,G)
 if r==10:table+=rect(330,y+2,1370,32,Y,'none','id=\"compare-unavailable-fill\"')+text(358,y+27,'Insufficient history',32,I,700)
 else:
  table+=line(358,y+19,830,y+19,L,2)
  for x in [1060,1180,1300,1450]:table+=text(x,y+27,'—',32,G)
body+=group('compare-table',table)
script="""
gsap.set('#compare-title2,#compare-title3,#compare-table,#compare-recommendation',{opacity:0});
tl.fromTo('#compare-col-0,#compare-col-1,#compare-col-2',{opacity:0,y:12},{opacity:1,y:0,duration:.35,stagger:.1,ease:'power4.out'},0);
tl.fromTo('#compare-guide',{attr:{x2:192}},{attr:{x2:1728},duration:1,ease:'power2.inOut'},1.2);
tl.to('#compare-title1',{opacity:0,duration:.12},2.88);tl.to('#compare-title2,#compare-recommendation',{opacity:1,duration:.18},3);
tl.to('#compare-title2',{opacity:0,duration:.12},5.85);
tl.to('#compare-detail',{scale:.75,transformOrigin:'960px 540px',opacity:0,duration:.22,ease:'power3.in'},5.7);
tl.fromTo('#compare-table',{opacity:0,scale:1.04,transformOrigin:'960px 540px'},{opacity:1,scale:1,duration:.45,ease:'power4.out'},6);
tl.to('#compare-title3',{opacity:1,duration:.18},6);tl.to('#compare-unavailable-fill',{attr:{x:842,y:405,width:6,height:233},duration:.4,ease:'power2.inOut'},8.6);tl.to('#compare-table > text,#compare-table > line,#compare-table > rect:first-child,#compare-title3',{opacity:0,duration:.25},8.7);
"""
scene('compare',body,script)
# Historical reconstruction: data physically stops before the previous meeting.
body=heading('history-title1','Their most recent meeting')+heading('history-title2','Use only earlier information')+heading('history-title3','Prediction then ↔ Actual result')
timeline=text(244,360,'Earlier history',48,G,700)+text(900,360,'Last meeting',48,G,700)+text(1450,360,'Your match',48,G,700)
timeline+=line(260,530,1660,530,G,3,extra='id=\"history-axis\"')
for x in [300,420,540]:
 timeline+=rect(x,425,58,64,'#fff',G,'stroke-width="2"')+line(x+10,444,x+45,444,L,2)+line(x+10,458,x+45,458,L,2)+line(x+10,473,x+37,473,L,2)
timeline+=rect(842,405,6,233,Y)+text(845,700,'Information cutoff',36,M,400,'text-anchor="middle"')
timeline+=rect(980,455,5,140,G)+rect(1580,455,5,140,G)
timeline+=group('history-past-data',rect(610,507,38,46,Y))
timeline+=text(192,795,'Prediction then —',48,G,700)
body+=group('history-timeline',timeline)
comparison=rect(192,360,680,330,'#fff',G,'stroke-width="2"')+text(230,437,'Prediction then',48,G,700)+text(532,610,'—',110,G,400,'text-anchor="middle"')
comparison+=group('history-actual',rect(1048,360,680,330,'#fff',G,'stroke-width="2"')+text(1086,437,'Actual result',48,G,700)+text(1388,610,'—',110,G,400,'text-anchor="middle"'))
comparison+=line(872,525,1048,525,Y,6,extra='id="history-bracket"')+text(192,804,'Where reliable history is available',40,M)
body+=group('history-comparison',comparison)
script="""
gsap.set('#history-title2,#history-title3,#history-comparison,#history-actual',{opacity:0});
tl.fromTo('#history-axis',{attr:{x1:842,x2:842}},{attr:{x1:260,x2:1660},duration:.5,ease:'power2.inOut'},0);tl.to('#history-past-data',{x:185,duration:.65,ease:'power2.inOut'},1.9);
tl.to('#history-title1',{opacity:0,duration:.12},1.88);tl.to('#history-title2',{opacity:1,duration:.12},2);
tl.to('#history-title2,#history-timeline',{opacity:0,duration:.2},3.8);
tl.to('#history-title3,#history-comparison',{opacity:1,duration:.18},4);
tl.fromTo('#history-actual',{opacity:0,x:45},{opacity:1,x:0,duration:.3,ease:'power4.out'},4.25);
tl.fromTo('#history-bracket',{attr:{x2:872}},{attr:{x2:1048},duration:.3,ease:'power2.inOut'},4.3);tl.to('#history-bracket',{attr:{x1:370,x2:1550,y1:530,y2:530},duration:.35,ease:'power2.inOut'},6.65);tl.to('#history-comparison > rect,#history-comparison > text,#history-actual,#history-title3',{opacity:0,duration:.2},6.75);
"""
scene('history',body,script)
# Original brand asset, unmodified pixels and proportional dimensions.
body=group('close-lockup','<image id="close-logo" href="assets/logo.png" x="370" y="270" width="1180" height="271.4" preserveAspectRatio="xMidYMid meet"/>'+text(960,655,'Explore the project',48,G,400,'text-anchor="middle"')+text(960,753,'esst-prog2.github.io/toto/',64,G,700,'text-anchor="middle"'))
body+=line(370,530,1550,530,Y,6,extra='id="close-carry"')
script="""
tl.fromTo('#close-lockup',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.35,ease:'power2.inOut'},0);
tl.to('#close-carry',{opacity:0,duration:.15},.25);
"""
scene('close',body,script)
# Topmost, independent status: no scene transition can cover or fade it.
body=line(192,908,1728,908,L,1)+text(192,968,'Concept preview · In development',56,G,700)
body+=group('status-no-data',text(192,870,'Illustration only · No prediction data',42,M,400))
scene('status',body,"gsap.set('#status-no-data',{opacity:0});tl.set('#status-no-data',{opacity:1},11);tl.set('#status-no-data',{opacity:0},27);")
scenes=[('ticket',0,6),('entry',6,5),('compare',11,9),('history',20,7),('close',27,3)]
hosts='\n'.join(f'<div id="{n}" class="clip" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="{s}" data-duration="{d}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:1"></div>' for n,s,d in scenes)
hosts+='<div id="status" class="clip" data-composition-id="status" data-composition-src="compositions/status.html" data-start="0" data-duration="30" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index:10;pointer-events:none"></div>'
(p/'index.html').write_text(f'''<!doctype html><html lang="en" data-composition-variables='[{{"id":"paper","type":"color","label":"Paper","default":"#faf9f3"}}]'><head><meta charset="utf-8"><meta name="viewport" content="width=1920,height=1080"><title>The Pick Sheet — The Last Box · concept preview</title><script src="assets/gsap.min.js"></script><style>*{{box-sizing:border-box;margin:0}}html,body{{width:1920px;height:1080px;overflow:hidden;background:{P}}}#root{{position:relative;width:1920px;height:1080px;background:var(--paper,{P});color:{I};font-family:Inter,Arial,sans-serif}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="30" data-width="1920" data-height="1080" data-fps="30">{hosts}</div><script>window.__timelines=window.__timelines||{{}};window.__timelines.main=gsap.timeline({{paused:true}});</script></body></html>''')
(p/'ASSETS.json').write_text(json.dumps({'logo':{'source':'../../homework9/assets/the-pick-sheet-logo.png','file':'assets/logo.png','use':'Approved supplied brand asset, copied without edits'},'animation':{'file':'assets/gsap.min.js','version':'3.15.0','source':'Official GSAP npm CDN asset already downloaded for the setup test'},'fonts':{'family':'Inter','source':'HyperFrames bundled/cached Google Fonts renderer'}},indent=2)+'\n')
print('Built five continuous narrative scenes and an independent persistent-disclosure composition.')
