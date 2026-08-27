# 엘리먼트 카탈로그 (인터랙티브·입력)

> 블록 안에 들어가는 요소들. 공통: `action_id` 255자(블록 내 유일), `placeholder` plain_text 150자, `focus_on_load`는 view당 1개.
> 클릭/선택 시 `block_actions` 페이로드 발송 — **앱 백엔드가 있어야 반응한다** `[문서]`.

## 버튼·액션 계열

| 엘리먼트 | 들어가는 블록 | Surface | 핵심 제한·특이 | 실측 |
|---|---|---|---|---|
| `button` | section, actions | M V H | text 75자 ✅T24, value 2000, url 3000, style primary/danger, confirm 지원, `agent_prompt`(Slackbot 핸드오프) 4000자 | ✅ T06 T27 |
| `overflow` | section, actions | M V H | options **≤5** ✅T21, option에 url 가능(유일) | ✅ T07 T20 T22 |
| `workflow_button` | section, actions | M만 | workflow trigger 필수, action_id 필수 | 미실측 |
| `feedback_buttons` | context_actions만 | M만 | text 75, value 2000(필수) | ✅ T38b |
| `icon_button` | context_actions만 | M만 | icon은 `trash`만, **text 필수** ✅T38 | ✅ T38b |

## 선택 계열

| 엘리먼트 | 들어가는 블록 | Surface | 핵심 제한·특이 | 실측 |
|---|---|---|---|---|
| `static_select` | section, actions, input | M V H | options ≤100 또는 option_groups ≤100 | ✅ T07 |
| `external_select` | section, actions, input | M V H | Options Load URL 필요, min_query_length 기본 3 | 미실측 |
| `users_select` / `conversations_select` / `channels_select` | section, actions, input | M V H | initial_*, filter, response_url_enabled(모달 input만) | 미실측 |
| `multi_static_select` | section, actions, input | M V H | options ≤100, **actions에서 유저 토큰 거부 → section accessory로** | ✅ T08b / ❌ T08 T08c |
| `multi_external_select` / `multi_users_select` / `multi_conversations_select` / `multi_channels_select` | section, actions, input | M V H | max_selected_items, multi_users_select도 actions에서 거부 확인 | ❌ T08c |
| `radio_buttons` | section, actions, input | M V H | options ≤10, option mrkdwn 허용 | ✅ T09 |
| `checkboxes` | section, actions, input | M V H | options ≤10, initial_options는 options와 정확히 일치 | ✅ T11 |

## 날짜·시간 계열

| 엘리먼트 | 들어가는 블록 | Surface | 특이 | 실측 |
|---|---|---|---|---|
| `datepicker` | section, actions, input | M V H | initial_date YYYY-MM-DD | ✅ T10 |
| `timepicker` | section, actions, input | M V H | initial_time HH:mm(24h), timezone IANA | ✅ T10 |
| `datetimepicker` | actions, input | M V (**H 제외**) | initial_date_time UNIX 초 | ✅ T10 |

## 텍스트 입력 계열 (주로 input 블록 안)

| 엘리먼트 | Surface | 특이 | 실측 |
|---|---|---|---|
| `plain_text_input` | M V H | multiline, min/max_length ≤3000, dispatch_action_config | ✅ T12 (메시지 내) |
| `rich_text_input` | V H (**M 제외**) | action_id 필수, min/max_lines 1~100(기본 8) | 미실측 |
| `email_text_input` / `url_text_input` / `number_input` | **V만** | number는 is_decimal_allowed 필수, min/max는 문자열 | 미실측 |
| `file_input` | **V만** | max_files 10, 파일당 100MB, files:read 필요, dispatch_action 병용 불가 | 미실측 |

## 콘텐츠 엘리먼트

| 엘리먼트 | 들어가는 곳 | 특이 |
|---|---|---|
| `image` (element) | section accessory, context | image_url 3000자 또는 slack_file, alt_text 필수 |
| `url` (URL source) | task_card.sources | url+text 필수 |

## rich_text 하위 요소 (rich_text 블록 남부 전용)

| 요소 | 용도·핵심 필드 |
|---|---|
| `rich_text_section` | 원자 요소 컨테이너 |
| `rich_text_list` | style bullet/ordered, indent, offset, border |
| `rich_text_preformatted` | 코드블록, language(구문강조), border |
| `rich_text_quote` | 인용, border |
| `text` | style: bold/italic/strike/highlight/underline 등 |
| `link` | url 필수, from_llm, truncated 등 |
| `date` | timestamp+format 토큰, fallback |
| `emoji` / `broadcast` / `channel` / `user` / `usergroup` / `team` / `color` / `tag` | 각종 참조·장식 |

## 인터랙션 페이로드 발송 시점

- button: 클릭 시 / checkboxes: 체크·해제 시 / datepicker: 날짜 선택 후 닫힐 때 / multi_*_select: 항목 선택마다 / overflow·radio·*_select: 선택 시 / plain·rich_text_input: dispatch_action_config에 따라 `[문서]`.
- 정적 옵션 선택 해제 시 `null` 반환 `[문서]`.

## 출처

- 엘리먼트 레퍼런스 총괄: https://docs.slack.dev/reference/block-kit/block-elements/
- block_actions 페이로드: https://docs.slack.dev/reference/interaction-payloads/block_actions-payload
