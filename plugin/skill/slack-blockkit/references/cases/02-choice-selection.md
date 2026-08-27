# 02. 선택지 제시 (Choice Selection)

## 언제 쓰는가

사람이 옵션 중 하나(또는 여러 개)를 골라야 에이전트가 다음 단계를 진행할 수 있을 때. 환경 선택(dev/stg/prod), 배포 대상, 리뷰어 지정, 다음 액션 분기 등.

## 선택 기준 — 옵션 수와 성격으로 고른다

| 옵션 수 / 성격 | 추천 요소 | 이유 | 검증 |
|---|---|---|---|
| 2개 (예/아니오) | 버튼 (`01` 케이스) | 셀렉트보다 클릭 1회 | [실측 ✅] |
| 3~10개, 단일 선택, 항상 보여야 함 | `radio_buttons` (옵션 ≤10) | 펼침 없이 전부 보임 | [실측 ✅ T09] |
| 3~100개, 단일 선택 | `static_select` (옵션 ≤100) | 공간 절약, 검색 제공 | [실측 ✅ T07] |
| 100개+ 또는 동적 | `external_select` (앱이 옵션 API 제공) | Options Load URL 필요 | [문서] |
| 복수 선택 | `multi_static_select` | section accessory로 | [실측 ✅ T08b] |
| 보조 액션 모음 (항목당 ⋯) | `overflow` (옵션 ≤5) | 공식 Search Results 템플릿 패턴 | [실측 ✅ T07,T22] |
| 체크리스트식 복수 선택 | `checkboxes` (옵션 ≤10) | actions 블록에서도 렌더됨 | [실측 ✅ T11] |

## 권장 형태

**셀렉트 하나를 놓을 때도 "무엇을 고르는 건지" section 텍스트로 맥락을 준다.** placeholder는 150자까지 `[문서]`.

```
section: *배포 환경을 선택하세요* — 선택 즉시 배포가 시작됩니다
actions: [ static_select "환경 선택" (dev/staging/prod) ] [ overflow ⋯ ]
```

- 단일 선택지 + 부가 액션이 있으면 셀렉트 옆에 `overflow`(⋯ 메뉴)를 나란히 둔다 `[실측 ✅ T07]`.
- 선택 결과도 `block_actions`로 오므로 **앱 백엔드 필요**. 없으면 셀렉트는 장식.

### section accessory vs actions 블록 — 중요한 실측 차이

- `static_select`, `radio_buttons`, `checkboxes`, `overflow`는 **actions 블록**에 넣는 것이 일반적 `[실측 ✅ T07, T09, T11]`.
- **`multi_static_select` / `multi_users_select`는 actions 블록에서 실측 거부됨** — `invalid_blocks: unsupported element: multiselect` `[실측 ✅ T08, T08c — 유저 토큰 기준]`. **section의 `accessory`로 넣으면 성공·렌더됨** `[실측 ✅ T08b]`.
  - 문서상 multi-select는 actions 호환으로 표기되어 있어 충돌. 유저 토큰 한정 현상일 가능성 있음 — 봇 토큰에서는 `[미검증]`. 안전한 기본값: **multi-select는 항상 section accessory로**.

## 스레드 동작

- 선택 프롬프트는 부모 메시지에. 선택이 완료되면 `chat.update`로 "staging 선택됨 ✅"으로 갱신하고 셀렉트를 제거 — 이후 사람들이 뭘 골랐는지 흔적이 남는다.
- 선택지마다 설명이 필요하면 option의 `description`(75자)을 쓰거나, 긴 설명은 스레드 답글로.

## 대안 패턴

- **옵션에 URL을 달고 싶으면** `overflow`만 가능하다 (option의 `url` 필드는 overflow 전용) `[문서]`. 클릭 시 외부 페이지로 나간다.
- 사람/채널을 고르게 하려면 `users_select`/`conversations_select`/`channels_select` (슬랙 네이티브 피커) `[문서]`. multi_users_select는 위 실측 주의 참조.
- 그룹화가 필요하면 `option_groups` (그룹 ≤100, 그룹당 옵션 ≤100) `[문서]`.

## 주의점

- option `text` 75자, `value` 150자, `description` 75자 `[문서]`. select/multi-select의 option은 `plain_text`만, radio·checkboxes는 mrkdwn 허용 `[문서]`.
- overflow 옵션은 **최대 5개** `[실측 ✅ T21 — 6개 거부 확인]`. 하한은 문서에 "up to five"만 있고 1개도 수락됨 `[실측 ✅ T20]`.
- 정적 옵션 선택 해제 시 `null`이 페이로드로 온다 — 앱이 처리해야 `[문서]`.
- 셀렉트는 선택하는 순간 페이로드를 본낸다. "여러 개 고르고 확정 버튼" 흐름이 필요하면 multi-select + 별도 확인 버튼 조합으로.

## 검증 상태

- static_select/overflow/radio/checkboxes/datepicker 계열: `[실측 ✅ T07, T09, T10, T11]`
- multi-select in section accessory: `[실측 ✅ T08b]` / in actions 거부: `[실측 ✅ T08, T08c]`
- external_select·option_groups: `[문서]` (미실측)

## 출처

- 엘리먼트 레퍼런스: https://docs.slack.dev/reference/block-kit/block-elements/select-menu-element , https://docs.slack.dev/reference/block-kit/block-elements/multi-select-menu-element , https://docs.slack.dev/reference/block-kit/block-elements/overflow-menu-element
- 공식 Search Results 템플릿(항목당 overflow): https://pkg.go.dev/github.com/slack-go/slack/examples/blocks
- 실측: `references/verified-matrix.md` T07, T08, T08b, T08c, T09, T11, T20, T21, T22
