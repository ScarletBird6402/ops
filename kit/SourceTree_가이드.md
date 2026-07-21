# SourceTree로 GitHub 레포지토리 올리기 — 실전 가이드

> 목표: 지식베이스 레포 + AI(SELD) 레포를 SourceTree로 생성·커밋·게시. Git 개념보다 **손 순서** 위주.
> 설치 마법사 화면은 버전에 따라 순서·문구가 조금씩 다를 수 있다. 화면이 달라도 "이 단계가 왜 있는지"를 알면 판단할 수 있도록 설명을 함께 둔다.

---

## 0-0. 설치 마법사 단계별 안내

1. **License(라이선스 동의)**: 동의하고 다음.
2. **Registration (Atlassian 계정 / Bitbucket)**: SourceTree는 Atlassian(Bitbucket 운영사) 제품이라 나오는 화면. **Bitbucket은 GitHub의 경쟁 서비스**이며 지금 쓸 계획이 없으므로 **건너뛰기(Skip / 나중에)** 를 찾아 누른다. 계정 생성을 강제하는 것처럼 보여도 대부분 하단·구석에 작게 건너뛰기 링크가 있다.
3. **Mercurial 체크박스**: Mercurial(머큐리얼)은 Git과는 다른 별개의 버전관리 시스템(과거 Git의 경쟁 기술, 현재는 거의 안 씀). **체크 해제 권장** — GitHub는 Git만 쓰므로, 켜면 불필요한 구성요소만 추가 설치된다.
4. **Git 설치 감지**: 시스템에 Git이 있으면 그대로 사용, 없으면 SourceTree가 **내장 Git**을 자동 설치한다. 그대로 진행하면 되고 별도로 Git을 먼저 설치할 필요 없음.
5. **기존 레포지토리 검색/추가**: 처음이라 아무것도 없으므로 **건너뛰기**(나중에 §2~3에서 직접 클론).
6. **Preferences(최초 설정)**:
   - SSH 키 생성: 처음엔 **건너뛰어도 무방**(HTTPS + 계정 연동만으로 충분, 나중에 추가 가능)
   - Diff/Merge 도구: 기본값 유지(내장 도구로 충분)
7. **계정 연결 화면**: 여기서 **GitHub**를 선택 → 아래 §0-A·1로 이어짐.

---

## 0-A. 준비물 체크
- GitHub 계정 (없으면 github.com에서 생성)
- SourceTree 설치 파일 (공식: https://www.sourcetreeapp.com/)
- 로컬에 각 레포용 폴더 (예: `C:\projects\knowledge-base`, `C:\projects\seld`)

---

## 0-B. 개인정보 보호 설정 (첫 커밋 전 필수)

> ⚠️ **반드시 1번(레포 생성)보다 먼저, 최소한 첫 커밋 전에 끝낼 것.** 커밋에는 작성자 이메일이 그대로 기록되며, 이미 커밋한 뒤 바꾸면 과거 커밋에는 소급 적용되지 않는다.

구글 계정으로 가입한 경우 특히 중요한 두 가지.

### 이메일 비공개 설정
1. GitHub 웹 → 우측 상단 프로필 → `Settings` → 좌측 `Emails`
2. **"Keep my email addresses private"** 체크
3. 그 아래 표시되는 대체 주소를 확인: `{아이디}@users.noreply.github.com`

### SourceTree(로컬 Git)의 커밋 이메일을 noreply 주소로 설정
1. SourceTree → `Tools` → `Options` → `Git` 탭
2. `Name`: 원하는 표시 이름 입력
3. `Email`: 위에서 확인한 `...@users.noreply.github.com` 주소 입력 (개인 Gmail 주소 아님)
4. 저장

> 이렇게 하지 않으면 공개 레포의 모든 커밋에 실제 Gmail 주소가 영구적으로 노출된다.

### 프로필 표시 이름·사진 점검
- `Settings` → `Public profile`에서 표시 이름(Name)과 프로필 사진 확인
- 구글 가입 시 개인 사진이 자동으로 들어와 있을 수 있으니, 커리어용으로 적절한 것으로 교체

---

## 1. SourceTree 설치 및 GitHub 연결

1. SourceTree 설치 후 첫 실행 시 **계정 연결** 화면이 뜬다.
2. `Add Account` → **GitHub** 선택 → 브라우저로 로그인해 인증(OAuth). 완료되면 SourceTree가 GitHub 계정과 연결된다.
3. 이후 SourceTree에서 `새로 만들기(New)` 시 원격 저장소를 GitHub에 바로 생성할 수 있다.

> ℹ️ 계정 연결이 안 되면: SourceTree 메뉴 → `Tools` → `Options` → `Authentication` 탭에서 GitHub 계정 추가.

---

## 2. GitHub에서 레포지토리 먼저 만들기 (권장 순서)

SourceTree에서도 만들 수 있지만, **GitHub 웹사이트에서 먼저 만드는 게 초보자에게 더 안전**하다(설정을 눈으로 보며 할 수 있음).

1. github.com 로그인 → 우측 상단 `+` → `New repository`
2. 입력:
   - Repository name: 예) `knowledge-base` (지식베이스), `seld` (AI 레포)
   - Description: 짧은 설명 (선택)
   - **Public** 선택 (포트폴리오 목적이므로)
   - `Add a README file` 체크 **하지 않음** (이미 우리가 만든 README를 올릴 것이므로 — 체크하면 나중에 충돌 처리가 필요해짐)
3. `Create repository` 클릭
4. 생성된 레포 페이지에서 초록색 `Code` 버튼 → **HTTPS 주소 복사** (예: `https://github.com/계정명/knowledge-base.git`)

> 지식베이스·AI 레포 둘 다 이 과정을 반복해 2개 만든다.

---

## 3. SourceTree로 로컬에 클론(Clone)

"클론"은 방금 만든 빈 GitHub 레포를 내 컴퓨터로 복사해오는 것이다.

1. SourceTree 실행 → 좌측 상단 `Clone` 버튼
2. `Source Path / URL`에 2단계에서 복사한 URL 붙여넣기
3. `Destination Path`: 로컬에 저장할 폴더 지정 (예: `C:\projects\knowledge-base`)
4. `Clone` 클릭 → 빈 폴더가 로컬에 생기고 SourceTree가 그 폴더를 "레포지토리"로 인식한다.

> AI 레포도 동일하게 별도 폴더로 클론 (예: `C:\projects\seld`).

---

## 4. 파일 넣고 구조 잡기

1. 탐색기(파일 탐색기)로 클론한 폴더를 열고, 앞서 준비한 파일들을 넣는다.

**지식베이스 레포 (`knowledge-base` 폴더 안)**
```
knowledge-base/
├─ README.md              ← "지식베이스_레포_README.md" 내용을 이 이름으로 저장
├─ index.html              ← 랜딩 페이지
├─ A/  B/  C/  ...  Q/     ← 카테고리 폴더 (문서 게시하며 하나씩 생성)
```

**AI(SELD) 레포 (`seld` 폴더 안)**
```
seld/
├─ README.md               ← "AI레포_README.md" 내용을 이 이름으로 저장
├─ ROADMAP.md               ← "AI레포_ROADMAP.md"
├─ .gitignore               ← "AI레포_gitignore.txt" 내용을 이 이름(점 포함)으로 저장
├─ requirements.txt         ← (아직 없으면 빈 파일이나 추후 채울 것)
├─ docs/
│   └─ report-template.md   ← "AI레포_report-template.md"
├─ 01-warmup-sed/           ← 빈 폴더 (내용 생기면 채움)
├─ 02-baseline/
└─ 03-improvement/
```

> ⚠️ **파일명 주의**: `README.md`, `.gitignore`는 정확히 이 이름(대소문자 포함)이어야 GitHub가 특별하게 인식한다(README는 레포 첫 화면에 자동 표시, .gitignore는 Git이 자동으로 읽음).
> ⚠️ **빈 폴더 문제**: Git은 빈 폴더를 추적하지 못한다. `01-warmup-sed` 등이 비어 있으면 커밋에 안 잡힌다. 안에 `.gitkeep`이라는 빈 파일을 하나 넣어두면 폴더가 유지된다(내용이 생기면 지워도 됨).

---

## 5. SourceTree로 커밋(Commit)

"커밋"은 변경사항을 기록으로 남기는 것 (아직 GitHub에 안 올라감, 로컬에만 저장).

1. SourceTree에서 해당 레포 열기 → 왼쪽 메뉴 `File Status` (또는 자동으로 뜸)
2. 화면 하단/중앙에 방금 추가한 파일들이 **Unstaged files**로 보인다.
3. 전체 선택 후 `Stage All` (또는 파일마다 체크) → 파일들이 **Staged files**로 이동
4. 하단 커밋 메시지 입력창에 메시지 작성. 예:
   - `Initial commit: README, index, structure`
   - (커밋 위생: 한 커밋 = 한 의도가 드러나는 메시지)
5. `Commit` 버튼 클릭

---

## 6. SourceTree로 푸시(Push) — 실제로 GitHub에 올리기

"푸시"는 로컬 커밋을 GitHub(원격)로 업로드하는 것.

1. 커밋 후 상단 `Push` 버튼 클릭
2. 브랜치 확인(보통 `main`) → `Push` 클릭
3. 완료되면 GitHub 레포 페이지를 새로고침 → 파일들이 보인다.

> 이후 작업 흐름은 반복: 파일 추가/수정 → SourceTree에서 `Stage` → `Commit` → `Push`.

---

## 7. GitHub Pages 활성화 (지식베이스 랜딩 공개)

지식베이스 레포의 `index.html`을 실제 웹사이트로 보이게 하는 단계.

1. GitHub에서 `knowledge-base` 레포 페이지 → 상단 `Settings` 탭
2. 왼쪽 메뉴 `Pages` 클릭
3. `Build and deployment` → `Source`: **Deploy from a branch** 선택
4. `Branch`: `main` / 폴더: `/ (root)` 선택 → `Save`
5. 몇 분 후 상단에 사이트 주소가 표시됨: `https://{계정}.github.io/knowledge-base/`
6. 그 주소로 접속해 `index.html`이 뜨는지 확인.

> AI(SELD) 레포는 코드·문서 저장소 목적이라 Pages 활성화는 선택사항(원하면 동일하게 켤 수 있음).

---

## 8. 프로필 README 반영 (계정 허브)

계정 자체에 소개 페이지를 만드는 특수 레포.

1. GitHub `+` → `New repository`
2. Repository name에 **본인 GitHub 계정명과 정확히 동일하게** 입력 (예: 계정이 `scarletbird`라면 레포명도 `scarletbird`)
3. GitHub가 "이건 특수 레포입니다" 안내를 보여줌 → `Public`으로 생성
4. 이 레포를 SourceTree로 클론 → `github_프로필_README.md` 내용을 `README.md`로 저장해 넣기
5. `{계정}`, `{지식베이스-레포}` 등 플레이스홀더를 실제 값으로 치환
6. Stage → Commit → Push
7. 본인 GitHub 프로필 페이지(`github.com/{계정}`)를 열면 이 README가 자동으로 표시됨.

---

## 9. 앞으로의 일상 작업 흐름 (요약)

```
파일 수정/추가 (탐색기 or 편집기)
      ↓
SourceTree: File Status → Stage All
      ↓
커밋 메시지 작성 → Commit
      ↓
Push
      ↓
GitHub / Pages에 반영 확인
```

- 문서 하나 게시할 때마다 이 사이클 한 번.
- 커밋 메시지는 짧고 의미 있게: 예) `Add F4: 의존성 주입과 테스트 용이성`
- 여러 파일을 한 번에 올릴 때도, **관련 있는 변경끼리만 묶어서** 커밋하면 나중에 히스토리를 보기 좋다(마스터 플랜 I3 항목과 동일 원칙).

---

## 10. 막히기 쉬운 지점 FAQ

| 상황 | 원인/해결 |
|---|---|
| Push 시 인증 오류 | GitHub 계정 재연결 필요 (`Tools` → `Options` → `Authentication`). 2단계 인증 계정은 토큰 방식 로그인이 필요할 수 있음 |
| 커밋했는데 Push 버튼이 비활성 | 커밋이 하나도 없는지 확인. `File Status`에서 Stage 후 Commit이 먼저 필요 |
| 폴더가 비어서 안 올라감 | §4의 `.gitkeep` 트릭 사용 |
| index.html이 안 보이고 코드만 보임 | Pages 설정(§7)이 아직 안 되어 있거나, 파일명이 정확히 `index.html`인지 확인 |
| 커밋에 실제 Gmail 주소가 노출됨 | §0-B를 건너뛴 경우. 지금이라도 noreply로 바꾸면 **이후 커밋부터** 적용(과거 커밋엔 소급 안 됨) |
| 한글 파일명이 깨져 보임 | 대부분 표시상 문제일 뿐 실제 파일은 정상. 링크 작성 시 URL 인코딩 문제면 파일명을 영문으로 바꾸는 것도 방법 |
