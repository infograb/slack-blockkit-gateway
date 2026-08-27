---
name: slack-blockkit
description: "Use when Slack 채널에 사람이 빠르게 읽고 행동할 수 있는 리치 Block Kit 메시지를 작성하거나 검증해야 할 때. Hermes Gateway, Hermes plugin, 승인 카드, 선택지, 접힌 상세, Markdown, 표·차트, 산출물, 진행 상태, 오류, 알림, 입력, 피드백, thread, chat.postMessage, chat.update, invalid_blocks, fallback text를 다룰 때 사용한다."
---

# Slack Block Kit

Slack 채널 메시지를 **읽기 쉽고, 접근 가능하며, API가 실제로 수락하는 Block Kit 페이로드**로 만든다. 이 스킬은 필요한 케이스 문서, 복사용 페이로드, 제한값, 텍스트 실측 기록, 로컬 검증기를 포함한다. 외부 웹 문서는 출처 확인용이며 실행에 필요하지 않다.

## 독립 실행 불변식

`SKILL_DIR`을 이 `SKILL.md`가 있는 디렉터리로 해석한다. 모든 `references/`와 `scripts/` 경로는 `SKILL_DIR` 기준이다. 호출한 프로젝트의 현재 작업 디렉터리나 원본 저장소 구조를 가정하지 않는다.

검증 명령:

```bash
python3 "$SKILL_DIR/scripts/validate_payload.py" <payload.json>
```

패키지 전체 점검:

```bash
python3 "$SKILL_DIR/scripts/check_package.py"
```

## 출력 모드

### Hermes Gateway 일반 응답

`slack-blockkit-gateway` 플러그인이 활성화된 Slack 세션에서는 semantic Markdown으로 최종 답변을 작성한다. 일반 응답에 `chat.postMessage` JSON을 노출하지 않는다. Hermes가 Slack 토큰, Socket Mode, fallback `text`, Block Kit 렌더링, 게시와 재시도를 담당한다. 자세한 설치·책임 경계는 `references/hermes-gateway.md`를 따른다.

### 명시적 API 페이로드 작성

사용자가 Slack API 페이로드나 별도 발송기용 JSON을 요청하면 다음을 제공한다.

1. 사용할 Slack API 메서드(`chat.postMessage`, `chat.update`, 파일 업로드 등)
2. 그대로 직렬화할 수 있는 JSON 페이로드 또는 완전한 SDK 호출
3. 의미 있는 top-level `text`
4. 채널·스레드·갱신 전략
5. 인터랙션 백엔드와 토큰 전제
6. 로컬 검증 결과와 남은 `[미검증]` 요소

게시까지 요청받고 사용 가능한 Slack 연결과 권한이 있으면 실제로 게시한 뒤 API 응답의 `ok:true`, `channel`, `ts`를 확인한다. 연결이나 권한이 없으면 게시했다고 말하지 않고 검증된 페이로드를 반환한다.

## 실행 절차

1. **메시지의 한 가지 목적을 정한다.** 알림, 결정, 선택, 산출물, 데이터, 진행, 오류, 입력, 피드백 중 주 목적 하나를 고른다.
2. **서피스를 정한다.** 채널에는 요약과 현재 상태를 두고, 긴 근거·로그·후속 토론은 `container` 또는 스레드로 보낸다. `references/cases/12-thread-and-surface-strategy.md`를 따른다.
3. **필요한 케이스만 읽는다.** 아래 라우팅 표에서 해당 파일을 열고, 가장 가까운 `references/payloads/` 템플릿을 복사한다. 처음부터 스키마를 추측하지 않는다.
4. **정보 계층을 구성한다.** 결론/상태 → 핵심 근거·데이터 → 접힌 상세 또는 스레드 → 행동 → 출처·메타데이터 순으로 배치한다.
5. **fallback과 접근성을 채운다.** top-level `text`만 읽어도 핵심 의미가 통해야 한다. 이미지에는 `alt_text`, 버튼에는 명확한 라벨을 둔다. 색상·이모지만으로 상태를 전달하지 않는다.
6. **문법을 하나로 통일한다.** 생성형 답변은 `markdown` 블록의 CommonMark를 사용한다. 구조 메시지는 `section`의 `mrkdwn`을 사용한다. 한 블록 안에서 두 문법을 섞지 않는다.
7. **인터랙션을 확인한다.** 버튼·셀렉트·페이지네이션은 `block_actions`를 받을 앱 백엔드가 있을 때만 사용한다. 백엔드가 없으면 `url` 버튼이나 텍스트 링크로 바꾼다.
8. **번들 검증기를 실행한다.** ERROR를 모두 고친다. WARN은 토큰·서피스·미검증 조합을 확인한 뒤 의도적으로만 허용한다.
9. **게시 결과를 API로 판정한다.** `invalid_blocks`는 전체 미게시다. 클라이언트의 일시적 렌더보다 API 응답을 신뢰한다.
10. **상태가 바뀌면 같은 메시지를 갱신한다.** 진행률이나 승인 결과는 저장한 `channel`과 `ts`로 `chat.update`하고, 완료된 인터랙션 컨트롤을 제거한다.

## 리치 메시지 구성 원칙

- **한 메시지, 한 일.** 제목과 첫 섹션만 읽어도 무엇을 알아야 하거나 해야 하는지 보여준다.
- **요약 우선.** 채널 본문은 핵심과 Top-N을 보여주고 전체 목록은 `container` 또는 스레드로 이동한다.
- **블록은 의미에 맞게 쓴다.** 데이터는 `table`/`data_table`, 차트는 검증된 `data_visualization`, 생성형 긴 답변은 `markdown`, 장문 목록은 `container`를 우선한다.
- **장식보다 스캔성.** divider, header, context를 정보 경계에만 사용한다. 모든 문단을 별도 카드처럼 만들지 않는다.
- **fallback은 중복이 아니라 요약.** 알림·검색·스크린리더에서 메시지 목적과 핵심 결과가 보이게 쓴다.
- **검증 등급을 보존한다.** `[실측 ✅]`, `[문서]`, `[미검증]`을 사실 수준에 맞게 유지한다. 스킬에 없는 조합은 성공한다고 단정하지 않는다.

## 케이스 라우팅

| 필요 | 우선 블록/수단 | 읽을 파일 | 시작 템플릿 |
|---|---|---|---|
| 승인·거절 | actions + confirm | `references/cases/01-approval-decision.md` | `references/payloads/approval-card.json` |
| 단일·복수 선택 | radio/select/overflow | `references/cases/02-choice-selection.md` | `references/payloads/choice-select.json` |
| 코드·파일·이미지 | snippet/image/link | `references/cases/03-artifact-preview.md` | `references/payloads/snippet-upload.js` |
| 링크·출처 | inline link + context | `references/cases/04-links-citations.md` | `references/payloads/markdown-llm-output.json` |
| 긴 목록·장문 | collapsible container | `references/cases/05-collapsed-long-content.md` | `references/payloads/collapsed-container.json` |
| 진행·완료 갱신 | chat.update/plan/task_card | `references/cases/06-progress-and-streaming.md` | `references/payloads/progress-update.json` |
| 표·페이지네이션·차트 | table/data_table/data_visualization | `references/cases/07-tables-and-data.md` | `references/payloads/data-table-paginated.json` |
| 오류·복구 | error summary + recovery action | `references/cases/08-error-and-fallback.md` | 해당 케이스의 구조 |
| 여러 값 입력 | input/modal | `references/cases/09-collecting-input.md` | 해당 케이스의 구조 |
| 공지·멘션 | header/section/context | `references/cases/10-notifications-mentions.md` | 해당 케이스의 구조 |
| 답변 평가 | context_actions/feedback_buttons | `references/cases/11-feedback-loop.md` | `references/payloads/feedback-buttons.json` |
| 채널·스레드·DM | thread_ts/surface 선택 | `references/cases/12-thread-and-surface-strategy.md` | 해당 케이스의 구조 |

전체 색인: `references/cases/index.md`, `references/payloads/index.md`.

## 자주 쓰는 결정

| 상황 | 선택 |
|---|---|
| 2개 결정 | 버튼 |
| 3~10개를 항상 표시 | `radio_buttons` |
| 3~100개 중 하나 | `static_select` |
| 복수 선택 | `multi_static_select`를 section accessory에 배치 |
| 긴 항목 목록 | `container` 안의 `rich_text_list` |
| LLM 답변·CommonMark 표 | `markdown` 블록 |
| 작은 정적 표 | `table` |
| 큰 표·페이지네이션 | `data_table` |
| 검증된 네이티브 차트 | `data_visualization`의 pie |
| 진행 상태 | 최초 post 후 같은 `ts`에 update |

## 자주 터지는 한계

| 항목 | 한계 |
|---|---|
| blocks/메시지 | 50 |
| section text | 3,000자; fields 10개, 각 2,000자 |
| header | 150자, plain_text만 |
| 버튼 | 라벨 75자, value 2,000자 |
| overflow/select/radio | 5/100/10 옵션 |
| actions/context | 25/10 요소 |
| container | 자식 10개, title 150자 |
| table | 100행×20열, 셀 합산 10,000자 |
| data_table | 201행, 셀 합산 20,000자 |
| markdown | 메시지 합산 12,000자 |
| top-level text | 40,000자 |

전체 제한과 토큰별 차이는 `references/reference/limits.md`, `references/reference/surfaces-tokens.md`에서 확인한다.

## 흔한 실패와 교정

| 실패 | 교정 |
|---|---|
| `section.expand:false`를 확정적 접기로 간주 | 기본 접기가 필요하면 `container`의 `is_collapsible`와 `default_collapsed` 사용 |
| Slack에 네이티브 차트가 없다고 가정 | 검증된 pie는 `data_visualization`; bar/line/area는 `[미검증]` 표시 |
| 표 스키마나 셀 타입을 기억으로 작성 | 번들 `table-basic.json` 또는 `data-table-paginated.json` 복사 |
| blocks만 만들고 top-level `text` 누락 | 독립적으로 의미가 통하는 fallback 요약 추가 |
| 버튼이 렌더되면 기능도 된다고 간주 | interactivity 백엔드 확인; 없으면 URL/텍스트로 전환 |
| `mrkdwn`에 `**bold**` 또는 `[text](url)` 사용 | `mrkdwn`은 `*bold*`, `<url|text>`; CommonMark는 `markdown` 블록 |
| 현재 작업 디렉터리에서 `scripts/` 경로를 바로 실행 | 항상 `SKILL_DIR/scripts/` 절대 경로 사용 |
| 실패한 rich payload를 그대로 반복 | ERROR를 수정; 인증·권한·rate limit은 block fallback으로 숨기지 않음 |

## 검증 근거와 번들 리소스

- `references/verified-matrix.md` — 2026-08-24 InfoGrab 워크스페이스 유저 토큰 실측 T01~T42
- `references/reference/` — 블록·엘리먼트·문법·제한·토큰 카탈로그
- `references/cases/` — 상황별 패턴 12종
- `references/payloads/` — 복사용 JSON 10종과 파일 업로드 SDK 예시
- `references/hermes-gateway.md` — Hermes 네이티브 플러그인 설치, 토큰 경계, 자동 렌더 범위
- `references/gaps.md` — 아직 성공을 단정할 수 없는 영역
- `references/sources.md` — 공식 문서와 조사 출처; 실행 의존성 아님
- `scripts/validate_payload.py` — 개별 페이로드 검증
- `scripts/check_package.py` — 패키지 경계와 번들 전체 검증
