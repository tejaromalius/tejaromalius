#!/usr/bin/env python3
"""Sync GitHub About descriptions to a GitHub-compatible profile README.

Only `description` from GitHub's repository REST API is used as descriptive
project copy. Missing/nonpublic repos are not rendered. No dependencies.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import textwrap
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
CARDS = ROOT / 'assets' / 'projects'
BEGIN = '<!-- REPOSITORY_REGISTRY:START -->'
END = '<!-- REPOSITORY_REGISTRY:END -->'
THEME = {
    'panel_1': '#1b1110',
    'panel_2': '#31201c',
    'dots': '#d4ab78',
    'text_main': '#ead8c5',
    'text_muted': '#c7b3a0',
    'text_dim': '#8a7267',
    'rule': '#8b5236',
}

OWNERS = (
    ('tejaromalius-labs', 'LABS / PUBLIC RESEARCH', '#d4ab78', 4, ('Comprenchmark', 'BitonicBreaker')),
    ('tejaromalius-contributes', 'CONTRIBUTES / OPEN SOURCE', '#8b2a37', 2, ('Adaptive-Tab-Bar-Colour-Asus-Edition',)),
    ('tejaromalius-snax', 'SNAX / SMALL BUILDS', '#b26f4a', 4, ('PilotFan', 'SmartToDock', 'Tigit', 'Scribdify')),
)
REPO_NAME = re.compile(r'^[A-Za-z0-9_.-]+$')


def _api_get(url: str):
    token = os.environ.get('GITHUB_TOKEN', '').strip()
    headers = {
        'Accept': 'application/vnd.github+json',
        'User-Agent': 'Tejaromalius-Profile-Repository-Sync',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = Request(url, headers=headers)
    with urlopen(req, timeout=25) as resp:
        return json.load(resp)


def fetch_public_repos():
    repos = []
    for owner, *_ in OWNERS:
        for page in range(1, 11):  # 1,000 per owner max; fail closed if API fails.
            batch = _api_get(f'https://api.github.com/orgs/{owner}/repos?type=public&per_page=100&page={page}')
            if not isinstance(batch, list):
                raise ValueError(f'Unexpected repository listing for {owner}')
            for r in batch:
                if r.get('owner', {}).get('login', '').lower() != owner.lower():
                    continue
                repos.append(r)
            if len(batch) < 100:
                break
    return repos


def cleaned(r, owner):
    if r.get('owner', {}).get('login', '').lower() != owner.lower():
        return None
    name = r.get('name', '')
    description = r.get('description')
    if not isinstance(name, str) or not REPO_NAME.fullmatch(name):
        return None
    if not isinstance(description, str) or not description.strip():
        return None
    if r.get('private') or r.get('archived') or r.get('disabled'):
        return None
    # API `description` is the SOLE source of project descriptive information.
    return {
        'owner': owner, 'name': name, 'description': description,
        'url': f'https://github.com/{owner}/{name}',
        'pushed_at': str(r.get('pushed_at') or ''),
    }


def select_repos(data):
    selected = []
    for owner, label, accent, cap, pinned in OWNERS:
        valid = [x for r in data if (x := cleaned(r, owner)) is not None]
        by_name = {r['name'].lower(): r for r in valid}
        pinned_set = {n.lower() for n in pinned}
        preferred = [by_name[n.lower()] for n in pinned if n.lower() in by_name]
        additional = sorted((r for r in valid if r['name'].lower() not in pinned_set),
                            key=lambda r: (r['pushed_at'], r['name'].lower()), reverse=True)
        picks = (preferred + additional)[:cap]
        if picks:
            selected.append((owner, label, accent, picks))
    if not selected:
        raise ValueError('No public repositories with descriptions found; README preserved unchanged.')
    return selected


def wrap_text(s, width):
    # Do not rephrase or truncate the GitHub description; only insert SVG line wraps.
    return textwrap.wrap(s.replace('\r', ' ').replace('\n', ' '), width,
                         break_long_words=True, break_on_hyphens=True)


def make_card(repo, accent, number):
    name, desc, owner = repo['name'], repo['description'], repo['owner']
    name_lines = wrap_text(name, 32)
    desc_lines = wrap_text(desc, 52)
    name_line_h = 28
    desc_line_h = 23
    name_start = 68
    desc_start = name_start + (len(name_lines) - 1) * name_line_h + 42
    foot_y = desc_start + (len(desc_lines) - 1) * desc_line_h + 36
    h = max(213, foot_y + 26)
    def tx(x,y,value,sz,color,weight=400,space=0):
        return (f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" '
                f'font-size="{sz}" font-weight="{weight}" letter-spacing="{space}" '
                f'fill="{color}">{html.escape(value, quote=True)}</text>')
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="560" height="{h}" viewBox="0 0 560 {h}" '
        f'role="img" aria-label="{html.escape(name, quote=True)}: {html.escape(desc, quote=True)}">',
        f'<defs><linearGradient id="panel" x2="1" y2="1"><stop stop-color="{THEME["panel_1"]}"/>'
        f'<stop offset="1" stop-color="{THEME["panel_2"]}"/></linearGradient>'
        '<pattern id="dots" width="27" height="27" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r=".75" fill="{THEME["dots"]}" opacity=".16"/></pattern></defs>',
        f'<rect width="560" height="{h}" rx="12" fill="url(#panel)"/>',
        f'<rect width="560" height="{h}" rx="12" fill="url(#dots)"/>',
        f'<rect x="1" y="1" width="558" height="{h-2}" rx="12" fill="none" stroke="{accent}" stroke-opacity=".50"/>',
        f'<rect x="18" y="18" width="5" height="{h-36}" rx="2" fill="{accent}" opacity=".82"/>',
        f'<path d="M34 40 H526" stroke="{accent}" opacity=".32"/>',
        tx(38,31,f'GITHUB / {owner.upper()}',11,accent,700,1.1),
        tx(514,31,f'{number:02}',13,THEME['text_dim'],700,1.1),
    ]
    for i,t in enumerate(name_lines):
        parts.append(tx(39,name_start+i*name_line_h,t,24,THEME['text_main'],700,-.3))
    parts.append(f'<path d="M39 {desc_start-26} H514" stroke="{THEME['rule']}" opacity=".34"/>')
    for i,t in enumerate(desc_lines):
        parts.append(tx(39,desc_start+i*desc_line_h,t,16,THEME['text_muted'],400,.12))
    parts.extend([
        f'<path d="M39 {foot_y-13} H514" stroke="{accent}" opacity=".23"/>',
        tx(39,foot_y+7,'SOURCE  /  GITHUB ABOUT DESCRIPTION',11,accent,600,1),
        f'<path d="M513 {foot_y-5} h12 v-12 m0 12 l-13 0" fill="none" stroke="{accent}" stroke-width="2"/>',
        '</svg>',
    ])
    path = CARDS / (owner+'--'+name+'.svg')
    path.write_text(''.join(parts),encoding='utf-8')
    return path


def render_registry(selected):
    blocks = ['<p align="right"><sub>SOURCE / GITHUB REPOSITORY ABOUT → DESCRIPTION · REGENERATED BY GITHUB ACTIONS</sub></p>']
    used_paths = set()
    number = 0
    for owner, heading, accent, repos in selected:
        blocks.append(f'\n#### `{heading}`\n')
        blocks.append('<table><tbody>')
        for i in range(0,len(repos),2):
            blocks.append('<tr>')
            for repo in repos[i:i+2]:
                number+=1
                card=make_card(repo,accent,number)
                used_paths.add(card)
                src=card.relative_to(ROOT).as_posix()
                title=html.escape(repo['name'],quote=True)
                descr=html.escape(repo['description'],quote=True)
                blocks.append(f'<td width="50%" valign="top"><a href="{repo["url"]}">'
                              f'<img src="./{src}" alt="{title}: {descr}" width="100%" />'
                              '</a></td>')
            if len(repos[i:i+2]) == 1:
                blocks.append('<td width="50%"></td>')
            blocks.append('</tr>')
        blocks.append('</tbody></table>')
    return '\n'.join(blocks)+'\n',used_paths


def replace_section(content, replacement):
    if content.count(BEGIN)!=1 or content.count(END)!=1:
        raise ValueError('README must contain one matching pair of registry markers')
    start=content.index(BEGIN)+len(BEGIN)
    end=content.index(END)
    if start>=end:
        raise ValueError('Repository registry markers reversed')
    return content[:start]+'\n'+replacement+content[end:]


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--snapshot',type=Path,help='Offline verification fixture; normal Actions use the GitHub API')
    args=p.parse_args()
    if args.snapshot:
        data=json.loads(args.snapshot.read_text(encoding='utf-8'))
        if not isinstance(data,list):
            raise ValueError('Snapshot must be a list of GitHub-shaped repository metadata')
    else:
        data=fetch_public_repos()
    chosen=select_repos(data)
    CARDS.mkdir(parents=True,exist_ok=True)
    content,used_paths=render_registry(chosen)
    updated=replace_section(README.read_text(encoding='utf-8'),content)
    README.write_text(updated,encoding='utf-8')
    # Remove only our generated per-repository cards after a successful API refresh.
    for stale in CARDS.glob('*.svg'):
        if stale not in used_paths:
            stale.unlink()
    print(f'Synced {sum(len(x[3]) for x in chosen)} public described repositories across {len(chosen)} namespaces')

if __name__=='__main__':
    main()
