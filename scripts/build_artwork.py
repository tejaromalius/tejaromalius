#!/usr/bin/env python3
"""Create editable, dependency-free, GitHub-compatible Command Deck SVG assets."""
from pathlib import Path
from math import sin,cos,pi

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets'
OUT.mkdir(exist_ok=True)
THEME={
  'obsidian':'#140d0d',
  'shadow':'#241716',
  'panel':'#2f1d1a',
  'panel_hi':'#4f2f26',
  'oxblood':'#6f1f2d',
  'crimson':'#8b2a37',
  'bronze':'#8b5236',
  'copper':'#b26f4a',
  'antique_gold':'#d4ab78',
  'bone':'#ead8c5',
  'muted':'#b59b8b',
  'smoke':'#8a7267',
}

def svg(name,body,w,h):
  defs='''<defs><linearGradient id="base" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#140d0d"/><stop offset=".56" stop-color="#241716"/><stop offset="1" stop-color="#4f2f26"/></linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#b26f4a"/><stop offset=".58" stop-color="#d4ab78"/><stop offset="1" stop-color="#8b2a37"/></linearGradient><radialGradient id="fog"><stop stop-color="#8b2a37" stop-opacity=".24"/><stop offset=".55" stop-color="#b26f4a" stop-opacity=".08"/><stop offset="1" stop-color="#8b2a37" stop-opacity="0"/></radialGradient><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="#d4ab78" stroke-opacity=".08" stroke-width=".7"/></pattern><filter id="bloom" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter></defs>'''
  full=f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Tejaromalius Command Deck artwork" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{defs}{body}</svg>'
  (OUT/name).write_text(full,encoding='utf-8')

def line(x1,y1,x2,y2,stroke='#b26f4a',opacity=.24,sw=1,dash=''):
  return f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{opacity}" fill="none" '+(f'stroke-dasharray="{dash}"' if dash else '')+'/>'

def txt(x,y,t,size=16,color='#d7f0ff',spacing=None,weight=400,anchor='start',family='ui-monospace,Consolas,monospace'):
  import html
  ls=f' letter-spacing="{spacing}"' if spacing is not None else ''
  return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" font-family="{family}"{ls}>{html.escape(t)}</text>'

# HERO: intentionally asymmetrical, like a control-room viewport, not a generic banner.
b=['<rect width="1200" height="430" rx="18" fill="url(#base)"/>','<rect width="1200" height="430" fill="url(#grid)" opacity=".9"/>','<ellipse cx="1004" cy="209" rx="305" ry="268" fill="url(#fog)"/>']
b += [f'<circle cx="{(i*137+59)%1150}" cy="{(i*73+23)%405}" r="{.7+i%2*.4}" fill="{["#b26f4a","#8b2a37","#ead8c5"][i%3]}" opacity=".33"/>' for i in range(48)]
b += ['<path d="M18 70V18H69 M1130 18H1182V70 M18 360V412H69 M1130 412H1182V360" stroke="#d4ab78" stroke-width="2" opacity=".7" fill="none"/>',line(40,80,720,80,opacity=.28),line(39,332,715,332,opacity=.28)]
b += [txt(44,47,'// TEJAROMALIUS / INTERACTIVE SYSTEMS',15,'#d4ab78',2,700), txt(716,47,'PORTFOLIO // GITHUB',13,'#b59b8b',1,anchor='end'), txt(44,115,'[ 01 / IDENTITY ]',14,'#b26f4a',2)]
b += [txt(42,195,'TEJAROMALIUS',76,'#ead8c5',-3,800,family='Arial,Helvetica,sans-serif'),txt(46,226,'ENGINEERING    /    DEVOPS    /    RESEARCH',16,'#d4ab78',1.9,600),txt(46,276,'Turning chaos into code, one line at a time.',20,'#c7b3a0',0,400,family='Arial,Helvetica,sans-serif')]
b += ['<rect x="44" y="302" rx="4" width="256" height="25" fill="#2a1b19" stroke="#8b5236"/>',txt(56,319,'LOCATION // IZMIR · TR',12,'#d7bf9c',1.2),'<rect x="314" y="302" rx="4" width="238" height="25" fill="#3a141d" stroke="#8b2a37"/>',txt(326,319,'MODE // BUILD & EXPLORE',12,'#d9b79a',1.1)]
# radial reactor
cx,cy=980,213
b += [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity="{o}" stroke-width="{sw}" stroke-dasharray="{dash}"/>' for r,c,o,sw,dash in [(149,'#b26f4a',.22,1,'5 11'),(131,'#d4ab78',.8,2,'72 13 7 14'),(112,'#8b2a37',.45,1,'14 12'),(93,'#d4ab78',.55,1,'2 7'),(73,'#b26f4a',.6,3,'47 18')]]
# arcs and spokes
for i in range(18):
  a=2*pi*i/18
  r0=152 if i%3 else 160; r1=172 if i%3 else 187
  b.append(line(round(cx+cos(a)*r0,1),round(cy+sin(a)*r0,1),round(cx+cos(a)*r1,1),round(cy+sin(a)*r1,1),'#d4ab78',.55,1.2))
for i in range(6):
  a=pi*i/3+pi/6
  x=round(cx+cos(a)*61,1);y=round(cy+sin(a)*61,1)
  b.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#ead8c5" opacity=".95"/>')
b += [f'<path d="M{cx} {cy-51}L{cx+45} {cy-26}L{cx+45} {cy+26}L{cx} {cy+51}L{cx-45} {cy+26}L{cx-45} {cy-26}Z" stroke="#d4ab78" stroke-width="2" fill="#3a231f"/>',f'<path d="M{cx-30} {cy+8} Q{cx-13} {cy-34} {cx+5} {cy+6} Q{cx+17} {cy+28} {cx+31} {cy-22}" fill="none" stroke="#8b2a37" stroke-width="4" stroke-linecap="round"/>',f'<circle cx="{cx+30}" cy="{cy-22}" r="4.5" fill="#d4ab78"/>',f'<circle cx="{cx}" cy="{cy}" r="14" fill="none" stroke="#ead8c5" stroke-width="1.5"/>',txt(cx,cy+79,'T / 72',12,'#b59b8b',2,700,anchor='middle')]
# bottom mini telemetry, decorative only
for i,(a,d) in enumerate([('NODE-A','READY'),('NODE-B','SYNC'),('NODE-C','BUILD')]):
  x=48+i*205
  b += [txt(x,380,a,11,'#8a7267',1.2,600),txt(x+90,380,d,11,'#d4ab78',.9,600),line(x,391,x+172,391,'#b26f4a',.34,1.2)]
b += [txt(1163,397,'SYS.REF / 0X72',11,'#8a7267',1.2,anchor='end'),'<path d="M724 0 L724 430" stroke="#6b5349" stroke-opacity=".17"/>']
svg('command-header.svg',''.join(b),1200,430)

# decorative divider strip
b=['<rect width="1200" height="46" fill="#1a1112"/>',line(9,23,1190,23,'#d4ab78',.37,1),'<path d="M20 12 L31 23 L20 34 M1180 12L1169 23L1180 34" stroke="#8b2a37" fill="none"/>',txt(55,18,'// DATA PATH',10,'#8a7267',1.5),txt(1150,18,'END / TRANSMISSION',10,'#8a7267',1.3,anchor='end')]
for i in range(12):
  x=398+i*36
  b.append(f'<rect x="{x}" y="21" height="5" width="{20 if i%4==0 else 8}" fill="{["#b26f4a","#8b2a37","#d4ab78"][i%3]}" opacity=".65"/>')
svg('signal-divider.svg',''.join(b),1200,46)

orgs=[('labs','LABS','01 / RESEARCH DIVISION','Systems  ·  Experiments','#d4ab78'),('contributes','CONTRIBUTES','02 / COLLABORATION','Patches  ·  Open source','#8b2a37'),('snax','SNAX','03 / SIDE QUESTS','Utilities  ·  Small builds','#b26f4a')]
for idx,(slug,name,sub,blurb,color) in enumerate(orgs):
  b=['<rect width="375" height="177" rx="14" fill="url(#base)"/>','<rect width="375" height="177" fill="url(#grid)"/>',f'<rect x="1" y="1" width="373" height="175" rx="14" fill="none" stroke="{color}" stroke-opacity=".55"/>',f'<path d="M17 51H356" stroke="{color}" stroke-opacity=".28"/>',txt(20,30,sub,11,color,1.2,700),txt(20,100,name,34,'#f0fbff',-.4,800,family='Arial,Helvetica,sans-serif'),txt(21,133,blurb,13,'#a6bbd4',.1),txt(20,159,'OPEN NAMESPACE     / /',11,color,1.3),f'<path d="M316 73h27v27h-27z" fill="none" stroke="{color}" stroke-opacity=".6" transform="rotate(45 329 87)"/>']
  if idx==0:
    b += [f'<circle cx="330" cy="87" r="12" stroke="{color}" fill="none"/>',f'<circle cx="330" cy="87" r="3" fill="{color}"/>']
  elif idx==1:
    b += [f'<path d="M316 91l13-13 13 13 M316 81l13 13 13-13" fill="none" stroke="{color}" stroke-width="2"/>']
  else:
    b += [f'<path d="M319 95l9-23 5 15 9-4" fill="none" stroke="{color}" stroke-width="2"/>']
  svg(f'org-{slug}.svg',''.join(b),375,177)

# Tech matrix: self-reported tools from provided README, not attributes of individual repos.
b=['<rect width="1200" height="203" rx="14" fill="url(#base)"/>','<rect x="1" y="1" width="1198" height="201" rx="14" fill="none" stroke="#6b5349"/>','<rect width="1200" height="203" fill="url(#grid)"/>',txt(28,34,'// LOCAL TOOLCHAIN',15,'#d4ab78',1.5,700),txt(1170,34,'OPERATOR-DEFINED / NOT REPO METADATA',11,'#8a7267',1,anchor='end')]
langs=[('RUST','#b26f4a'),('GO','#d4ab78'),('C# / .NET','#8b2a37'),('PYTHON','#d4ab78'),('TYPESCRIPT','#c7b3a0'),('REACT','#bfa596'),('FLUTTER','#ead8c5'),('DART','#c7b3a0'),('POSTGRES','#8b2a37'),('SQLITE','#8a7267'),('REDIS','#8b5236'),('DOCKER','#b59b8b'),('GIT','#d4ab78'),('ANGULAR','#8b2a37')]
for i,(name,color) in enumerate(langs):
  row=i//7; col=i%7; x=27+col*165; y=56+row*64; width=154
  b += [f'<rect x="{x}" y="{y}" width="{width}" height="45" rx="6" fill="#2a1a18" stroke="{color}" stroke-opacity=".5"/>',f'<rect x="{x+1}" y="{y+1}" width="4" height="43" rx="2" fill="{color}" opacity=".9"/>',txt(x+16,y+28,name,15,'#ead8c5',.2,700)]
svg('toolchain-matrix.svg',''.join(b),1200,203)

# foot graphics
b=['<rect width="1200" height="85" rx="13" fill="#1a1112"/>','<rect x="1" y="1" width="1198" height="83" rx="13" stroke="#6b5349" fill="none"/>','<path d="M20 40H398L425 16H740L766 40H1180" fill="none" stroke="#b26f4a" stroke-opacity=".45"/>',txt(40,62,'EOF / COMMAND DECK',13,'#d4ab78',1.7,700),txt(1148,62,'TEJAROMALIUS // SYSTEMS • RESEARCH • TOOLING',12,'#b59b8b',1.1,anchor='end')]
svg('command-footer.svg',''.join(b),1200,85)
print('Built',len(list(OUT.glob('*.svg'))),'SVG assets in',OUT)
