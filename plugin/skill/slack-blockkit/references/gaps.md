# 갭 목록 (미검증·미조사 영역)

> 수집 정지 조건: 3개 조사 축(공식 문서 전수 / AI 에이전트 기능 / 프로덕션 패턴 15+ 소스)과 42건 실측 후 신규 패턴 포화.
> 아래는 **알고 있지만 검증하지 못한 것**과 **조사가 부족한 영역**. 지어내서 채우지 말고, 검증하면 본문으로 승격한다.

## A. 실행 환경 한계로 미검증

| # | 항목 | 왜 못 했나 | 검증 방법 |
|---|---|---|---|
| A1 | **봇 토큰(xoxb)의 나머지 블록 동작** — controls/date/input/table/data_visualization/plan은 T43~T49로 승격, carousel/card/task_card 직접 post가 잔여 | 일부 신형 블록 미시험 | 잔여 블록을 동일 xoxb 환경에서 분리 시험 |
| A2 | **ephemeral / 스트리밍(chat.*Stream) 실제 동작** | 유저 토큰 `not_allowed_token_type` 확인만 | 봇 토큰 + interactivity 앱 |
| A3 | **버튼·셀렉트·피드백 클릭 페이로드(block_actions) 수신** | interactivity 백엔드 부재 | Socket Mode 앱으로 클릭 시험 |
| A4 | **confirm 다이얼로그 실제 표시** | 클릭 플로우 필요 | A3과 함께 |
| A5 | **모달(views.open/view_submission), App Home** | 앱 필요 | 앱 + trigger |
| A6 | **모바일 클라이언트 렌더** (fields 2열→1열, container 접기, table 가로 스크롤) | 데스크톱만 시험 | iOS/Android 앱에서 동일 스레드 열기 |
| A7 | **alert / carousel 블록 게시** | 미시험 (alert는 Modals only) | carousel은 메시지로 시험 가능 |
| A8 | **data_visualization bar/line/area 스키마** | pie만 실측 | 동일 방식으로 시험 |
| A9 | **table 블록의 raw_number 셀** (data_table과 달리 되는지) | 미시험 | T14 변형 시험 |
| A10 | **markdown 블록에서 멘션(<@U>, <!here>)·날짜 토큰 동작** | 미시험 | T37 변형 |
| A11 | **Hermes `slack-blockkit-gateway`의 Task Card 재시작 후 스트리밍** — 일반 rich_blocks xoxb 게시·저장은 완료 | long-lived Gateway가 core 수정 전 코드일 수 있음 | 외부 Gateway 재시작 후 appendStream 오류·fallback 로그 재검사 |

## B. 문서만 있고 실측·사례가 약한 영역

| # | 항목 | 상태 |
|---|---|---|
| B1 | **Slack Code** (2026-08-20 발표 — 에이전트가 코드 diff/HTML 프리뷰/캔버스 아티팩트 게시) | 발표만 있고 개발자 API 상세 미공개 `[미검증]` |
| B2 | **서드파티 앱의 캔버스(canvas) 생성 API GA 여부** | 접근 제한/allowlist 관측 — 공식 확인 필요 |
| B3 | **Work Objects / 커스텀 언펄(chat.unfurl) + flexpane 상세** | Sourcegraph 사례만, 일반화 검증 없음 |
| B4 | **data_table 정렬·필터 인터랙션 동작 조건** | 페이지네이션만 실측 |
| B5 | **plan 블록 task status 완전 enum** (문서 2곳 표기 상이) | pending/in_progress/complete 렌더 실측, error는 미실측 |
| B6 | **section `expand` 자동 접힘의 클라이언트 임계값** | 공식 임계값 없음, 클라이언트 결정 |
| B7 | **suggested prompt title 75자 제한** | 서드파티 강의에만 있음, 공식 문서 미확인 |
| B8 | **container 블록 중첩(container 안 container) 가능 여부** | 미시험 — 문서상 child_blocks에 container 미명시 |
| B9 | **message metadata(approval 스키마)의 Activity feed 표시** | 문서만, 실사용 사례 미수집 |
| B10 | **봇 게시 링크의 자동 언펄 조건** (2020년 SO "봇은 언펄 안 함"이 2026년에도 유효한지) | T29는 유저 토큰+미설치 앱 — 조건 분리 못 함 |

## C. 조사 포화 판단 근거 (왜 멈췄나)

- 공식 블록 20종·요소 30+종 전수 카탈로그화 완료, 2026-08 changelog까지 추적.
- 커뮤니티 패턴 수집이 A1(승인 카드) 이후 신규 패턴 수확 급감 — HumanLayer/LangSmith/n8n/Wrangle/StackAI/Sourcegraph/PagerDuty/incident.io/Sleuth/CircleCI 계열이 전부 동일 패턴군(승인 카드, 근거 팩, 스레드 상세, 스니펫, reacji)으로 수렴.
- 2026년 신형 블록(container/plan/task_card/data_*/alert/card/carousel)은 실측을 우선했고 문서 조사는 changelog 원문까지 도달.
- 잔여 갭은 대부분 "앱(봇 토큰)이 있어야 검증 가능"한 영역으로 수렴 → 환경 갭(A군)으로 정리.
