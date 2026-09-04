#!/usr/bin/env python3
"""학습자료 HTML 검증 게이트 (Claude Code 파일럿용)
사용: python tools/verify_material.py "output/I13 의도를 드러내는 네이밍.html"
전 항목 PASS여야 검수 대기 자격. 정본: canon/실무역량_커리큘럼_마스터플랜_v3.md
"""
import re, html, sys, html
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parent.parent
PLAN = ROOT.parent / 'ops' / 'swe' / '실무역량_커리큘럼_마스터플랜_v3.md'  # canon 폐지 — ops 정본 직접 참조(2026-07-21 컨트롤룸)

VOID = {'br','hr','img','meta','link','input','area','base','col','embed','source','track','wbr'}
SENSITIVE = r'이직|커리어|방산|KAI|한화|\bLIG\b|면접|자소서|승진|JD|사내|본부|브리프'  # 컨트롤룸 4-2: 단순형 채택

def canon_titles():
    t = PLAN.read_text(encoding='utf-8')
    d = {}
    for m in re.finditer(r'^\| ([A-Z]+\d+) \| ([^|]+) \|', t, re.M):
        title = re.sub(r'\s*·?\s*\*\*[^*]*\*\*', '', m.group(2)).strip(' ·')
        d[m.group(1)] = title
    return d

def fname_of(code, title):
    s = re.sub(r'\s*\([^)]*\)', '', title).replace('/', '·').replace('  ', ' ').strip()
    return f"{code} {s}.html"

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in VOID: self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.stack and self.stack[-1] == tag: self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"미닫힘 <{self.stack.pop()}>")
            if self.stack: self.stack.pop()
        else: self.errors.append(f"고아 종료 </{tag}>")

def main(path):
    p = Path(path)
    results, ok = [], True
    def check(name, passed, detail=""):
        nonlocal ok
        results.append(f"  [{'PASS' if passed else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
        if not passed: ok = False

    if not p.exists():
        print(f"파일 없음: {p}"); sys.exit(2)
    t = p.read_text(encoding='utf-8')
    titles = canon_titles()

    # 1. 파일명 규칙
    m = re.match(r'([A-Z]+\d+) ', p.name)
    code = m.group(1) if m else None
    if code and code in titles:
        want = fname_of(code, titles[code])
        check("파일명 = 정본 제목(괄호 제거·슬래시 치환)", p.name == want,
              "" if p.name == want else f"기대: {want}")
    else:
        check("파일명 코드 식별", False, f"코드 '{code}' 정본 부재")

    # 2. 태그 균형
    tc = TagChecker(); tc.feed(t)
    residual = [x for x in tc.stack if x != 'html']
    check("HTML 태그 개폐 균형", not tc.errors and not residual,
          "; ".join(tc.errors[:3]) + (f" 미닫힘 잔여 {residual[:3]}" if residual else ""))

    # 3. 골격 섹션 순서
    h2s = [re.sub(r'<[^>]+>', '', h).strip() for h in re.findall(r'<h2[^>]*>(.*?)</h2>', t, re.S)]
    needed = ['한눈에 보는 결론', '흔히 헷갈리는 지점', '언어별 대조', '함께 알면 좋은 것', '한 장 요약', '관련 문서']  # 순서는 게시본 6종 실측(헷갈 절 = ★대조 직전) — 컨트롤룸 3-1 취지 유지, 위치만 교정
    idx = []
    for n in needed:
        pos = next((i for i, h in enumerate(h2s) if n in h), -1)
        idx.append(pos)
    check("표준 골격 섹션 존재·순서", all(i >= 0 for i in idx) and idx == sorted(idx),
          f"h2 발견: {[n for n, i in zip(needed, idx) if i < 0]} 누락" if not all(i >= 0 for i in idx) else "")

    # 4. 관련 문서 링크 전량 정본 대조
    bad_links = []
    for href in set(re.findall(r'href="([^"]+\.html)"', t)):
        h = html.unescape(href).split('/')[-1]
        mm = re.match(r'([A-Z]+\d+) ', h)
        if not mm: bad_links.append(f"{h}(코드 없음)"); continue
        c = mm.group(1)
        if c not in titles: bad_links.append(f"{h}(정본 부재)"); continue
        if h != fname_of(c, titles[c]): bad_links.append(f"{h} ≠ {fname_of(c, titles[c])}")
    check("내부 링크 정본 정합", not bad_links, "; ".join(bad_links[:3]))

    # 5. 4언어 심화 (소제목 + 코드 블록) — 2026-07-25 개정: Java·JS/TS 심화 승격
    has_cpp = bool(re.search(r'<h[34][^>]*>[^<]*C\+\+', t))
    has_py = bool(re.search(r'<h[34][^>]*>[^<]*Python', t))
    has_java = bool(re.search(r'<h[34][^>]*>[^<]*\bJava\b(?!\s*Script)', t))
    has_js = bool(re.search(r'<h[34][^>]*>[^<]*(JS|JavaScript|TypeScript)', t))
    ncode = len(re.findall(r'<pre', t))
    check("4언어 별도 심화 소제목(Java·JS/TS·Python·C++)", all([has_cpp, has_py, has_java, has_js]),
          f"Java:{has_java} JS/TS:{has_js} Python:{has_py} C++:{has_cpp}")
    check("코드 예제 블록(pre) 4개 이상", ncode >= 4, f"{ncode}개")

    # 4.5 링크 경로 형식 (2026-09-04 표준: ../{코드문자 카테고리명}/{파일명}) — 폴더 구조에서 동작하는 유일 형식
    hrefs = re.findall(r'href="([^"]+\.html)"', t)
    bad_path = [h for h in hrefs if not re.match(r'\.\./[A-Z]+ [^/]+/(?:AI-)?[A-Z]+\d+ ', html.unescape(h))]
    check("링크 경로 형식(../카테고리 폴더/파일명)", not bad_path, bad_path[0][:50] if bad_path else "")

    # 4.6 ★ 헤더 번호 형식 (규격: '★ N. 언어별 대조' + 하위 'N.1 Java —')
    star_ok = bool(re.search(r'<h2[^>]*>\s*★\s*\d+\.\s*언어별 대조', t)) and bool(re.search(r'<h3[^>]*>\s*\d+\.\d+\s', t))
    check("★ 절·하위 소제목 번호 형식", star_ok)

    # 5.5 다이어그램 정렬 (2026-08-03: flow/pre 가운데 정렬 금지)
    css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', t, re.S))
    bad_align = re.findall(r'((?:\.flow|pre)[^{}]*\{[^}]*text-align:\s*center[^}]*\})', css)
    check("다이어그램 블록 왼쪽 정렬(pre/.flow center 금지)", not bad_align,
          bad_align[0][:60] if bad_align else "")

    # 6. 민감어·내부 용어 (공개 게이트)
    hits = [l.strip()[:60] for l in t.split('\n') if re.search(SENSITIVE, l)]
    check("민감어·내부 용어 0건", not hits, "; ".join(hits[:2]))

    print(f"=== 검증: {p.name} ===")
    print('\n'.join(results))
    print("결과:", "ALL PASS — 검수 대기 자격" if ok else "FAIL — 수정 후 재검증")
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    main(sys.argv[1])
