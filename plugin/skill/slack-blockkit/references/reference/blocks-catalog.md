# 블록 카탈로그 (20종, 2026-08 기준)

> 표면(Surface): M=Messages, V=Modals(views), H=App Home. 검증 열은 이 볼트의 실측 여부.
> 전량 docs.slack.dev 정본 기준 `[문서]`, 실측 표시는 유저 토큰 결과.

## 레이아웃·텍스트 계열

| 블록 | 용도 | Surface | 핵심 제한 | 실측 |
|---|---|---|---|---|
| `section` | 텍스트+accessory의 기본 단위 | M V H | text 3000자, fields 10×2000자, `expand` 속성(AI 장문) | ✅ T01 T03 T41 |
| `header` | 큰 제목 | M V H | plain_text 150자, level 1~4 | ✅ T02 T18 |
| `divider` | 수평선 | M V H | 없음 | ✅ T02 |
| `context` | 작은 회색 보조 텍스트 | M V H | elements 10 (image+text) | ✅ T02 |
| `rich_text` | WYSIWYG 서식 (리스트/인용/코드) | M V H | 하위 요소 조합 | ✅ T05 |
| `markdown` | **CommonMark 입력 → 서버가 rich_text 변환** | M만 | 합산 12,000자, block_id 무시 | ✅ T13 T37 T42 |
| `input` | 라벨 붙은 입력 | M V H | label/hint 2000자 | ✅ T12 |
| `container` | **접기 가능한 그룹 래퍼** (2026-06-29) | M H | title 150, child 10, is_collapsible/default_collapsed | ✅ T30 |
| `file` | 리모트 파일 표시 | M만 | **앱이 직접 게시 불가** (조회 전용) | — |

## 미디어·데이터 계열

| 블록 | 용도 | Surface | 핵심 제한 | 실측 |
|---|---|---|---|---|
| `image` | 단독 이미지 | M V H | url 3000자, alt 2000자 | ✅ T04 (외부 URL 실패 사례) |
| `video` | 임베디드 비디오 | M V H | links.embed:write + 도메인 등록 | ❌ T15 스코프 부재 |
| `table` | 정적 표 (2025-08-14) | M H | 100×20, 셀 합산 10,000자 | ✅ T14 |
| `data_table` | 페이지네이션 표 (2026-05-20) | M H | 201행, 20,000자, caption 필수 | ✅ T40d |
| `data_visualization` | pie/bar/area/line (2026-06-16) | M만 | 메시지당 2개 | ✅ T31 (pie) |
| `card` | 카드 콘텐츠 (2026-04-16) | M V H | title 150, body 200, 버튼 3 | ✅ T32 |
| `carousel` | 카드 가로 스크롤 (2026-04-16) | M H | 카드 1~10 | 미실측 |

## 인터랙션·에이전트 계열

| 블록 | 용도 | Surface | 핵심 제한 | 실측 |
|---|---|---|---|---|
| `actions` | 인터랙티브 요소 컨테이너 | M V H | elements 25 | ✅ T06~T11 T20~T23 |
| `context_actions` | 피드백/아이콘 버튼 행 | M만 | elements 5 | ✅ T38b |
| `alert` | 레벨 있는 배너 (2026-04-16) | **V만** | text 200 | 미실측 |
| `plan` | 작업 체크리스트 (2026-02-11) | M만 | tasks 50, title 문자열 | ✅ T35b |
| `task_card` | 단일 작업 카드 (2026-02-11) | M만 | title 문자열, status 3종 | ✅ T36b |

## 신규 블록 타임라인 (공식 changelog)

| 날짜 | 블록 |
|---|---|
| 2023-09-29 | rich_text (surface 개방) |
| 2025-02-03 | **markdown** |
| 2025-08-14 | **table** |
| 2026-02-11 | **plan, task_card** |
| 2026-03-06 | rich text 확장(구문강조·표·task list·구분선·가변 헤더) |
| 2026-04-16 | **alert, card, carousel** + 스트림 내 블록 청크 |
| 2026-05-20 | **data_table** |
| 2026-06-16 | **data_visualization** |
| 2026-06-29 | **container** |

## 문서 vs 실측 충돌 기록 (중요)

1. **input 블록**: 구 문서 기준 "Modals 전용"으로 알려졌으나 현행 문서는 Messages 포함, 실측도 렌더됨 → **메시지 사용 가능** ✅
2. **multi-select in actions**: 문서는 호환으로 표기, 유저 토큰 실측은 `unsupported element: multiselect` 거부 → **section accessory 사용** ✅
3. **data_table raw_number 셀**: 문서 명시 있으나 유저 토큰 메시지에서 거부 → **raw_text 사용** ✅
4. **plan/task_card title**: 문서 예시가 plain text 객체처럼 보이나 실제로는 **문자열**이어야 함 ✅
5. **icon_button**: 문서상 text 언급이 약하나 실제로는 **text 필수** ✅
6. **overflow 하한**: 구 문서 "2~5개", 현행 문서 "up to five", 실측 1개 수락 ✅

## 출처

- 블록 레퍼런스 총괄: https://docs.slack.dev/reference/block-kit/blocks/
- changelog: https://docs.slack.dev/changelog
