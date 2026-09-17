#!/usr/bin/env python3
"""마스터플랜 v3 → index.html 생성 (2단 레이아웃).
게시 완료분은 하이퍼링크, 미생성분은 회색 텍스트. PUB 집합만 갱신하면 재생성 가능."""
import re, html as H

PLAN = '../ops/swe/실무역량_커리큘럼_마스터플랜_v3.md'  # swe-gen에서 실행 기준
OUT  = '../swe-notes/index.html'

# 게시 완료 문서 (갱신 지점) — 2026-08-01 실제 게시 파일 기준 재동기화
# ※ 3주차 12건(세션1 C21·O7·O8·C1·C6 / 세션2 M1~M4·C20 / 세션3 A2·I8)은 검수·이동 전 선반영 — 이동 전까지 링크 404
PUB = {'A12','A13','C10','C11','C17','C18','D2',
       'E1','E3','E4','E5','E18','E19','G1',
       'A14','I1','I4','I11','I13','J10','K5','K9',
       'O1','O2','O3','O5','P1','P3',
       'S1','S2','S3','S10','V1','V2','V3','W4','Z1',
       'C21','O7','O8','C1','C6',
       'M1','M2','M3','M4','C20','A2','I8',
       'J1','J5','J2','J14','J9','J3','J4','J7','J12','J6','J11','J13','J15','J16','J18',  # 2026-09-03 유닛 테스트 팩 15건
       'K3','L1','L3','M12','I14','I16','D12','C16','C15','K13','C4','D1','B2','P4','Q3','I2','E17','E24','I24','I27',
       'C8'}  # 2026-09-18 C8(사용자 직접 생성분)

# 최근 추가 (코드, 제목, 날짜) — 최신순, 최대 10
RECENT = [('C8','디스패처 패턴과 method 분기','2026-09-18'),
          ('I27','정규화 정본과 표현형 — 경계에서 한 번','2026-09-16'),
          ('I24','실패 채널의 분리와 원인 보존','2026-09-16'),
          ('E24','배치화 — N+1 제거와 그 대가','2026-09-16'),
          ('E17','계층형 트리 탐색의 조회 단위 설계','2026-09-16'),
          ('I2','DRY 원칙과 범위','2026-09-16'),
          ('Q3','캐싱 전략','2026-09-16'),
          ('P4','분산 추적','2026-09-16'),
          ('B2','브라우저 이벤트 루프','2026-09-16'),
          ('D1','HTTP 심화','2026-09-16'),
          ('C4','서버 세션 관리','2026-09-16'),
          ('K13','독자 기준 산출물 설계','2026-09-16'),
          ('C15','트랜잭션 관리와 전파','2026-09-16'),
          ('C16','예외 처리 전략','2026-09-16'),
          ('D12','응답 계약의 이형 반환과 타입 가드','2026-09-16'),
          ('I16','오도성 시그니처와 계약 정직성','2026-09-16'),
          ('I14','암묵적 결합과 이중 목적 데이터','2026-09-16'),
          ('M12','빌드 재현성과 환경 독립성','2026-09-16'),
          ('L3','커밋 위생','2026-09-16'),
          ('L1','Git 상태 모델과 선별 스테이징','2026-09-16'),
          ('K3','코드 컨벤션 조사 방법론','2026-09-16'),
          ('J18','다층 방어의 층별 검증 — 무증상 퇴화','2026-09-03'),
          ('J16','조합적 결함과 pairwise 테스트','2026-09-03'),
          ('J15','미실행 경로와 활성화 리스크','2026-09-03'),
          ('J13','테스트 러너의 수집 규칙과 선택 실행','2026-09-03'),
          ('J11','테스트 결정성과 환경 의존 함정','2026-09-03'),
          ('J6','추상 클래스·인터페이스 테스트 전략','2026-09-03'),
          ('J12','목킹 주입 2패러다임 — 객체 교체 vs 이름 패치','2026-09-03'),
          ('J7','Mock 생명주기 관리','2026-09-03'),
          ('J4','Mockito 인자 검증 — Matcher와 Captor','2026-09-03'),
          ('J3','Mockito 기본 3단계','2026-09-03'),
          ('J9','테스트 커버리지의 의미와 함정','2026-09-03'),
          ('J14','테스트 케이스 설계 관점','2026-09-03'),
          ('J2','테스트 피라미드','2026-09-03'),
          ('J5','상태 검증 vs 행위 검증','2026-09-03'),
          ('J1','테스트 더블과 단위 테스트 격리','2026-09-03'),
          ('I8','재활용 원칙 — 원천 값','2026-08-02'),
          ('A2','Vue 반응성 시스템 원리','2026-08-02'),
          ('C20','날짜·시간·타임존 처리','2026-08-02'),
          ('M4','정적 자산 캐싱과 무효화','2026-08-02'),
          ('M3','빌드 번들 검사 방법론','2026-08-02'),
          ('M2','빌드 방식 vs dev 서버','2026-08-02'),
          ('M1','패키지 의존성 3층 구조','2026-08-02'),
          ('C21','원격·리플렉션 경계의 메서드 오버로딩','2026-08-01'),
          ('O7','에러 재래핑과 진단 경로','2026-08-01'),
          ('O8','설정의 배포 원천 분리와 로드 역추적','2026-08-01'),
          ('C1','서버사이드 렌더링 vs 클라이언트 렌더링','2026-08-01'),
          ('C6','SSR·SPA 통합','2026-08-01'),
          ('A14','다중 키 정렬과 방향 독립 제어','2026-08-01'),
          ('I13','의도를 드러내는 네이밍','2026-08-01'),
          ('A12','파생 상태 계산 파이프라인','2026-07-28'),
          ('A13','센티널 레코드와 계층 표현','2026-07-28'),
          ('E18','ORM 삭제·벌크 DML과 세션 정합','2026-07-28'),
          ('E19','세션 수명주기와 트랜잭션 확정 지점','2026-07-28'),
          ('G1','스레드 안전성 기초','2026-07-28'),
          ('J10','테스트 대상 선정 — 무엇을 테스트하지 않을지','2026-07-28'),
          ('K9','문제 해결 방법론','2026-07-28'),
          ('O1','환경변수 수명주기와 12-Factor','2026-07-28'),
          ('O2','정적 파일 서빙 모델','2026-07-28')]

BLOCKS = [('클라이언트','AB'), ('서버 · 데이터','CDEFGH'), ('설계 · 품질 · 협업','IJKL'),
          ('운영 · 플랫폼','MNOPQR'), ('보안','STU'), ('CS · 통신','VWXYZ')]

plan = open(PLAN, encoding='utf-8').read()
cats = dict(re.findall(r'^## ([A-Z])\. (.+?) — \[', plan, re.M))
cats.setdefault('X', '임베디드 시스템(예약)')

items = {}
for m in re.finditer(r'^\| ([A-Z])(\d+) \| ([^|]+) \|', plan, re.M):
    items.setdefault(m.group(1), []).append((m.group(1)+m.group(2), m.group(3).strip()))
for k in items: items[k].sort(key=lambda x: int(x[0][1:]))

clean  = lambda t: re.sub(r'\s*·?\s*\*\*[^*]*\*\*', '', t).strip(' ·')   # 표기 마커 제거
strip_p= lambda s: re.sub(r'\s*\([^)]*\)', '', s).replace('/', '·').replace('  ',' ').strip()  # 파일명: 괄호 병기 제거 + 슬래시→가운뎃점
folder = lambda L: f"{L} {cats[L].replace(chr(47), chr(183))}"            # 폴더: 카테고리명(슬래시→가운뎃점)

total = sum(len(v) for v in items.values())
nlink = 0
parts = []
for bname, letters in BLOCKS:
    parts.append(f'<h2>{bname}</h2>')
    for L in letters:
        parts.append(f'<section class="cat"><h3><span class="code">{L}</span>{H.escape(cats[L])}</h3>')
        if L == 'X':
            parts.append('<p class="rsv">예약 — 개시 여부 미정</p></section>'); continue
        rows = []
        for code, title in items.get(L, []):
            ct = clean(title)
            if code in PUB:
                href = f"{folder(L)}/{code} {strip_p(ct)}.html"
                cell = f'<a href="{H.escape(href)}">{H.escape(ct)}</a>'
                nlink += 1
            else:
                cell = f'<span class="todo">{H.escape(ct)}</span>'
            rows.append(f'<tr><td class="c">{code}</td><td>{cell}</td></tr>')
        parts.append('<table>' + ''.join(rows) + '</table></section>')
sections = '\n'.join(parts)

recent_html = '\n'.join(
    f'  <li><a href="{H.escape(folder(c[0] if not c[1:].isdigit() else c[0])+"/"+c+" "+t+".html")}">'
    f'<span class="code">{c}</span>{H.escape(t)}</a><span class="date">{d}</span></li>'
    for c, t, d in RECENT[:10])

html = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>실무 학습 노트</title>
<style>
  :root {{
    --bg:#fff; --fg:#24292f; --border:#d0d7de;
    --code-bg:#f6f8fa; --accent:#0969da; --muted:#57606a;
  }}
  * {{ box-sizing:border-box; }}
  body {{
    background:var(--bg); color:var(--fg);
    font-family:-apple-system,"Segoe UI","맑은 고딕","Malgun Gothic",sans-serif;
    line-height:1.6; margin:0; padding:36px 20px;
  }}
  main {{ max-width:1100px; margin:0 auto; }}
  h1 {{ font-size:1.85rem; border-bottom:2px solid var(--border); padding-bottom:.35em; margin:0 0 .4em; }}
  .intro {{ margin:.3em 0 0; }}
  .meta {{ color:var(--muted); font-size:.88rem; margin:.5em 0 0; }}
  a {{ color:var(--accent); text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}
  .code {{ font-family:Consolas,"D2Coding",monospace; color:var(--muted); font-size:.85em; margin-right:.45em; }}

  /* 최근 추가 — 2단 */
  .recent {{ columns:2; column-gap:32px; list-style:none; padding:0; margin:.6em 0 0; }}
  .recent li {{ break-inside:avoid; margin:.2em 0; font-size:.94rem; }}
  .date {{ color:var(--muted); font-size:.82em; margin-left:.4em; }}

  /* 목차 — 논문형 2단, 블록 헤더는 양단 걸침 */
  .toc {{ columns:2; column-gap:34px; margin-top:1.2em; }}
  .toc h2 {{
    column-span:all; -webkit-column-span:all;
    font-size:1.28rem; margin:1.6em 0 .5em;
    border-bottom:1px solid var(--border); padding-bottom:.28em;
  }}
  .toc h2:first-of-type {{ margin-top:.6em; }}
  .cat {{ break-inside:avoid; -webkit-column-break-inside:avoid; page-break-inside:avoid; margin:0 0 1.1em; }}
  .cat h3 {{ font-size:.98rem; margin:0 0 .35em; }}
  .cat table {{ border-collapse:collapse; width:100%; }}
  .cat td {{ border:1px solid var(--border); padding:3px 8px; font-size:.88rem; line-height:1.45; }}
  .cat td.c {{
    width:3.1em; text-align:center; background:var(--code-bg);
    font-family:Consolas,"D2Coding",monospace; font-size:.82rem; color:var(--muted);
  }}
  .cat tr:nth-child(even) td {{ background:#fafbfc; }}
  .cat tr:nth-child(even) td.c {{ background:var(--code-bg); }}
  .todo {{ color:var(--muted); }}
  .rsv {{ color:var(--muted); font-size:.86rem; margin:0; padding:4px 8px;
          border:1px dashed var(--border); border-radius:5px; }}

  footer {{ margin-top:3em; padding-top:1em; border-top:1px solid var(--border);
            color:var(--muted); font-size:.86rem; }}
  @media (max-width:760px) {{ .toc, .recent {{ columns:1; }} }}
</style>
</head>
<body>
<main>

<h1>실무 학습 노트</h1>
<p class="intro">웹 프론트엔드 · 백엔드 · 데이터베이스 · 인프라 · 보안 · CS를 정리합니다.
업무 중 학습한 내용을 기반으로 계속 추가됩니다.</p>
<p class="meta">모든 문서는 언어 중립으로 원리를 설명하고, Java · JS/TS · Python · C++에서 같은 개념이
어떻게 나타나는지 대조합니다. <strong>링크 = 게시된 문서</strong> · 회색 = 예정 목차
(게시 {len(PUB)} / 전체 {total}).</p>

<h2>최근 추가</h2>
<ul class="recent">
{recent_html}
</ul>

<div class="toc">
{sections}
</div>

<p class="meta">전체 학습 계획은 <a href="https://github.com/ScarletBird6402/swe-notes/blob/main/CURRICULUM.md">CURRICULUM</a> 참고 — 계속 확장 중입니다.</p>

<footer>
  학습 노트이며 계속 추가·수정됩니다.<br>
  문서는 Claude(Anthropic)를 활용해 생성합니다. 주제 선정·구성·검토는 직접 합니다.
</footer>

</main>
</body>
</html>
'''
open(OUT, 'w', encoding='utf-8').write(html)
print(f"생성: 카테고리 {len(cats)} / 항목 {total} / 링크 {nlink}")

# 검증
valid = {f"{k} {v}" for k, v in cats.items()}
bad = [f for f in set(re.findall(r'href="([A-Z][^/"]*)/', html)) if f not in valid]
print("정본 불일치 폴더:", bad if bad else "0건")
print("항목 행:", html.count('<tr>'), "/ 링크:", html.count('<td><a href'), "/ 미생성:", html.count('<span class="todo"'))
