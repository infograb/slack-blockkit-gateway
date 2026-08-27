# 12. 스레드와 서피스 전략 (Where to Post)

## 언제 쓰는가

메시지를 **어디에** 올릴지가 가독성의 절반이다. 채널 / 스레드 답글 / DM / ephemeral / 모달 / App Home 중 고르는 기준.

## 배치 결정표

| 상황 | 가는 곳 | 이유 | 검증 |
|---|---|---|---|
| 모두가 알아야 할 결과·공지 | 채널 부모 메시지 | 가시성 | [실측 ✅] |
| 요청에 대한 답변·진행·에러 | **스레드 답글** | 채널 스캔 유지. 스트리밍도 답글이 원칙 | [문서 + 실측 ✅] |
| 긴 상세 (전체 목록, 로그) | 스레드 답글 or container 접기 | `05` 케이스 | [실측 ✅] |
| 개인에게만 필요한 승인·입력 요청 | DM | 프라이버시, 알림 확실 | [문서 — HumanLayer 기본값] |
| 요청한 사람에게만 보여야 할 일시 정보 | ephemeral | **봇 토큰 필수** — 유저 토큰은 실패 | [실측 ✅ T28] |
| 정형 폼 입력 | 모달 | 제출 시점 명확, 필드 검증 | [문서] |
| 스크롤 가능한 긴 목록·개인 대시보드 | App Home | 100블록, 페이지네이션 | [문서] |

## 스레드 사용 규칙 (핵심)

1. **부모 = 요약 + 행동 요소** (결론, 버튼, 대표 항목). **답글 = 상세** (전체 목록, 로그, 근거, 후속 Q&A).
2. 에이전트 응답은 항상 **요청이 발생한 스레드 안**에 둔다 — Sourcegraph(후속 Q&A), LangSmith Fleet(에러), PagerDuty(활동 로그) 모두 같은 패턴 `[문서]`.
3. 채널에서 @멘션으로 시작된 대화는 스레드로 이어지게 한다. 채널 메인에 연속 게시하는 것은 안티패턴.
4. `broadcast`(답글을 채널에도)는 정말 중요한 최종 결과 1건에만.
5. 스레드 부모가 업데이트되면(`chat.update`) 스레드 요약도 맞춘다.

## ephemeral (나에게만 보임)

- 호출한 사람에게만 보이는 일시 메시지. 새로고침하면 사라진다 `[문서]`.
- **유저 토큰(xoxc)으로는 `not_allowed_token_type`으로 실패 — 봇 토큰 필수** `[실측 ✅ T28]`.
- 용도: 채널을 더럽히지 않는 확인("승인이 접수됐습니다"), 개인별 안내, 민감하지 않은 일시 정보.
- Slack 스태프의 대용량 사본 패턴: 채널에는 ephemeral로 짧게 알리고 실제 파일/분석은 앱 DM으로 `[문서 — bolt-js#1030]`.

## Agents 기능의 전용 서피스 (참고)

- Agents & AI Apps 기능을 켠 앱은 **split-view 패널, 세션 사이드바, suggested prompts, 상태줄** 등 전용 UI를 얻는다 `[문서]`. 유료 플랜 필요, 게스트 사용 불가 `[문서]`.
- `assistant_view`는 2027-02 deprecation 예정, 신규는 `agent_view` `[문서 — 2026-08-20 changelog]`.
- 자체 에이전트를 정식 Slack AI 앱으로 만들지, 단순 봇으로 둘지의 분기점이다. 단순 봇이면 이 볼트의 메시지 패턴이 전부다.

## 주의점

- 스레드 답글은 채널 멤버에게 알림이 가지 않는다(참여자·멘션 대상 제외) — 중요한 최종 결과는 부모 갱신 + 필요시 채널 게시.
- DM은 검색·감사에서 채널보다 불리하다. 승인 감사가 필요하면 채널+스레드 `[문서 — Wrangle]`.
- Slack Connect 채널·게스트는 앱 기능 제한이 있다 `[문서]`.

## 검증 상태

- 스레드 답글 게시·파일 스레드 업로드·ephemeral 실패: `[실측 ✅ T25, T28]`
- 모달/App Home/Agents 서피스: `[문서]` (미실측)

## 출처

- 스트리밍은 답글 원칙: https://docs.slack.dev/changelog/2025/10/7/chat-streaming
- 에이전트 디자인(스레드 응답·알림 배치): https://docs.slack.dev/concepts/agent-design
- agent_view: https://docs.slack.dev/changelog/2026/06/30/agent-messages-tab , https://docs.slack.dev/changelog/2026/08/20/agent-updates
- ephemeral 대용량 패턴: https://github.com/slackapi/bolt-js/issues/1030
- 실측: `references/verified-matrix.md` T25, T28
