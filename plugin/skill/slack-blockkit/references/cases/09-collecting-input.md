# 09. 사용자 입력 수집 (Collecting Input)

## 언제 쓰는가

단순 선택이 아니라 사람이 텍스트·날짜·파일 등을 입력해야 할 때. 배포 사유 작성, 일정 지정, 피드백 문장 수집 등.

## 권장 형태

### A. 메시지 안 input 블록 (간단한 1~2개 입력)

실측으로 **input 블록이 일반 메시지에서도 렌더됨을 확인**했다 `[실측 ✅ T12 — plain_text_input, 라벨+입력창 렌더]`. 현행 문서도 input 블록의 surface에 Messages 포함 `[문서]`. (구 문서·구 SDK 상식 "input은 모달 전용"은 더 이상 아니다.)

- 사용 가능 입력: `plain_text_input`(multiline 가능, min/max_length ≤3000), datepicker/timepicker/datetimepicker, 셀렉트류, radio, checkboxes `[문서]` `[실측 ✅ T10, T11, T12]`.
- **Modals 전용 입력**: `email_text_input`, `url_text_input`, `number_input`, `file_input` `[문서]`.
- `rich_text_input`은 Messages에서 사용 불가(Modals/Home) `[문서]`.

### B. 모달 (정형 폼, 3개+ 입력)

- 버튼/단축키 → `views.open`으로 모달. input 블록 100개까지, 제출은 `view_submission`, 필드별 인라인 에러 반납 가능 `[문서]`.
- 모달이 정석인 이유: **제출 버튼이 있어 입력 확정 시점이 명확**하고, 검증 에러를 필드 옆에 표시할 수 있다.
- incident.io는 70+ 모달을 운영하며 입력 6개 이상이면 페이지네이션하라고 권장 `[문서 — incident.io, Slack 모달 가이드]`.
- **앱 백엔드 필수** (views.open 트리거, view_submission 수신).

### C. 자유 텍스트 답글 (가장 간단)

"이 스레드에 사유를 답글로 남겨 주세요" — HumanLayer가 프로덕션에서 병행하는 패턴 `[문서]`. 앱이 message 이벤트를 구독하면 된다. 구조화는 못 하지만 마찰이 가장 적다.

## 스레드 동작

- 입력 요청은 부모(또는 DM), 입력 결과 확인은 `chat.update`로 요청 카드를 갱신("사유 등록됨 ✅").
- 입력값이 민감하면 DM/ephemeral로 (`12` 케이스). **비밀번호·토큰은 절대 받지 않는다** `[문서 — Slack 모달 가이드]`.

## 주의점

- input 블록 `label`/`hint` 각 2000자, `optional: true`로 선택 입력화 `[문서]`.
- 메시지 안 input에서 값 변경 이벤트를 받으려면 `dispatch_action` 설정이 필요하고, file_input과 병용 불가 `[문서]`.
- `dispatch_action_config`: `on_enter_pressed` / `on_character_entered` — 입력 중에도 페이로드 발송 `[문서]`.
- datetimepicker는 Home tab 미지원 `[문서]`.
- 모달 title/close/submit은 각 24자 제한 `[문서]`.

## 검증 상태

- 메시지 내 input/plain_text_input/datepicker 계열: `[실측 ✅ T10, T12]`
- 모달 라이프사이클: `[문서]` (앱 필요, 미실측)

## 출처

- input 블록: https://docs.slack.dev/reference/block-kit/blocks/input-block
- 모달 가이드: https://docs.slack.dev/surfaces/modals
- incident.io 모달 운영: https://incident.io/blog/slack-previews
- 실측: `references/verified-matrix.md` T10, T12
