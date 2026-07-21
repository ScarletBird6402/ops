# ops — 운영 레포 (영구 비공개)

전 프로젝트 save-state의 **단일 정본** + 프로젝트 간 공유 상태 버스.
쓰기 = 사람 / Claude Code. 읽기 = claude.ai GitHub 통합(프로젝트 지식에 **폴더 선택 연동**).

> ⚠ **영구 비공개. 공개 전환 금지.** (설계 §4 / 핸드오프 §0)
> 공개 산출물 레포(swe-notes · ai-engineering-notes · algorithm-notes)에 운영 문서가 발견되면
> 게시-검증 에이전트가 FAIL 처리한다. 티어를 섞지 말 것.

## 폴더 구조 (ops_레포_설계 §1 / ops_파일배치_가이드)

| 폴더 | 들어가는 것 | 민감도 |
|---|---|---|
| `status/` | ★공유 표면: 프로젝트별 현황 요약(범공유 수준). 표준 양식으로 새로 작성 | 범공유 |
| `control/` | 컨트롤룸 전용: 핸드오프 v3(정본)·개설킷·레포 설계·배치 가이드 | 전략 |
| `career/` | 커리어 전용: 이직 전략 상세·회사별 분석. `transfers/` 아카이브 | **최상** |
| `swe/` | SWE 운영: 마스터플랜 본부판·운영문서·복습트랙. `briefs/`·`transfers/` | 본부 |
| `ai/` | AI 운영: 온보딩 패키지·생성 프롬프트·커리큘럼 요청서 | 운영 |
| `algo/` `lang/` | 알고리즘·어학 방 운영노트 | 운영 |
| `health/` `bike/` `misc/` | 각 방 운영노트 (보관 전용, claude.ai 미연동) | 보관 |
| `logs/` | Claude Code 세션 로그 (자동 커밋 대상) | 운영 |
| `kit/` | claude-work 킷 백업 (CLAUDE.md·agents) + 환경 문서 | 백업 |

## 연동 매트릭스 (claude.ai 프로젝트 지식 ← ops 폴더)

| claude.ai 프로젝트 | 연동 폴더 |
|---|---|
| SWE | `status/` + `swe/` |
| AI | `status/` + `ai/` |
| 알고리즘 | `status/` |
| 커리어 | `status/` + `career/` + `control/` (전체 관제) |
| 어학 | `status/` |
| 건강·운동 / 바이크 / 기타 | 미연동 |

- **원칙: `status/`만 범공유, 민감 상세는 소관 프로젝트 폴더에만.** career/·control/은 커리어 전용 불변.
- **`status/`에 health.md는 두지 않는다** — 건강 정보는 건강 방에만. career.md는 요약판만.
- Claude GitHub App 권한은 이 ops 단일 레포에만 부여.

## status/{프로젝트}.md 표준 양식 (설계 §3)
```
# {프로젝트} 현황
- 갱신: YYYY-MM-DD (갱신 주체)
- 단계: (한 줄)
- 최근 완료: (불릿 2~4)
- 진행 중 / 다음: (불릿 2~4)
- 타 프로젝트 전달사항: (있을 때만 — 프로젝트 간 통신 채널)
```
"타 프로젝트 전달사항"이 방 간 메시지 버스다.

## 현재 배치 상태 (2026-07-21 반입)

Downloads에서 확보한 문서를 가이드 배치 맵대로 넣었다. 원본이 없는 것은 각 폴더 `.gitkeep`에
"배치 예정" 목록으로 남겨 두었다 — 원본 확보 시 그 자리에 넣고 .gitkeep은 지운다.

- **control/**: 핸드오프 v3·개설킷·레포 설계·배치 가이드 (4종)
- **status/**: swe·ai·algo·career(요약)·lang (5종, 표준 양식으로 새로 작성 — 각 방이 정본으로 갱신)
- **career/**: 커리어현황.md
- **swe/**: 실무역량_운영문서·복습트랙·SWE미니프로젝트방 운영노트·학습자료_생성프롬프트 / `briefs/` 07-11·14·16·17 / `transfers/` 마스터방전달 2종·미니PJ방전달 1종
- **ai/**: AI_curriculum_request·AI학습자료_생성프롬프트 (+ ROADMAP.md·ai-engineering-notes_push.zip 임시 파킹 — 실은 공개 레포 반영분, ops 소관 아님)
- **kit/**: CLAUDE.md·agents 4종 + 에이전트시스템_구축요구사항_2026-07-19

### 보류·주의
- **실무역량_커리큘럼_마스터플랜 v2 보류**: Downloads본은 v2(A~V 21카테고리)로, 현재 공개 CURRICULUM(A~Z 26)·핸드오프 v3.1보다 구버전. 본부 정본은 **v3**여야 하므로 배치하지 않음 — v3 확보 시 swe/에.
- **ai/의 ROADMAP·push.zip**은 공개 ai-engineering-notes 반영분을 "일단" 여기 둔 것. 공개 레포 반영은 별도 작업.

## 킷 백업·복원

작업 루트 `claude-work/`의 `CLAUDE.md`·`.claude/agents/`는 어느 레포에도 속하지 않는다(구조적 차단).
`kit/`가 유일한 백업. 원본 수정 시 `kit/`도 수동 동기화.

### 복원 절차 (새 PC)
1. 작업 루트 폴더 생성 후 각 레포 클론
2. `kit/CLAUDE.md` → 작업 루트에 복사
3. `kit/agents/*.md` → 작업 루트 `.claude/agents/`에 복사
