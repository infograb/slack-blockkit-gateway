# 제한값 총표 (Limits)

> 페이로드 작성 전에 여기서 수치를 확인한다. `[실측 ✅]`는 2026-08-24 유저 토큰으로 직접 확인한 값.
> 초과 시 동작: blocks 관련은 **`invalid_blocks`로 메시지 전체 미게시** `[실측 ✅]`, text 40,000자 초과는 경고와 함께 잘림 `[문서]`.

## 메시지/서피스 전역

| 항목 | 값 | 근거 |
|---|---|---|
| 메시지당 blocks | **50** | [실측 ✅ T17 — 51개 거부, 50개 성공] |
| 모달·App Home당 blocks | 100 | [문서] |
| top-level `text` (폴 스트링) | **40,000자** (초과 시 `message_truncated` 경고·잘림) | [문서 — 2018 changelog] — 4,024자 저장 확인 [실측 ✅ T19] |
| markdown 블록 합산 | 12,000자/payload | [문서] |
| `block_id` | 255자 | [문서] |
| `action_id` | 255자 (블록 내 유일) | [문서] |
| `metadata` event_payload | JSON, 스키마 등록 필요 | [문서] |

## 텍스트 객체·블록별

| 항목 | 값 | 근거 |
|---|---|---|
| text object `text` | min 1 / **max 3000** | [실측 ✅ T16 — 3001 거부, 3000 성공] |
| section `fields` | 최대 10개, 각 2000자 | [문서] |
| header | plain_text만, **150자** | [실측 ✅ T18 — 151자 거부] |
| context `elements` | 10개 (image+text만) | [문서] |
| context_actions `elements` | 5개 (feedback_buttons/icon_button만) | [문서] |
| actions `elements` | **25개** | [문서] — 6개 버튼 렌더 확인 [실측 ✅ T23] |
| container `title` | 150자, `child_blocks` 10개 | [문서] — 접기 렌더 [실측 ✅ T30] |
| card | title/subtitle 150, body/subtext 200, 버튼 ≤3 | [문서] — 렌더 [실측 ✅ T32] |
| alert (Modals만) | text 200자 | [문서] |
| plan | tasks 50개, **title은 문자열** | [문서] — title text 객체 시 거부 [실측 ✅ T35] |
| task_card | **title은 문자열** | [실측 ✅ T36] |
| carousel | 카드 1~10 | [문서] |
| table | 행 100 × 열 20, **셀 합산 10,000자** | [문서] — 렌더 [실측 ✅ T14] |
| data_table | 행 2~201, 열 1~20, 셀 합산 20,000자, page_size ≤100 | [문서] — 페이지네이션 렌더 [실측 ✅ T40d] |
| data_visualization | 메시지당 2개, title 50자, 세그먼트/시리즈 1~12, 포인트 1~20 | [문서] — 파이 렌더 [실측 ✅ T31] |
| image | image_url 3000자, alt_text 2000자(필수), png/jpg/gif | [문서] — 외부 URL 로드 실패 사례 [실측 ✅ T04] |
| video | title <200 + `links.embed:write` + 도메인 등록 | [문서] — 스코프 부재 거부 [실측 ✅ T15] |

## 인터랙티브 엘리먼트

| 항목 | 값 | 근거 |
|---|---|---|
| 버튼 `text` | plain_text **75자** | [실측 ✅ T24 — 76자 거부] |
| 버튼 `value` | 2000자 | [문서] |
| 버튼 `url` | 3000자 | [문서] |
| placeholder | plain_text 150자 | [문서] |
| option `text` | 75자 (select/overflow/multi는 plain_text만) | [문서] |
| option `value` | 150자 / `description` 75자 | [문서] |
| static_select `options` | 100개 (또는 option_groups 100×100) | [문서] |
| overflow `options` | **최대 5개** | [실측 ✅ T21 — 6개 거부, 5개 성공, 1개 수락 T20] |
| radio `options` | 10개 | [문서] |
| checkboxes `options` | 10개 | [문서] |
| confirm | title 100 / text 300 / 버튼 각 30자 | [문서] — 페이로드 수락 [실측 ✅ T27] |
| plain_text_input | min/max_length 3000자 | [문서] — 메시지 내 렌더 [실측 ✅ T12] |
| file_input (Modals만) | 파일당 100MB, 최대 10개 | [문서] |
| 모달 title/close/submit | 각 24자 / private_metadata 3000자 / callback_id 255자 | [문서] |

## API·레이트리밋 (에이전트 관련)

| 항목 | 값 | 근거 |
|---|---|---|
| chat.update 진행 갱신 권장 | 최대 3초에 1회 | [문서 — developing-agents] |
| chat.startStream/stopStream | Tier 2 (20+/분), markdown_text 12,000자 | [문서] |
| chat.appendStream | Tier 4 (100+/분) | [문서] |
| 스트림 청크 task_update/plan_update | 각 256자, blocks 청크당 50 | [문서] |
| assistant.threads.setStatus | 600 req/분/app/team, loading_messages 10개 | [문서] |
| setSuggestedPrompts | 프롬프트 4개 | [문서] |
| 스니펫 업로드 | 1MB | [문서] |
| 인라인 이미지 프리뷰 | 긴 변 <25,000px, 총 <45M 화소 | [문서 — slack.com 헬프] |

## 토큰 타입별 가능 여부

| 기능 | 유저 토큰(xoxc) | 봇 토큰(xoxb) | 근거 |
|---|---|---|---|
| 블록 메시지 게시·수정 | ✅ | ✅ | [실측 ✅] |
| ephemeral | ❌ `not_allowed_token_type` | ✅ | [실측 ✅ T28] |
| 스트리밍 | ❌ `not_allowed_token_type` | ✅ | [실측 ✅ T39] |
| multi-select in actions 블록 | ❌ `unsupported element` | 미검증 (문서상 가능) | [실측 ✅ T08] |
| video 블록 | ❌ (스코프 필요) | 스코프 있으면 ✅ | [실측 ✅ T15] |
