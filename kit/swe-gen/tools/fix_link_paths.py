#!/usr/bin/env python3
"""문서 간 링크를 카테고리 폴더 상대 경로로 일괄 정정 (2026-09-04 표준)
표준: href="../{코드문자 카테고리명}/{코드 제목}.html"  — 같은 카테고리도 동일 형식(통일).
사용: swe-notes 리포 루트에서
  python fix_link_paths.py            # dry-run
  python fix_link_paths.py --apply
폴더명은 리포의 실제 폴더에서 추출(코드문자 → 폴더), 폴더가 없는 카테고리는 ops 정본의 '## X. 이름' 헤더로 보완.
앵커 표시 텍스트가 파일명과 동일하면 괄호 병기 제거형 파일명으로 함께 정리.
"""
import re, sys, html
from pathlib import Path
APPLY = '--apply' in sys.argv
PLAN = Path('../ops/swe/실무역량_커리큘럼_마스터플랜_v3.md')

folders = {}
for d in Path('.').iterdir():
    m = re.match(r'([A-Z]+) (.+)$', d.name)
    if d.is_dir() and m: folders[m.group(1)] = d.name
if PLAN.exists():
    for m in re.finditer(r'^## ([A-Z]+)\. ([^—\n]+?)\s*(?:—|$)', PLAN.read_text(encoding='utf-8'), re.M):
        folders.setdefault(m.group(1), f"{m.group(1)} {m.group(2).strip().replace('/', '·')}")
print(f"카테고리 폴더 매핑 {len(folders)}개: {sorted(folders)}\n")

fixed = unresolved = 0
for f in sorted(Path('.').rglob('*.html')):
    if f.name == 'index.html': continue
    t = f.read_text(encoding='utf-8'); orig = t
    def repl(m):
        global unresolved
        href = html.unescape(m.group(1)); fname = href.split('/')[-1]
        cm = re.match(r'([A-Z]+)\d+ ', fname)
        if not cm: return m.group(0)
        cat = cm.group(1)
        if cat not in folders:
            unresolved += 1; print(f"  [미해결] {f.name}: {href} (카테고리 {cat} 폴더 불명)"); return m.group(0)
        return f'href="../{folders[cat]}/{fname}"'
    t = re.sub(r'href="([^"]+\.html)"', repl, t)
    if t != orig:
        n = sum(1 for a, b in zip(re.findall(r'href="[^"]+"', orig), re.findall(r'href="[^"]+"', t)) if a != b)
        fixed += n; print(f"[{'FIX' if APPLY else 'DRY'}] {f} — {n}건")
        if APPLY: f.write_text(t, encoding='utf-8')
print(f"\n{'적용' if APPLY else '검출(미적용)'} {fixed}건 / 미해결 {unresolved}건", "" if APPLY else "→ 적용: --apply")
