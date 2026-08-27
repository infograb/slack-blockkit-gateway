# 서피스와 토큰 — 어디에 무엇을, 어떤 자격으로

## 서피스 3종

| 서피스 | 무엇 | 블록 한도 | 에이전트 활용 |
|---|---|---|---|
| **Messages** | 채널/DM/스레드의 메시지 | 50 | 주 물대. ephemeral은 봇 토큰 필요 |
| **Modals** (views) | 팝업 폼 | 100 | 정형 입력 수집. `views.open`은 앱 트리거 필요 |
| **App Home** | 앱의 홈 탭 | 100 | 개인 대시보드·긴 목록·페이지네이션 |

- Messages 전용 블록: `markdown`, `context_actions`, `file`, `plan`, `task_card`, `data_visualization`, `workflow_button`(요소) `[문서]`
- Modals 전용 블록/요소: `alert`, `email/url/number/file_input` `[문서]`
- Home 제외: `datetimepicker` / Messages 제외: `rich_text_input` `[문서]`
- table·data_table·container는 Modals 불가 (Messages/Home만) `[문서]`

## 토큰 타입 (실측 중심)

| 자격 | 되는 것 | 안 되는 것 [실측 ✅] |
|---|---|---|
| **유저 토큰 (xoxc)** — 사용자 본인으로 게시 | 블록 메시지, chat.update, 파일 업로드, 대부분의 신형 블록(container/plan/task_card/data_*/card/markdown) | ephemeral ❌ T28, 스트리밍 ❌ T39, multi-select in actions ❌ T08, video ❌ T15(스코프) |
| **봇 토큰 (xoxb)** — 앱으로 게시 | 위 모든 것 + ephemeral, 스트리밍, setStatus, interactivity | 이 볼트에서 미실측 — 앱 생성 필요 |

- 유저 토큰으로 게시하면 **사람 본인이 쓴 것처럼** 보인다. 에이전트 표명 원칙(Slack agent-design: non-human identity)과 충돌하므로, 정식 에이전트는 봇 토큰+앱이 맞다 `[문서]`.
- 이 볼트의 `[실측 ✅]`는 전부 유저 토큰 기준 — 봇 토큰에서만 바뀌는 항목은 위 표와 `references/reference/limits.md` 하단에 모아뒀다.

## Agents & AI Apps 기능 (정식 AI 앱 서피스)

- 앱 설정에서 "Agents" 기능을 켜면: split-view 컨테이너, 세션 사이드바, suggested prompts, 상태줄, Marketplace AI 카테고리 `[문서]`.
- 요구: **유료 플랜**(AI 컨테이너), 게스트 불가, `assistant:write` 자동 부여 `[문서]`.
- `assistant_view` → 2027-02 deprecation, 신형 `agent_view` `[문서 — 2026-08-20]`.
- Marketplace AI 정책: 모델/보관/테넌시 공개, 부정확 가능성 고지, 슬랙 데이터 LLM 학습 금지, 사용자 메시지마다 상태 설정 의무 등 `[문서]`.

## 인터랙티비티 배선 (버튼이 살아나는 조건)

1. Slack 앱 생성 → interactivity 활성화
2. 이벤트 수신: **Socket Mode**(방화벽 친화, 아웃바운드 WebSocket) 또는 **Request URL**(공개 HTTPS)
3. `block_actions` 수신 → 3초 안에 ack → 필요하면 `response_url`이나 `chat.update`로 후속
4. Hermes 계열은 Socket Mode로 인바운드 포트 없이 동작 `[사용자 메모리 — 운영 사례]`

## 출처

- surfaces: https://docs.slack.dev/surfaces/modals
- agent 업데이트: https://docs.slack.dev/changelog/2026/08/20/agent-updates
- Marketplace AI 정책: https://docs.slack.dev/slack-marketplace/slack-marketplace-app-guidelines-and-requirements
- 실측: `references/verified-matrix.md` T08, T15, T28, T39
