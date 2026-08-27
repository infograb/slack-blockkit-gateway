# 06. 진행 상태와 스트리밍 (Progress & Streaming)

## 언제 쓰는가

작업이 오래 걸릴 때(수 초~수십 분) 사람이 "아직 돌고 있나"를 알아야 하고, LLM 답변을 실시간으로 보여주고 싶을 때.

## 수단 선택표

| 상황 | 수단 | 요구 | 검증 |
|---|---|---|---|
| 단계 진행 (1/3 → 3/3) | **`chat.update`로 같은 메시지 갱신** | chat:write | [실측 ✅ T26] |
| 다단계 작업의 체크리스트 | **`plan` 블록** (task ≤50, 상태 pending/in_progress/complete/error) | chat:write (스트림 청크 또는 메시지) | [실측 ✅ T35b] |
| 개별 작업 상세 카드 | **`task_card` 블록** (status/details/output/sources) | chat:write | [실측 ✅ T36b] |
| LLM 토큰 스트리밍 | **`chat.startStream/appendStream/stopStream`** | **봇 토큰 필수** | [실측 ✅ T39 — 유저 토큰 거부 확인] |
| "OO이 생각 중…" 상태줄 | `assistant.threads.setStatus` / `agents.sessions.setStatus` | assistant:write 또는 chat:write (2026-03-05~) | [문서] |
| 긴 작업 살아있음 표시 | 주기적 `chat.update` (최대 3초에 1회 권장) | chat:write | [문서 — developing-agents] |

## 권장 형태

### A. 갱신형 진행 메시지 (가장 범용)

새 메시지를 쌓지 말고 **같은 메시지를 덮어쓴다**:

```
1차 게시:  :hourglass_flowing_sand: *배포 진행 중* (1/3) 빌드…
           context: started 12:53:00
완료 시:   :white_check_mark: *배포 완료* (3/3)
           context: started 12:53:00 • finished 12:55:41
```

- `[실측 ✅ T26 — chat.update로 내용 교체 확인]`
- 갱신 빈도는 **최대 3초에 1회**가 Slack 공식 권장 `[문서 — developing-agents]`.
- 진행 바는 유니코드 블록(`████░░ 60%`)이나 이모지로 텍스트 내에서 흉내 — 네이티브 프로그레스 바 블록은 없다 `[미검증 — 없다는 공식 명시는 없으나 블록 카탈로그에 부재]`.

### B. plan / task_card (2026-02-11 추가) — "생각 과정 보여주기"

- `plan`: 작업 목록을 하나의 블록에. **title은 text 객체가 아니라 문자열**이다 — text 객체로 본낼 시 `invalid_blocks` `[실측 ✅ T35 실패 → T35b 성공]`. tasks 최대 50.
- `task_card`: 개별 작업 하나. title 역시 문자열. `status`(in_progress/complete/error), `details`/`output`(rich_text), `sources`(url 배열) `[실측 ✅ T36b]`.
- 스트리밍 중 `task_display_mode: plan|timeline`과 `task_update`/`plan_update` 청크(각 256자)로 실시간 갱신 `[문서]`.
- 페이로드: `references/payloads/plan-tasks.json`

### C. 스트리밍 (LLM 답변)

- `chat.startStream` → `chat.appendStream`(markdown_text 청크, 12,000자/호출) → `chat.stopStream`(여기서만 최종 blocks 부착 가능) `[문서]`.
- **유저 토큰(xoxc)으로는 `not_allowed_token_type`으로 실패** `[실측 ✅ T39]`. 봇 토큰 + `chat:write`.
- 레이트리밋: start/stop Tier 2(20+/분), append Tier 4(100+/분) `[문서]`.
- 스트림 중 언펄 비활성화, 사용자 중단 시 append가 `stopped_by_user`로 실패 `[문서]`.
- 스트리밍 답변은 **스레드 답글**이 원칙("Streamed messages should always be replies") `[문서]`.

### D. 상태줄 (setStatus)

- "Jeeves is working on your request…" 같은 로딩 UX. legacy `assistant.threads.setStatus`(커스텀 문구 + loading_messages ≤10), 신형 `agents.sessions.setStatus`(processing/active/suspended/closed 고정) `[문서]`.
- Marketplace 정책상 에이전트 앱은 **사용자 메시지마다 상태를 설정해야 함** `[문서]`.
- 채널에서도 2026-03-05부터 chat:write 스코프로 사용 가능 `[문서]`.
- 봇용 typing indicator("입력 중…")는 **존재하지 않는다** — Slack 스태프 확인. 대안이 setStatus와 스트리밍 `[문서 — bolt-js#885]`.

## 스레드 동작

- 진행 메시지는 **요청이 있던 스레드의 답글**로 — 채널 메인 타임라인을 오염시키지 않는다.
- 작업 완료 후 진행 메시지는 결과로 갱신(condense)하거나, 요약 카드로 교체 (`01`의 resolved state).
- 장시간 작업은 부모에 "시작됨" 1회 + 완료 시 결과 1회만 남기고 중간 진행은 스레드 안에서 갱신.

## 주의점

- plan 블록 task status의 완전한 enum은 문서 두 곳이 다르게 표기(plan 예시: pending/in_progress/complete, task_card: in_progress/complete/error) — 통합 enum은 `[미검증]`. 실측으로 pending/in_progress/complete 렌더 확인 `[실측 ✅ T35b]`.
- `chat.update` 실패 시(메시지 삭제 등) 새 메시지로 폴 스트링.
- 에이전트가 멈추면 상태도 반드시 지운다 — 걸린 상태로 남는 로딩은 최악의 신호 `[문서 — developing-agents]`.

## 검증 상태

- chat.update / plan / task_card: `[실측 ✅ T26, T35b, T36b]`
- 스트리밍 유저 토큰 거부: `[실측 ✅ T39]`; 스트리밍 자체 동작: `[문서]`
- setStatus: `[문서]` (assistant:write 스코프 앱 필요, 미실측)

## 출처

- 스트리밍 changelog: https://docs.slack.dev/changelog/2025/10/7/chat-streaming
- plan/task_card changelog: https://docs.slack.dev/changelog/2026/02/11/task-cards-plan-blocks
- plan 블록: https://docs.slack.dev/reference/block-kit/blocks/plan-block
- task_card 블록: https://docs.slack.dev/reference/block-kit/blocks/task-card-block
- 에이전트 개발 가이드(3초 갱신 권장): https://docs.slack.dev/ai/developing-agents
- setStatus: https://docs.slack.dev/reference/methods/assistant.threads.setStatus/ , https://docs.slack.dev/reference/methods/agents.sessions.setStatus
- typing indicator 부재: https://github.com/slackapi/bolt-js/issues/885
- 실측: `references/verified-matrix.md` T26, T35, T35b, T36b, T39
