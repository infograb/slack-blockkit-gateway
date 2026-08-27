# mrkdwn vs markdown 블록 — LLM이 절대 헷갈리면 안 되는 문법 차이

슬랙에는 **두 개의 서로 다른 문법 체계**가 있다. LLM은 CommonMark를 낸내는 경향이 있어 이 차이에서 사고가 가장 많이 난다.

## 비교표

| 하고 싶은 것 | `mrkdwn` (text object — 슬랙 고유) | `markdown` 블록 (CommonMark) |
|---|---|---|
| 볼드 | `*bold*` | `**bold**` 또는 `__bold__` |
| 이탤릭 | `_italic_` | `*italic*` 또는 `_italic_` |
| 취소선 | `~strike~` | `~~strike~~` |
| 링크 | `<https://url\|텍스트>` | `[텍스트](https://url)` |
| 인라인 코드 | `` `code` `` | `` `code` `` (동일) |
| 코드블록 | ```` ``` ```` (언어 강조 없음) | ```` ```python ```` (언어별 구문강조 ✅) |
| 리스트 | **문법 없음** — `•` 문자+줄바꿈으로 흉내 | `-` / `1.` 네이티브 ✅ |
| 표 | **불가** | `\|` 표 문법 ✅ (2026-03-06~) |
| 헤더 | 없음 (header 블록 사용) | `#`~`######` (가변 크기, 2026-03-06~) |
| 인용 | `> 인용` | `> 인용` (동일) |
| task list | 불가 | `- [x]` / `- [ ]` ✅ |
| 구분선 | 없음 (divider 블록) | `---` ✅ |
| 멘션/채널 | `<@U…>` `<#C…>` `<!here>` `<!date^…>` | 슬랙 확장 문법 지원 여부 [미검증] |
| 이미지 | 불가 (image 블록) | `![alt](url)`은 **링크로 변환**됨 `[문서]` |

**전부 서버 사이드 파싱 실측** `[실측 ✅ T13, T37, T42 — 저장된 rich_text 검사로 확인]`.

## 어디에 뭘 쓰나

| 상황 | 권장 |
|---|---|
| **LLM 생성 텍스트를 그대로 본낼 때** | **`markdown` 블록** — CommonMark가 그대로 먹힌다. 변환 로직 불필요 |
| 에이전트가 직접 조립하는 구조화 메시지 | `section`(mrkdwn) + 필요 시 rich_text |
| 멘션·날짜 토큰 필요 | mrkdwn 계열 (markdown 블록에서의 멘션 동작은 [미검증]) |
| 스트리밍 청크 | `markdown_text` 파라미터 (markdown 블록과 같은 CommonMark) `[문서]` |

## 실측 팁

1. `markdown` 블록은 **서버가 rich_text로 변환해 저장**한다 — API로 읽으면 원본 markdown이 아니라 rich_text가 온다 `[실측 ✅]`.
2. 첫 렌더에서 일시적으로 원문이 그대로 보였다가 올바르게 다시 렌더되는 **클라이언트 과도기 현상**을 관측했다. API 저장본이 정본이다 `[실측 ✅ T13]`.
3. markdown 블록은 **Messages only** — 모달/App Home 불가, `block_id` 무시 `[문서]`.
4. 합산 12,000자/payload `[문서]`.
5. mrkdwn에서는 `&` `<` `>`만 이스케이프(`&amp;` 등), 전체 인코딩 금지 `[문서]`.
6. mrkdwn 자동 파싱: text object는 `verbatim: false`(기본)일 때 URL·멘션 자동 변환 `[문서]`.

## 변환 치트 (LLM 출력 → mrkdwn이 꼭 필요할 때)

| CommonMark | mrkdwn |
|---|---|
| `**x**` / `__x__` | `*x*` |
| `*x*` (이탤릭 의도) | `_x_` |
| `~~x~~` | `~x~` |
| `[t](u)` | `<u\|t>` |
| `- item` | `• item` (리터럴 불릿) |
| `| 표 |` | table 블록으로 재구성 |

가능하면 변환하지 말고 `markdown` 블록을 쓴다 — 변환은 항상 엣지 케이스를 만든다.

## 출처

- mrkdwn 규칙: https://docs.slack.dev/messaging/formatting-message-text
- markdown 블록: https://docs.slack.dev/reference/block-kit/blocks/markdown-block , https://docs.slack.dev/changelog/2025/02/03/block-kit-markdown , https://docs.slack.dev/changelog/2026/03/06/block-kit-rich-text
- 실측: `references/verified-matrix.md` T01, T13, T37, T42
