# 08. 에러 보고와 폴 스트링 (Error Reporting & Fallback)

## 언제 쓰는가

작업 실패, 도구/API 오류, 부분 성공, 타임아웃 — 에이전트가 멈췄을 때 사람에게 알릴 때. **최악은 조용히 멈추는 것**(로딩 상태가 영원히 도는 것)이다 `[문서 — developing-agents]`.

## 권장 형태 (실패 카드)

```
section:  :x: *배포 실패* — api-server v2.3.1
section:  fields = [실패 단계: 테스트, 원인: 3건 타임아웃, 진행분: 빌드까지 완료]
section:  ```또는 container에 핵심 로그 10줄 (전체는 스니펫)
actions:  [ 재시도(primary) ] [ 로그 전체(url) ] [ 담당자 호출 ]
context:  run-123 • 2026-08-24 12:58 • retry 가능
```

원칙 (Slack 공식 에이전트 가이드) `[문서]`:

1. **부분 진행을 보존**한다 — "어디까지 됐고 어디서 막혔는지"를 명시.
2. **다음 선택지를 준다** — 재시도 / 정보 보강 / 건너뛰기 / 사람이 인계.
3. **로딩 상태를 반드시 해제**한다 (setStatus 해제, 스트림 stop).
4. **원시 모델 출력·스택트레이스를 그대로 덤프하지 않는다** — 사람용으로 결정론적 문구로 변환("일시적 처리 문제입니다. 잠시 후 재시도해 주세요")하고 원문은 스니펫/로그 링크로.

## 폴 스트링(fallback text) 규칙 — 블록 메시지의 안전망

- 모든 `chat.postMessage`에 **평문 `text`를 반드시 병기**한다. blocks가 렌더되지 않는 환경(알림, 검색 결과, 일부 클라이언트, 스크린리더)에서 보이는 텍스트다.
- blocks 검증 실패 시 API는 `invalid_blocks`를 반납하고 **메시지는 저장되지 않는다** `[실측 ✅ T18, T24 — API 조회로 부재 확인]`. 단, 데스크톱 클라이언트가 실패 메시지를 잠시 "유령 렌더"하는 경우가 있으니 **게시 성공 여부는 항상 API 응답으로 판단** `[실측 ✅]`.
- 자주 터지는 검증 실패(전부 실측): section 3001자, header 151자, 버튼 라벨 76자, overflow 6개, 블록 51개, plan title을 text 객체로, icon_button에 text 누락. 전부 `references/reference/limits.md`에 있다.

## 스레드 동작

- 실패는 **요청이 있던 스레드 안에** 보고한다 — LangSmith Fleet도 에러를 스레드에 게시 `[문서]`. 채널 메인에 올리는 것은 사람의 개입이 필요한 최종 실패뿐.
- 재시도 성공 시 실패 카드를 `chat.update`로 "✅ 재시도로 복구됨"으로 갱신하면 이력이 깔끔하다.

## 대안 패턴

| 상황 | 수단 |
|---|---|
| 경고 수준 (작업은 계속) | section에 `:warning:` + context로 세부 — alert 블록은 Modals 전용이라 메시지에서 못 씀 `[문서]` |
| 긴 에러 로그 | 스니펫 업로드 + 카드에는 마지막 10줄만 |
| 인증/권한 오류 | 전용 안내(어떤 스코프/권한이 필요한지) + 설정 링크 버튼 |
| 반복 실패 | 알림 자체를 다이제스트로 묶기 (`10` 케이스) |

## 주의점

- Webhook/이벤트 핸들러에서는 Slack에 200을 먼저 반납하고(재시도 폭풍 방지) 에러 메시지는 비동기로 본낸다 `[문서 — 커뮤니티 패턴]`.
- `chat.update`로 원본 메시지를 덮을 때 진행 정보가 유실되지 않게 — 실패 원인과 성공 이력을 context에 남긴다.
- alert 블록(레벨 있는 배너)은 **Modals only** — 메시지에서 경고 느낌을 낼 때는 이모지+header로 흉낸다 `[문서]`.

## 검증 상태

- 실패 카드 구성 요소: `[실측 ✅ T02, T03, T06]`
- invalid_blocks 시 미저장: `[실측 ✅ T18, T24]`
- alert 블록 Modals 전용: `[문서]` (메시지 게시 미실측)

## 출처

- 에이전트 에러 설계: https://docs.slack.dev/ai/developing-agents , https://docs.slack.dev/ai/agent-governance
- alert 블록: https://docs.slack.dev/reference/block-kit/blocks/alert-block
- LangSmith Fleet 스레드 에러: https://docs.langchain.com/langsmith/fleet/slack-app
- 실측: `references/verified-matrix.md` T18, T24
