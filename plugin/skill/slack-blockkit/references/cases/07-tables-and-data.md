# 07. 표와 차트 (Tables & Data)

## 언제 쓰는가

행×열 구조 데이터(검색 결과, 상태 목록, 지표 비교)나 차트(비율, 추이)를 보여줄 때. **mrkdwn에는 표 문법이 없다** — 아래 수단을 쓴다.

## 수단 선택표

| 데이터 | 수단 | 제한 | 검증 |
|---|---|---|---|
| 소규모 키-값 (4~10개) | section `fields` (2열 그리드) | fields ≤10, 각 2000자 | [실측 ✅ T03] |
| 정적 표 (결과 목록) | **`table` 블록** (2025-08-14~) | 행 ≤100, 열 ≤20, 셀 합산 10,000자 | [실측 ✅ T14] |
| 대형 표 (페이지네이션/정렬) | **`data_table` 블록** (2026-05-20~) | 행 2~201, 열 1~20, 셀 합산 20,000자, page_size ≤100 | [실측 ✅ T40d] |
| 비율/추이 차트 | **`data_visualization` 블록** (2026-06-16~) | 메시지당 2개, 시리즈 1~12, 데이터포인트 시리즈당 1~20 | [실측 ✅ T31] |
| LLM이 만든 마크다운 표 | `markdown` 블록 내 `\|` 표 문법 | 합산 12,000자 | [실측 ✅ T37] |

## 권장 형태

### A. table 블록 (정적 표의 기본)

```json
{ "type": "table", "rows": [
  [ {"type":"raw_text","text":"서비스"}, {"type":"raw_text","text":"상태"} ],
  [ {"type":"raw_text","text":"api"},  {"type":"rich_text","elements":[{"type":"rich_text_section","elements":[{"type":"text","text":"정상","style":{"bold":true}}]}]} ]
]}
```

- 첫 행이 헤더로 렌더된다 `[실측 ✅ T14]`.
- 셀 타입: `raw_text` / `raw_number` / `rich_text` `[문서]`. table에서는 raw_number가 유효 `[문서]`(미실측).
- `column_settings`로 열 정렬(left/center/right)·래핑 제어 `[문서]`.
- Modals에서는 사용 불가(Messages/Home만) `[문서]`.
- 페이로드: `references/payloads/table-basic.json`

### B. data_table 블록 (크고 페이지네이션 필요할 때)

- `caption` 필수, `page_size`(기본 5, 최대 100)로 페이지네이션. 실측에서 page_size 2로 페이지 1/2 렌더 확인 `[실측 ✅ T40d]`.
- **실측 주의**: `raw_number` 셀이 메시지 게시에서 거부됨(`raw_text`는 성공) `[실측 ✅ T40b/T40c 실패 → T40d 성공]`. 문서는 헤더 행에 raw_text/raw_number를 명시하나 실측과 충돌 — **모든 셀을 raw_text로 본내는 것이 안전**(유저 토큰 기준).
- `columns` 같은 속성은 없다 — 첫 행이 곧 헤더 `[실측 ✅ T40 — "invalid additional property: columns"]`.
- 정렬/필터 인터랙션 동작은 `[미검증]`(렌더·페이지네이션만 실측).
- 페이로드: `references/payloads/data-table-paginated.json`

### C. data_visualization 블록 (차트)

- pie/bar/area/line. 실측 파이 차트 렌더 확인: `{ "type":"data_visualization", "title":"…", "chart":{ "type":"pie", "segments":[{"label":"성공","value":42}, …] } }` `[실측 ✅ T31]`.
- 제한: 메시지당 2개, title 50자, pie 세그먼트 1~12(label 20자, value>0), bar/area/line은 series 1~12·series당 data 1~20개 `[문서]`.
- bar/line/area의 정확한 페이로드 스키마는 `[미검증]` — pie만 실측. 페이로드: `references/payloads/data-viz-pie.json`

### D. markdown 표 (LLM 출력 그대로)

LLM이 `| a | b |` 형식으로 만든 표는 `markdown` 블록에 넣으면 서버가 실제 표 rich_text로 변환해 렌더한다 `[실측 ✅ T37]`. 수동으로 table 블록 JSON을 짜는 것보다 LLM 출력에 그대로 쓰기 좋다.

## 스레드 동작

- 표가 크면(행 20+) 부모에는 상위 N행 표 + "전체는 스레드/스니펫" 안내. data_table 페이지네이션이 있어도 메시지가 세로로 길어지는 것은 같다.
- 갱신되는 지표 표는 `chat.update`로 같은 메시지를 갱신 — 새 표를 연속 게시하면 스캔이 어렵다.

## 주의점

- **셀 합산 문자 제한**이 진짜 한계다: table 10,000자/메시지, data_table 20,000자/메시지 `[문서]`. 큰 표는 메시지를 나눈다.
- 2025년 이전의 "등폭 코드블록 표" 핵은 더 이상 쓰지 않는다(가독성 나쁨). 레거시 호환용으로만.
- fields 2열은 모바일에서 1열로 바뀐다 — 순서 의존 데이터는 fields 대신 table 권장 `[미검증 — 모바일 렌더 미실측]`.

## 검증 상태

- table / data_table / data_visualization(pie) / markdown 표 / fields: 전부 `[실측 ✅ T03, T14, T31, T37, T40d]`
- bar/line/area 차트, raw_number 셀(table), 정렬·필터: `[미검증]`

## 출처

- table 블록: https://docs.slack.dev/reference/block-kit/blocks/table-block , https://docs.slack.dev/changelog/2025/08/14/block-kit-table-block
- data_table 블록: https://docs.slack.dev/reference/block-kit/blocks/data-table-block , https://docs.slack.dev/changelog/2026/05/20/block-kit-more-new-blocks
- data_visualization 블록: https://docs.slack.dev/reference/block-kit/blocks/data-visualization-block , https://docs.slack.dev/changelog/2026/06/16/block-kit-data-visualization-block
- 실측: `references/verified-matrix.md` T03, T14, T31, T37, T40, T40b~T40d
