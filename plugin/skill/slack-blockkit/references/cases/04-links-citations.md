# 04. 링크와 출처 (Links & Citations)

## 언제 쓰는가

답변의 근거 URL을 보여줘야 할 때, 외부 문서/이슈/PR로 본내야 할 때, AI 생성 답변에 출처를 달아 신뢰를 줄 때.

## 권장 형태

### 1. 인라인 링크 (기본)

- mrkdwn: `<https://example.com|표시 텍스트>` `[실측 ✅ T01]`
- markdown 블록: `[표시 텍스트](https://example.com)` — 서버가 CommonMark를 rich_text로 변환 `[실측 ✅ T37]`
- **본문 중 출처는 인라인으로 달고, URL 나열은 피한다.** Slack 공식 에이전트 가이드도 인라인 인용을 권장 `[문서]`.

### 2. 인용 푸터 (context 블록) — AI 답변의 정석

답변 말미에 작은 회색 글씨로 출처를 모은다. Slack이 공식 문서에서 AI 앱용으로 제시한 패턴이다 `[문서 — developing-agents]`:

```
context: [ 📄 ] 출처: <url|[1] GitLab MR 가이드> • <url|[2] 남은 작업 이슈 #42> • AI 생성 답변 — 부정확할 수 있음
```

- context 블록의 elements는 최대 10개, image element + text object만 `[문서]` `[실측 ✅ T02]`.
- AI 디스클레이머도 같은 위치에 둔다(법적·정책 문구 포함). `10-notifications-mentions.md`의 신원 표시와 같은 계열.

### 3. 언펄 제어

- 링크가 여러 개면 언펄로 메시지가 더러워진다 — Slack 공식 권고: **출처가 많을 때는 언펄을 끈다** (`unfurl_links: false`) `[문서 — developing-agents]`.
- 언펄은 도메인 소유 앱(GitHub 앱 등)이나 슬랙 내장 파서가 있을 때만 일어난다. 실측: GitHub 앱 미설치 워크스페이스에서 `unfurl_links: true`로 게시했으나 → 미언펄 `[실측 ✅ T29]`.

## 스레드 동작

- 출처 목록이 길면(5개+) 본문 메시지에는 대표 2~3개만, 전체 목록은 스레드 답글에.
- 답변 본문이 스트리밍이면 스트림 중에는 언펄이 비활성화된다 `[문서 — chat-streaming changelog]`. 최종 링크 카드는 `chat.stopStream`의 blocks로.

## 대안 패턴

| 목적 | 수단 |
|---|---|
| "앱에서 열기" 유도 | `url` 버튼 (`03` 케이스) |
| 메일 주소 | `<mailto:a@b.c|텍스트>` `[문서]` |
| 채널 참조 | `<#C01234567>` `[문서]` |
| 날짜를 로컬 시간으로 | `<!date^epoch^{date_short_pretty}|fallback>` `[문서]` |

## 주의점

- mrkdwn 링크에서 **URL에 공백이 있으면 깨진다** `[문서]`. URL 인코딩 필수.
- `&`, `<`, `>`는 `&amp;` `&lt;` `&gt;`로 이스케이프 — 텍스트 전체를 인코딩하지 말고 해당 문자만 `[문서]`.
- top-level `text`(폴 스트링)에도 링크를 넣어라 — 알림/검색에서 blocks 내 링크는 안 보일 수 있다.
- Slack 도메인(slack.com 남남부 링크)은 video 블록 등 일부에서 거부된다 `[문서]`.

## 검증 상태

- 인라인 링크(mrkdwn/CommonMark), context 푸터: `[실측 ✅ T01, T02, T13, T37]`
- 언펄 제어·미언펄: `[실측 ✅ T29]`, 스트림 중 언펄 비활성: `[문서]`

## 출처

- 메시지 포맷팅: https://docs.slack.dev/messaging/formatting-message-text
- 에이전트 개발 가이드(인라인 인용·언펄 억제·디스클레이머): https://docs.slack.dev/ai/developing-agents
- 실측: `references/verified-matrix.md` T01, T02, T29, T37
