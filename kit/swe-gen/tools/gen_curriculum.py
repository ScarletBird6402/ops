#!/usr/bin/env python3
"""마스터플랜 v3 → swe-notes/CURRICULUM.md 생성 (gen_index.py와 같은 정본·블록 구조).
게시 상태(✅)는 하드코딩이 아니라 swe-notes에 실존하는 HTML 파일에서 코드를 추출해 판정한다.
사용: swe-gen에서  python tools/gen_curriculum.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT.parent / 'ops' / 'swe' / '실무역량_커리큘럼_마스터플랜_v3.md'
REPO = ROOT.parent / 'swe-notes'
OUT = REPO / 'CURRICULUM.md'

BLOCKS = [('클라이언트', 'AB'), ('서버 · 데이터', 'CDEFGH'), ('설계 · 품질 · 협업', 'IJKL'),
          ('운영 · 플랫폼', 'MNOPQR'), ('보안', 'STU'), ('CS · 통신', 'VWXYZ')]
NOTES = {  # 표 앞 안내문(기존 CURRICULUM.md 문구 유지)
    'X': '예약 카테고리 — 다른 카테고리의 계획 항목이 대부분 소진된 뒤 다룰 수도 있는 영역이며, 개시 여부는 정해져 있지 않습니다.',
    'Z': '설계 시나리오를 문서로 정리하고 실제 구현(swe-projects)으로 잇는 통합 카테고리입니다.',
}

plan = PLAN.read_text(encoding='utf-8')
cats = dict(re.findall(r'^## ([A-Z])\. (.+?) — \[', plan, re.M))
cats.setdefault('X', '임베디드 시스템(예약)')
items = {}
for m in re.finditer(r'^\| ([A-Z])(\d+) \| ([^|]+) \|', plan, re.M):
    items.setdefault(m.group(1), []).append((m.group(1) + m.group(2), m.group(3).strip()))
for k in items:
    items[k].sort(key=lambda x: int(x[0][1:]))
clean = lambda t: re.sub(r'\s*·?\s*\*\*[^*]*\*\*', '', t).strip(' ·')

published = set()
for f in REPO.rglob('*.html'):
    if f.name == 'index.html':
        continue
    mm = re.match(r'([A-Z]+\d+) ', f.name)
    if mm:
        published.add(mm.group(1))

lines = ['# CURRICULUM', '',
         '학습 노트의 전체 계획표입니다. 게시 완료 항목은 ✅, 나머지는 예정 목차입니다.',
         '코드 체계는 고정(재사용 없음)이라 파일명·링크가 안정적으로 유지됩니다.', '']
total = 0
for bname, letters in BLOCKS:
    lines += [f'## {bname}', '']
    for L in letters:
        lines.append(f'### {L}. {cats[L]}')
        if L in NOTES:
            lines.append(NOTES[L])
            if L == 'X':
                lines.append('')
                continue
            lines.append('')
        lines += ['| 코드 | 주제 | 상태 |', '|---|---|---|']
        for code, title in items.get(L, []):
            total += 1
            lines.append(f'| {code} | {clean(title)} | {"✅" if code in published else ""} |')
        lines.append('')

OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'생성: 카테고리 {len(cats)} / 항목 {total} / 게시 {len(published & {c for v in items.values() for c, _ in v})}')
orphan = published - {c for v in items.values() for c, _ in v}
print('정본에 없는 게시 파일 코드:', sorted(orphan) if orphan else '0건')
