# 실측 검증 매트릭스 (T01~T49)

> 환경: 2026-08-24, InfoGrab 테스트 워크스페이스(workspace ID는 공개 패키지에서 제거), **유저 토큰(xoxc)**, `chat.postMessage`를 본인 DM 스레드에 게시.
> "수락" = API ok:true, "렌더" = 데스크톱 클라이언트 시각 확인, "저장" = `conversations.replies` 조회 확인.

> 추가 환경: 2026-08-27, 동일 워크스페이스의 **봇 토큰(xoxb)**, 테스트 스레드에 게시. 공개 패키지에는 channel/ts를 기록하지 않는다. T43~T49는 API `ok:true`와 `conversations.replies`의 저장 block type을 확인했다.

## 표시 블록

| ID | 시험 내용 | 결과 |
|---|---|---|
| T01 | section + mrkdwn 전종 (bold/italic/strike/code/quote/fence/링크/`<!here>`/이모지) | ✅ 수락·렌더 |
| T02 | header + divider + context(아이콘+텍스트) | ✅ 수락·렌더 |
| T03 | section fields 2열×4 + accessory 이미지 | ✅ 수락·렌더 |
| T04 | image 블록 (외부 thrillist URL) | ✅ 수락 / ⚠️ **이미지 로드 실패 — alt만 표시**. 외부 URL은 불안정, 업로드 권장 |
| T05 | rich_text (section/bullet list/preformatted/quote) | ✅ 수락·렌더 |

## 인터랙티브

| ID | 시험 내용 | 결과 |
|---|---|---|
| T06 | 버튼 3종 (primary/danger/url) | ✅ 수락·렌더 |
| T07 | static_select + overflow in actions | ✅ 수락·렌더 |
| T08 | multi_static_select **in actions** | ❌ `invalid_blocks: unsupported element: multiselect [json-pointer:/blocks/1]` |
| T08b | multi_static_select **in section accessory** | ✅ 수락·렌더 |
| T08c | multi_users_select in actions | ❌ 동일 에러 `unsupported element: multiselect` |
| T09 | radio_buttons 3옵션 in actions | ✅ 수락·렌더 |
| T10 | datepicker/timepicker/datetimepicker | ✅ 수락·렌더 |
| T11 | checkboxes in actions | ✅ 수락·렌더 |
| T12 | **input 블록 in 메시지** (plain_text_input) | ✅ 수락·렌더 — 구 문서 "모달 전용"과 상이, 현행 문서 Messages 포함 |
| T20 | overflow 옵션 1개 | ✅ 수락·렌더 (하한 제약 없음) |
| T21 | overflow 옵션 6개 | ❌ `no more than 5 items allowed` |
| T22 | overflow 옵션 5개 | ✅ 수락·렌더 |
| T23 | actions에 버튼 6개 | ✅ 수락·렌더 (문서상 25까지) |
| T24 | 버튼 text 76자 | ❌ `must be less than 76 characters` |
| T27 | 버튼 confirm 객체 | ✅ 수락 (다이얼로그 상호작용은 미시험) |
| T38 | icon_button에 text 누락 | ❌ `missing required field: text` |
| T38b | feedback_buttons + icon_button(text 포함) | ✅ 수락·렌더 |

## 신형 블록 (2025~2026 추가)

| ID | 시험 내용 | 결과 |
|---|---|---|
| T13 | markdown 블록 (혼합 문법) | ✅ 수락 — **서버가 CommonMark로 올바르게 파싱해 rich_text로 저장**(API 확인). 첫 렌더는 일시적으로 원문 표시→재렌더 |
| T14 | table 블록 3×3 (raw_text+rich_text) | ✅ 수락·렌더 |
| T15 | video 블록 (youtube) | ❌ `Video validation failed: Bot scopes missing: [links:read, links:write, links.embed:write]` |
| T30 | **container is_collapsible + default_collapsed** | ✅ 수락·**접힘 렌더·클릭 펼침 전부 확인** |
| T31 | data_visualization pie (추정 스키마) | ✅ 수락·렌더 (chart:{type,segments} 유효) |
| T32 | card 블록 (title/body/hero_image/actions) | ✅ 수락·렌더 |
| T35 | plan — title을 plain_text 객체로 | ❌ `must provide a string [/blocks/0/title]` |
| T35b | plan — title 문자열 | ✅ 수락·렌더 (pending/in_progress/complete 아이콘) |
| T36 | task_card — title plain_text 객체 | ❌ 동일 에러 |
| T36b | task_card — title 문자열 + sources | ✅ 수락·렌더 |
| T37 | markdown CommonMark 전종 (**/[]()/~~/#/표/task list/---) | ✅ 수락·렌더·저장 rich_text 검사로 전부 정확 변환 확인 |
| T40 | data_table — columns 속성 + raw_number(value) | ❌ `invalid additional property: columns` 등 |
| T40b | data_table — raw_number(text) | ❌ 셀 스키마 불일치 |
| T40c | data_table — raw_number(value) | ❌ 동일 — **raw_number 셀 거부 결론** |
| T40d | data_table — 전부 raw_text | ✅ 수락·렌더 (page_size 2 → 페이지 1/2 표시) |
| T41 | section에 expand:true | ✅ 수락 (AI 앱 전용 속성이나 일반 메시지에서 거부되지 않음) |
| T42 | markdown 인라인 문법 위치 프로브 6종 (문장 중간 **, ~~, 물음표 포함 등) | ✅ 전부 올바르게 파싱·렌더 |

## 한계·동작

| ID | 시험 내용 | 결과 |
|---|---|---|
| T16 | section text 3001자 | ❌ `must be less than 3001 characters` |
| T16b | section text 3000자 | ✅ 수락·렌더 |
| T17 | 블록 51개 | ❌ `no more than 50 items allowed` |
| T17b | 블록 50개 | ✅ 수락·렌더 |
| T18 | header 151자 | ❌ 거부. **거부된 메시지는 저장되지 않음**(API 조회 부재). 단 데스크톱 클라이언트가 잠시 유령 렌더 |
| T19 | top-level text 4,024자 | ✅ 수락·**저장 4,024자 온전**(40,000자 한도와 일치) |
| T25 | filesUploadV2 python 스니펫 (thread_ts 지정) | ✅ 업로드·프리뷰 렌더 |
| T26 | chat.update로 진행→완료 교체 | ✅ 갱신 확인 |
| T28 | chat.postEphemeral (유저 토큰) | ❌ `not_allowed_token_type` — 봇 토큰 필요 |
| T29 | GitHub 링크 + unfurl_links:true | ✅ 게시 / ⚠️ **언펄 없음**(GitHub 앱 미설치) |
| T39 | chat.startStream (유저 토큰) | ❌ `not_allowed_token_type` — 봇 토큰 필요 |

## 봇 토큰(xoxb) 리치 컨트롤·데이터 블록

| ID | 시험 내용 | 결과 |
|---|---|---|
| T43 | button + static_select + overflow in actions | ✅ 수락·저장 (`header`, `actions`) |
| T44 | datepicker + timepicker + datetimepicker in actions | ✅ 수락·저장 (`header`, `actions`) |
| T45 | multi_static_select section accessory + radio_buttons + checkboxes | ✅ 수락·저장 (`header`, `section`, `actions`) |
| T46 | users_select + conversations_select + channels_select | ✅ 수락·저장 (`header`, `actions`) |
| T47 | message input: plain_text_input + email_text_input + url_text_input | ✅ 수락·저장 (`header`, `input` ×3) |
| T48 | native table | ✅ 수락·저장 (`header`, `table`) |
| T49 | data_visualization pie + plan 및 T43~T49 종합 11-block payload | ✅ 수락·저장. 종합 payload도 정확히 11개 block type으로 readback |

## 핵심 교훈 (에이전트용 요약)

1. **`invalid_blocks` = 전체 미게시.** 부분 성공 없음. API 응답만 믿을 것(유령 렌더 존재).
2. **container 블록이 네이티브 접기다.** 접힌 목록 요구에는 이것이 정답(2026-06-29~).
3. **LLM 출력은 markdown 블록에 그대로.** 서버가 CommonMark를 정확히 rich_text로 변환한다.
4. **multi-select는 section accessory로.** actions 블록은 유저 토큰에서 거부.
5. **plan/task_card title은 문자열.** text 객체 아님.
6. **icon_button은 text 필수.** 문서보다 실측이 강하다.
7. **ephemeral·스트리밍은 봇 토큰 필요.**
8. **data_table 셀은 raw_text로.** raw_number는 유저 토큰에서 거부됨(문서와 충돌).
9. **외부 이미지 URL은 깨질 수 있다.** 파일 업로드가 안전.
10. **폴 스트링 text는 항상.** 알림/검색/저장 실패 분석의 기준.
11. **xoxb에서는 multi-select를 section accessory로 사용하면 안전하다.** 메시지 input의 email/url도 게시·저장됐다.
12. **렌더 성공과 동작 성공을 구분한다.** T43~T49는 게시·저장 검증이며 임의 action_id 클릭 처리는 별도 interactivity 백엔드가 필요하다.

## 렌더 증거 공개 정책

원본 렌더 캡처에는 개인 DM·워크스페이스 식별 정보가 포함될 수 있어 공개 플러그인 패키지에서 제외한다. T01~T42의 텍스트 결과, API 오류 원문, 검증 등급은 이 매트릭스에 유지한다.
