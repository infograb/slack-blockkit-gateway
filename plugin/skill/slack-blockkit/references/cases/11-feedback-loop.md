# 11. 피드백 수집 (Feedback Loop)

## 언제 쓰는가

AI 답변의 품질 신호를 모아 개선에 쓰고 싶을 때. "이 답변이 도움 됐나?"를 한 클릭으로 수집.

## 권장 형태: context_actions + feedback_buttons (AI 전용 신형)

```
section:         (AI 답변 본문)
context_actions: [ 👍 도움됨 ] [ 👎 부정확 ] [ 🗑 ]
```

- `feedback_buttons`는 **`context_actions` 블록 안에만** 넣을 수 있다(메시지 전용, elements ≤5) `[문서]`.
- positive/negative 각 버튼: text 75자, **value 필수** 2000자 `[문서]`. value에 답변 ID를 넣어 추적.
- `icon_button`은 현재 아이콘이 **`trash` 하나뿐** `[문서]`. 그리고 **`text` 필드가 사실상 필수** — 없으면 `invalid_blocks: missing required field: text` `[실측 ✅ T38 실패 → T38b 성공]`. (문서는 accessibility_label 중심으로 안내 — 실측 우선)
- 클릭은 `block_actions`로 온다 — **앱 백엔드 필요**. 👎에는 모달로 상세 사유를 받는 흐름을 Slack이 권장 `[문서 — developing-agents]`.
- 페이로드: `references/payloads/feedback-buttons.json` `[실측 ✅ T38b — 렌더 확인]`

## 대안 패턴

| 수단 | 특징 |
|---|---|
| `reaction_added` 이벤트 구독 | UI 추가 없이 👍/👎 이모지 반응을 신호로. Slack 남부 봇도 사용 `[문서 — slack.engineering]` |
| 스레드 답글 자유 피드백 | 정성 피드백. HumanLayer 패턴 (`01` 케이스) |
| 스트림 종료 시 부착 | `chat.stopStream`의 blocks로 feedback_buttons 부착 — 스트리밍 답변의 표준 마무리 `[문서]` |

## 스레드 동작

- 피드백 행은 답변 메시지에 붙는다(별도 메시지 금지). 답변이 스레드 답글이면 피드백도 그 답글에.
- 피드백 수신 후 "피드백 감사합니다"로 갱신하거나 버튼을 비활성화해 중복 수집 방지 `[미검증 — 구현 패턴]`.

## 주의점

- context_actions는 **Messages only** — 모달/Home 불가 `[문서]`.
- 피드백 수집 자체가 목적이 되지 않게 — 답변마다 붙이되 조용한 UI로. context_actions가 시각적으로 작은 이유다.
- 수집한 신호의 저장·학습 사용은 Marketplace AI 정책(슬랙 데이터로 LLM 학습 금지 등)을 확인 `[문서 — Marketplace 정책]`.

## 검증 상태

- feedback_buttons + icon_button 렌더: `[실측 ✅ T38b]`
- 클릭 페이로드 수신: `[미검증]` (앱 백엔드 필요)

## 출처

- feedback_buttons: https://docs.slack.dev/reference/block-kit/block-elements/feedback-buttons-element
- context_actions: https://docs.slack.dev/reference/block-kit/blocks/context-actions-block
- 스트리밍과 함께 출시: https://docs.slack.dev/changelog/2025/10/7/chat-streaming
- 실측: `references/verified-matrix.md` T38, T38b
