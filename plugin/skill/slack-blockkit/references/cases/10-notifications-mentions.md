# 10. 알림과 멘션 (Notifications & Mentions)

## 언제 쓰는가

결정이 필요 없는 단방향 통지 — 작업 완료, 배포 결과, 주간 리포트, 모니터링 이벤트. 사람이 3초 안에 "나와 관계있나, 뭘 하면 되나"를 판단하게 하는 것이 목표.

## 권장 형태 (헤더 우선 구조)

```
header:   🚀 배포 완료 — api-server v2.3.1        ← 스캔의 기준점
section:  핵심 한두 문장 (무엇이, 어디에, 결과는)
section:  fields = [환경 prod, 소요 3분, 커밋 14, 롤백 가능]
actions:  [ 리포트 열기(url) ]                      ← 예측 가능한 다음 액션 1개
context:  deploy-agent • <!date^…^{time}> • run-123
```

- **header는 plain_text만, 150자** `[실측 ✅ T18 — 151자 거부]`. 이모지로 종류를 구분(🚀 배포, ⚠️ 경고, 📊 리포트).
- Knock의 알림 디자인 분석도 "header → divider → 이모지 구분 리스트 → 명확한 버튼" 구조를 권장 `[문서 — Knock]`.
- 버튼은 예측 가능한 액션이 있을 때만. 모든 알림에 버튼을 달면 오히려 무거워진다(Beep Boop 교훈) `[문서 — Slack 개발자 블로그]`.

## 멘션 문법 (mrkdwn)

| 대상 | 문법 | 검증 |
|---|---|---|
| 특정 사용자 | `<@U012AB3CD>` | [문서] |
| 채널 참조 | `<#C01234567>` | [문서] |
| 온라인 사람만 | `<!here>` | [실측 ✅ T01 — 렌더 확인] |
| 채널 전원 | `<!channel>` | [문서] |
| 워크스페이스 전원 | `<!everyone>` | [문서] |
| 그룹 | `<!subteam^SAZ94GDB8>` | [문서] |
| 날짜/시간 | `<!date^epoch^{date_short_pretty}^링크\|폴 스트링>` — 수신자 기기 타임존으로 표시 | [문서] |

- `<!here>`/`<!channel>` 남용 금지 — 알림 피로의 주범. "정말 지금 깨울 일인가" 기준 `[문서 — Slack app-design]`.
- top-level text의 자동 멘션 파싱(link_names) 방식은 deprecated — 위 문법을 명시 사용 `[문서]`.

## 다이제스트 (알림이 잦을 때)

- 이벤트를 실시간으로 1건씩 본내지 말고 **주기적으로 묶어 1메시지**로. Slack 공식 앱 디자인 가이드 권장 `[문서 — app-design]`.
- 다이제스트는 table 또는 container 접기와 궁합이 좋다 (`05`, `07` 케이스).

## 스레드 동작

- 같은 주제의 후속 알림은 첫 알림의 스레드 답글로 묶는다 (채널 스캔 유지).
- 중요도가 낮으면 부모 갱신(`chat.update`)으로 최신 상태 하나만 유지.

## 주의점

- AI가 생성·발송하는 자율 콘텐츠에는 **"AI 생성" 표시와 on-behalf-of 라벨**을 context에 단다 `[문서 — Slack agent-design]`.
- 알림 폭주는 곧 뮤트다. 발송 기준을 사용자가 조절할 수 있게(채널/빈도 선택) 설계 `[문서 — app-design]`.

## 검증 상태

- header/divider/context/fields/버튼 조합: `[실측 ✅ T02, T03, T06]`
- 멘션 렌더: `<!here>` `[실측 ✅ T01]`, 나머지 문법 `[문서]`

## 출처

- 메시지 포맷팅(멘션·날짜): https://docs.slack.dev/messaging/formatting-message-text
- 알림 디자인: https://knock.app/blog/the-guide-to-designing-slack-notifications
- Slack 앱 디자인(다이제스트·버튼 절제): https://docs.slack.dev/concepts/app-design
- Beep Boop 교훈: https://medium.com/slack-developer-blog/lessons-learned-from-beep-boops-new-slack-bot-bd250e8d9887
- 에이전트 디자인 원칙: https://docs.slack.dev/concepts/agent-design
- 실측: `references/verified-matrix.md` T01, T02, T03, T06, T18
