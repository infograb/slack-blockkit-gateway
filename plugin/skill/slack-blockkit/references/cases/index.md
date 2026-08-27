# Cases — 상황별 패턴 인덱스

에이전트가 사람에게 메시지를 본낼 때 마주치는 상황 12종. 각 파일은 같은 구조를 따른다:
**언제 쓰는가 → 권장 형태(기본 패턴) → 스레드 동작 → 페이로드 → 대안 패턴 → 주의점 → 검증 상태 → 출처**

## 선택 매트릭스

| 하고 싶은 것 | 가는 곳 | 기본 블록/수단 | 검증 |
|---|---|---|---|
| "이거 승인/진행/중단" 결정 받기 | `01-approval-decision.md` | actions + primary/danger 버튼 + confirm | [실측 ✅] |
| 옵션 3~100개 중 선택 | `02-choice-selection.md` | static_select (≤100), radio (≤10), overflow (≤5) | [실측 ✅] |
| 코드/문서/이미지 산출물 보여주기 | `03-artifact-preview.md` | filesUploadV2 스니펫, image, URL 버튼 | [실측 ✅] |
| 링크·출처 달기 | `04-links-citations.md` | `<url\|text>` 인라인 + context 푸터 | [실측 ✅] |
| 긴 목록/로그 접어서 보여주기 | `05-collapsed-long-content.md` | **container 블록** (네이티브 접기, 2026-06~) | [실측 ✅] |
| "하는 중… → 완료" 상태 표시 | `06-progress-and-streaming.md` | chat.update, plan/task_card | [실측 ✅] |
| LLM 출력 실시간 타이핑 | `06-progress-and-streaming.md` | chat.*Stream (봇 토큰 필요) | [실측 ✅ — 유저 토큰 실패 확인] |
| 표 형태 데이터 | `07-tables-and-data.md` | table (정적), data_table (페이지네이션) | [실측 ✅] |
| 차트 | `07-tables-and-data.md` | data_visualization (pie/bar/line/area) | [실측 ✅] |
| 실패 보고 + 복구 유도 | `08-error-and-fallback.md` | section + 복구 버튼 | [실측 ✅] |
| 여러 값 입력받기 | `09-collecting-input.md` | input 블록 / 모달 views | [실측 ✅ / 모달은 문서] |
| 공지·멘션 | `10-notifications-mentions.md` | header + context, 멘션 문법 | [실측 ✅] |
| 답변 평가 받기 | `11-feedback-loop.md` | context_actions + feedback_buttons | [실측 ✅] |
| 채널 vs 스레드 vs DM vs ephemeral | `12-thread-and-surface-strategy.md` | thread_ts, DM, ephemeral(봇) | [실측 ✅] |

## 케이스 목록

1. [01 승인/거절 결정 받기](01-approval-decision.md) — 근거 팩 + 버튼 + confirm + 결정 후 카드 갱신
2. [02 선택지 제시](02-choice-selection.md) — 셀렉트/오버플로/라디오/체크박스 선택 기준
3. [03 산출물 미리보기](03-artifact-preview.md) — 스니펫·파일·이미지·언펄·외부 링크 버튼
4. [04 링크와 출처](04-links-citations.md) — 인라인 링크, 인용 푸터, 언펄 제어
5. [05 긴 목록·긴 텍스트 접기](05-collapsed-long-content.md) — container 네이티브 접기 + 대안 7종
6. [06 진행 상태와 스트리밍](06-progress-and-streaming.md) — chat.update, plan/task_card, setStatus, Stream API
7. [07 표와 차트](07-tables-and-data.md) — table / data_table / data_visualization / fields
8. [08 에러 보고와 폴 스트링](08-error-and-fallback.md) — 실패 카드, 복구 옵션, 금지 사항
9. [09 사용자 입력 수집](09-collecting-input.md) — input 블록, 모달, dispatch_action
10. [10 알림과 멘션](10-notifications-mentions.md) — 헤더 우선 구조, 멘션 문법, 다이제스트
11. [11 피드백 수집](11-feedback-loop.md) — feedback_buttons, icon_button, reacji
12. [12 스레드와 서피스 전략](12-thread-and-surface-strategy.md) — 채널/스레드/DM/ephemeral/모달/Home 배치 기준
