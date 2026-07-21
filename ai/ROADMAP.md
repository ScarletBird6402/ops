# ROADMAP

> 4단계로 성장하는 저장소. 각 단계는 이전 단계 위에 쌓이되, 병행 진행도 가능(특히 1단계는 상시).

## 현재 위치
- 단계: 1 (트렌드 노트, 상시) + 2 (워밍업 프로젝트, 착수)
- 진행: Chapter 1 노트 6편 발행(아래 노트 목록)
- 다음 액션: 단계 2 환경 세팅 / 단계 1 다음 노트(강화학습 기초)
- 최근 갱신: 2026-07-19

---

## 단계 1 — 트렌드 따라잡기 (상시)
> 최신 AI/ML 흐름을 노트로 정리. 완결된 프로젝트가 아니어도 됨. `notes/`에 누적(HTML, 심화 규격).

- [x] 노트 작성 규칙 정하기 → 심화 학습자료 규격 확정(수식·직관·구현 3종 세트, shape 주석, 원 논문 앵커)
- [ ] Chapter 1 — 기초 계보 (확립된 것):
  - 딥러닝 수식을 읽기 위한 수학 재가동 (프리퀄)
  - 신경망 준비운동 — ANN에서 CNN·RNN까지
  - RNN의 한계에서 attention, self-attention, Transformer까지
  - BERT vs GPT: 사전학습→미세조정, instruction tuning
  - ViT — CNN의 inductive bias와의 트레이드오프
  - LLM 시대 — instruction tuning과 RLHF
  - 강화학습 기초 — MDP에서 정책 그래디언트까지
  - Diffusion — 잡음 제거로 생성하기
  - 손실 함수와 학습 레시피의 진화: focal / InfoNCE / AdamW / SpecAugment / LoRA
  - 학습 패러다임의 지도: 지도학습에서 zero-shot까지
- [ ] Chapter 2 — 진행형 트렌드 2021→2026 (개괄, 시점 표기):
  - 멀티모달: CLIP → VLM → 네이티브 멀티모달
  - RAG / 에이전트 성숙(도구 사용·MCP) / SSM·Mamba
  - 추론 모델과 test-time compute
  - MoE·효율화·오픈웨이트 생태계
- [ ] 도메인·심화 노트 (상시):
  - 오디오 자기지도 학습(SSL): wav2vec2 / HuBERT / BEATs 계열
  - Mel-spectrogram — 왜, 어떻게 계산되는가
  - SELD 태스크 해부: SED + DOA, Multi-ACCDOA 출력 표현
  - 오디오비주얼 SELD: 비전 결합 구조와 임베딩 융합
  - (심화) 암시적 신경 표현(INR/neural field)과 공간 음향
  - (심화) 연산자 학습(DeepONet/FNO)과 파동 전파

### 노트 목록
0. [딥러닝 수식을 읽기 위한 수학 재가동](<notes/딥러닝 수식을 읽기 위한 수학 재가동.html>)
1. [신경망 준비운동 — ANN에서 CNN·RNN까지](<notes/신경망 준비운동 — ANN에서 CNN·RNN까지.html>)
2. [RNN의 한계에서 Transformer까지](<notes/RNN의 한계에서 Transformer까지.html>)
3. [BERT vs GPT — 사전학습과 미세조정](<notes/BERT vs GPT — 사전학습과 미세조정.html>)
4. [ViT — CNN의 inductive bias와 트레이드오프](<notes/ViT — CNN의 inductive bias와 트레이드오프.html>)
5. [LLM 시대 — instruction tuning과 RLHF](<notes/LLM 시대 — instruction tuning과 RLHF.html>)

## 단계 2 — 간단한 프로젝트 (목표: 2026-10)
> 작게 완주하는 프로젝트로 실습 감각 복원. 스케일보다 완주 우선.

- [ ] 도구 체인 정비: PyTorch 2.12(CUDA) + librosa
      (오디오 I/O: torchaudio가 유지보수 단계로 전환·TorchCodec 이관 → librosa 채택)
- [ ] 주제: ESC-50 환경음 분류 — waveform → log-Mel → CNN, end-to-end 완주
- [ ] 완료 기준: 새 가상환경에서 README 명령만으로 재현 실행 → 동일 평가 숫자
- [ ] 산출물: `projects/00-esc50-warmup/` + README + requirements(버전 고정) + 시드 고정

## 단계 3 — 본 프로젝트: DCASE SELD 재현·개선 (목표: 2027-03)
> 규모 있는 과제에 재현·개선으로 참여. 완결성 > 순위.

- [ ] 과제 구조 파악: SELD = SED(무슨 소리) + DOA(어느 방향) 결합
- [ ] 베이스라인 선정: DCASE 2022~2023 FOA 계열(SELDnet CRNN + Multi-ACCDOA, STARSS 데이터셋)
      — 태스크 형식이 안정적이고 DOA 추정 구조가 명확한 구간
- [ ] 공식 베이스라인 재현 (환경 세팅 → 실행 → 결과 숫자 일치 확인)
- [ ] 평가 지표 정리: SED 지표(ER/F-score) + DOA 오차 지표(LE/LR)
- [ ] 개선 지점 1개 선정·실험 (후보: 사전학습 오디오 SSL 임베딩을 입력 특징으로)
- [ ] 결과 분석: 신호처리/모델 관점에서 "왜"
- [ ] 산출물: `projects/01-seld-dcase/` + 재현·개선 리포트
- [ ] (선택) DCASE 2027 챌린지 제출 — 오디오 트랙 기본, 오디오비주얼 트랙은 여력 시
      (Task 3는 2023년부터 오디오비주얼 트랙 병행: STARSS23 = 오디오 + 정렬된 비디오)

## 단계 4 — 확장 (목표: 미정)
> 음향 중심에서 인접 영역으로 확장. 다음 프로젝트 주제는 여기서 결정.

- [ ] 확장 방향 후보(심화 노트에서 숙성 중인 주제들):
  - 오디오비주얼 SELD 심화 — 비전 인코더 결합, 임베딩 융합
  - 강화학습 응용 — 능동 음원 탐색(active sound source localization): 에이전트가 이동·회전하며
    음향 단서(채널 간 시간차·레벨차)로 음원 방향을 찾는 정책 학습. 소형 시뮬레이션 환경 + 기본
    정책 그래디언트로 시작 ('강화학습 기초' 노트의 실습 확장, DOA 주제와 연속)
  - 암시적 신경 표현(INR/neural field) 기반 공간 음향 표현·증강
  - 연산자 학습(DeepONet/FNO) — 파동 전파의 학습 기반 서로게이트
  - 통신/RF 신호처리 — 변조·채널 모델·검출: 음향과 같은 신호처리 뿌리에서 인접 도메인으로 확장
- [ ] 다음 프로젝트 착수 (`projects/02-...`)

---

## 갱신 이력
- 2026-07-04: 저장소 생성, 4단계 로드맵 수립
- 2026-07-05: 계획 구체화 — 도구 체인 확정(PyTorch 2.12·librosa), 단계 2 주제 ESC-50 확정,
  단계 3 베이스라인 앵커(2022~2023 FOA) 확정, 노트 커리큘럼 초안·단계 4 확장 후보 추가
- 2026-07-09: 노트 목록에 강화학습 기초 추가(Chapter 1), 단계 4 확장 후보에 능동 음원 탐색(RL) 추가
- 2026-07-17: 단계 4 확장 후보에 통신/RF 신호처리 추가
- 2026-07-19: Chapter 1 노트 6편(0~5) 발행, 노트 목록 등재
