# 01. 승인/거절 결정 받기 (Approval)

## 언제 쓰는가

에이전트가 되돌리기 어렵거나 영향이 큰 작업(배포, 이메일 발송, 결제, 데이터 삭제, 외부 시스템 쓰기)을 하기 전에 사람의 결정을 받아야 할 때. "핵심은 사람이 슬랙을 떠나지 않고 10~30초 안에 결정하게 만드는 것"이다 `[문서 — StackAI HITL 가이드]`.

## 권장 형태 (기본 패턴: 승인 카드)

업계 표준 구조는 4층이다 — **한 줄 요약 → 근거 팩(fields) → 구분선 → 버튼**:

1. **한 줄 요약** (section, mrkdwn): "누가, 무엇을, 왜 승인해야 하는지" — 예: `*배포 승인 요청* — api-server v2.3.1 → prod`
2. **근거 팩** (section `fields`, 2열): 사람이 맹목 승인하지 않도록 결정에 필요한 증거를 2열 그리드로. fields는 최대 10개, 각 2000자 `[문서]`
3. **divider**
4. **버튼 행** (actions): `primary`(초록) 승인 + `danger`(빨강) 거절. 파괴적 작업은 버튼에 `confirm` 객체를 달아 네이티브 확인 다이얼로그를 한 번 더 띄운다 `[실측 ✅ T27 — confirm 페이로드 수락 확인]`

```
[ 승인 카드 구조 ]
section:  *배포 승인 요청* api-server v2.3.1 → prod
section:  fields = [커밋 14개, 테스트 312/312, 변경 파일 9, 롤백 가능]
divider
actions:  [ 승인(primary) ] [ 거절(danger) ] [ diff 보기(url) ]
context:  요청: deploy-agent • 2026-08-24 12:40 • run-123
```

페이로드: `references/payloads/approval-card.json` `[실측 ✅ T06, T27]`

### 결정 후 처리 (Resolved state) — 반드시 할 것

클릭이 처리되면 `chat.update`로 카드를 결과 상태로 바꾼다: 버튼을 제거하고 "✅ 승인됨 — @user, 12:43" 같은 한 줄 기록으로 압축한다. 죽은 버튼을 화면에 남기지 않는 것이 Slack 공식 디자인 가이드("cleaning up after your app") `[문서]`. `chat.update` 자체는 `[실측 ✅ T26]`.

### confirm 다이얼로그

모든 인터랙티브 엘리먼트에 `confirm` 객체를 달 수 있다. title 100자 / text 300자 / 버튼 라벨 각 30자 `[문서]`. "프로덕션 배포"처럼 실수 클릭이 치명적인 버튼에는 기본 장착. `[실측 ✅ T27 — 페이로드 수락, 다이얼로그 렌더는 클릭 시 발생]`

## 스레드 동작

- **요청은 부모 메시지로** (채널에 보여야 다른 사람도 진행 상황을 안다) — 단, 승인자 개인에게만 필요하면 DM (`12-thread-and-surface-strategy.md`).
- **결정 근거가 길면**(diff 전문, 로그) 부모는 카드만 두고 근거는 스레드 답글 또는 스니펫으로 (`05-collapsed-long-content.md`).
- **자유 텍스트 피드백 병행**: HumanLayer의 프로덕션 패턴 — 버튼과 함께 "이 스레드에 텍스트로 답하셔도 됩니다"를 안내하고, 답글 텍스트를 LLM 피드백으로 넘긴다 `[문서 — HumanLayer]`.
- 결정 완료 후 카드 갱신 + 결과를 스레드 답글로도 남기면 감사 추적이 쉽다.

## 대안 패턴

| 패턴 | 적합한 경우 | 비고 |
|---|---|---|
| 3지선다 이상 | "승인/수정요청/거절" | 버튼 3개까지 한 행에 무리 없음. Wrangle·LangGraph는 approve/edit/reject 3종을 권장 `[문서]` |
| reacji 승인 (👍 이모지) | 가벼운 게이트, 감사 불필요 | Sleuth 배포 승인 방식. 앱이 `reaction_added`를 구독해야 함. 감사·검색에 불리 `[문서]` |
| 선택지가 많은 승인 | 옵션 고르기 | `02-choice-selection.md`의 셀렉트 |
| 모달 폼 승인 | "수정 후 승인" | n8n Send-and-Wait 패턴 — 외부 폼/모달에서 내용을 고쳐 제출 `[문서]` |

## 주의점

- **버튼은 렌더되지만 클릭 처리는 앱이 필요하다.** `block_actions` 페이로드를 받을 interactivity 엔드포인트(Socket Mode 또는 Request URL)가 없으면 버튼은 장식이다. 백엔드가 없으면 `url` 버튼(외부 시스템 링크)으로 대체 `[문서]`.
- **버튼 라벨 75자 제한** `[실측 ✅ T24 — 76자 거부 확인]`. 라벨은 결과를 말하는 동사("배포 승인")로, "클릭하세요" 금지 `[문서 — Slack 디자인 가이드]`.
- **actions 블록당 요소 25개** `[문서]` — 6개 버튼 한 행 렌더 확인 `[실측 ✅ T23]`.
- 승인자를 제한하려면 앱이 클릭한 유저 ID를 검사한다(HumanLayer `allowed_responder_ids` 패턴) `[문서]`. 비대상자 클릭 시 동작(무시 vs ephemeral 경고)은 구현 의존 `[미검증]`.
- `value` 필드에 run-id 같은 상관관계 ID를 넣어 어떤 실행에 대한 승인인지 추적한다 (2000자까지) `[문서]`.

## 검증 상태

- 승인 카드 구성 요소 전부: `[실측 ✅ T02, T03, T06, T27]` (2026-08-24, 유저 토큰)
- chat.update 갱신: `[실측 ✅ T26]`
- confirm 다이얼로그 상호작용: 페이로드 수락만 확인, 실제 클릭 플로우는 앱 백엔드 필요 `[미검증]`

## 출처

- HumanLayer 승인 카드 실물: https://github.com/humanlayer/humanlayer/blob/main/docs/images/slack-conversation.png
- Slack 에이전트 거버넌스 가이드(Always allow/Allow once/Deny): https://docs.slack.dev/ai/agent-governance
- Slack 디자인 가이드(cleaning up): https://docs.slack.dev/concepts/designing-with-block-kit
- StackAI HITL 설계: https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation
- Wrangle 승인 워크플로 비판: https://www.wrangle.io/post/managing-approval-workflows-in-slack
- 실측: `references/verified-matrix.md` T06, T23, T24, T26, T27
