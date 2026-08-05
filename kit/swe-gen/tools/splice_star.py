#!/usr/bin/env python3
"""★언어별 대조 절 치환 도구 (개정 배치 C용)
사용: python tools/splice_star.py "<원본.html>" "<조각.html>" "<출력.html>"
원본에서 <h2>★ ...</h2> 절(다음 <h2> 직전까지)을 조각으로 교체해 출력에 저장.
★절 밖 바이트 보존을 구조적으로 보장하고, 보존 검증 결과를 출력한다.
"""
import re, sys
from pathlib import Path

def main(orig_path, frag_path, out_path):
    orig = Path(orig_path).read_text(encoding='utf-8')
    frag = Path(frag_path).read_text(encoding='utf-8')

    m_start = re.search(r'(?m)^[ \t]*<h2[^>]*>\s*★', orig)
    if not m_start:
        print("FAIL: 원본에서 ★ h2를 찾지 못함"); sys.exit(1)
    m_next = re.search(r'(?m)^[ \t]*<h2', orig[m_start.end():])
    if not m_next:
        print("FAIL: ★절 다음 h2를 찾지 못함"); sys.exit(1)
    start = m_start.start()
    end = m_start.end() + m_next.start()

    # 조각 선두 h2 제목이 원본과 동일한지 확인
    orig_h2 = re.search(r'<h2[^>]*>(.*?)</h2>', orig[start:end], re.S).group(1).strip()
    frag_h2_m = re.search(r'<h2[^>]*>(.*?)</h2>', frag, re.S)
    if not frag_h2_m:
        print("FAIL: 조각에 h2 없음"); sys.exit(1)
    frag_h2 = frag_h2_m.group(1).strip()
    if orig_h2 != frag_h2:
        print(f"FAIL: h2 제목 불일치\n  원본: {orig_h2!r}\n  조각: {frag_h2!r}"); sys.exit(1)

    if not frag.endswith('\n'):
        frag += '\n'
    result = orig[:start] + frag + orig[end:]
    Path(out_path).write_text(result, encoding='utf-8', newline='\n')

    # 보존 검증: ★절 밖 전위·후위 바이트 동일성
    ok_pre = result.startswith(orig[:start])
    ok_post = result.endswith(orig[end:])
    print(f"h2 일치: {orig_h2}")
    print(f"전위 보존: {'OK' if ok_pre else 'FAIL'} ({start}자) / 후위 보존: {'OK' if ok_post else 'FAIL'} ({len(orig)-end}자)")
    print(f"★절 크기: 구 {end-start}자 → 신 {len(frag)}자")
    sys.exit(0 if ok_pre and ok_post else 1)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(__doc__); sys.exit(2)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
