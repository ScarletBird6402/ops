#!/usr/bin/env python3
"""링크 부채 감사 — 게시 HTML이 링크하지만 아직 미생성인 문서를 전수 추출.
사용: swe-notes 리포 루트에서  python link_debt_audit.py
출력: 미생성 타깃별 [빈도 / 어느 게시 문서가 링크하는지] 빈도순 정렬.
"""
import re, html
from pathlib import Path
from collections import defaultdict

# 게시본 = 리포에 실존하는 HTML (index 제외)
published = {}
for f in Path('.').rglob('*.html'):
    if f.name == 'index.html': continue
    m = re.match(r'([A-Z]+\d+) ', f.name)
    if m: published[m.group(1)] = f

debt = defaultdict(set)   # 미생성 코드 → 링크한 게시 문서들
titles = {}               # 미생성 코드 → 링크에 쓰인 제목(파일명 기준)

for code, f in sorted(published.items()):
    t = f.read_text(encoding='utf-8')
    for href in set(re.findall(r'href="([^"]+\.html)"', t)):
        name = html.unescape(href).split('/')[-1]
        mm = re.match(r'([A-Z]+\d+) (.+)\.html$', name)
        if not mm: continue
        target = mm.group(1)
        if target not in published:
            debt[target].add(code)
            titles[target] = mm.group(2)

print(f"게시 {len(published)}종 스캔 — 링크 부채 {len(debt)}건\n")
print(f"{'코드':<6}{'빈도':<4} 링크 출처 → 제목")
for target, srcs in sorted(debt.items(), key=lambda x: (-len(x[1]), x[0])):
    print(f"{target:<6}{len(srcs):<4} {','.join(sorted(srcs)):<24} → {titles[target]}")
