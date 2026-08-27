# Payloads — 복사용 페이로드 색인

> 사용법: `channel`을 채우고 `chat.postMessage`에 그대로 전달. 모든 파일은 JSON 유효성 검사 완료.
> `text`(폴 스트링)는 알림/검색용으로 항상 유지할 것. 검증 환경: 2026-08-24 유저 토큰 + 2026-08-27 봇 토큰.

| 파일 | 패턴 | 대응 케이스 | 검증 |
|---|---|---|---|
| `approval-card.json` | 승인 카드 (fields+primary/danger+confirm+URL) | 01 승인 | [실측 ✅ T03 T06 T27 조합] |
| `choice-select.json` | static_select + overflow | 02 선택 | [실측 ✅ T07] |
| `collapsed-container.json` | container 접힌 목록 + 요약 | 05 접기 | [실측 ✅ T30 구조 확장 — 확장 페이로드 자체는 미게시, 구성 요소 전부 실측] |
| `table-basic.json` | table 정적 표 | 07 표 | [실측 ✅ T14와 동형] |
| `data-table-paginated.json` | data_table 페이지네이션 | 07 표 | [실측 ✅ T40d와 동형] |
| `progress-update.json` | chat.postMessage→chat.update 2단계 | 06 진행 | [실측 ✅ T26] |
| `plan-tasks.json` | plan + task_card | 06 진행 | [실측 ✅ T35b T36b] |
| `feedback-buttons.json` | context_actions 피드백 + AI 디스클레이머 | 11 피드백 | [실측 ✅ T38b + markdown 블록 T37] |
| `data-viz-pie.json` | data_visualization 파이 | 07 차트 | [실측 ✅ T31] |
| `markdown-llm-output.json` | markdown 블록 (CommonMark) | 04/07 전반 | [실측 ✅ T37] |
| `snippet-upload.js` | filesUploadV2 스니펫 | 03 산출물 | [실측 ✅ T25] |
| `rich-controls-message.json` | 버튼·콤보박스·날짜/시간·복수선택·대상선택·입력·표·차트 종합 | 02/07/09 | [xoxb 실측 ✅ T43~T49 정확 조합] |

## 주의

- **인터랙티브 페이로드**(버튼/셀렉트/피드백)는 렌더만 검증됐다. 클릭 처리는 앱 백엔드(interactivity) 필요 — `references/reference/surfaces-tokens.md`.
- `collapsed-container.json`은 실측 T30을 확장한 합성 페이로드다. 구성 요소(container 접기, rich_text_list, context)는 전부 개별 실측됐지만 이 정확한 조합의 게시는 하지 않았다 — `[미검증 조합]` 표시에 유의.
- multi-select가 필요하면 **actions가 아니라 section accessory**에 넣는다 (유저 토큰 실측) — `references/cases/02-choice-selection.md`.
