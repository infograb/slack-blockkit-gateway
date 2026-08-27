# Hermes Gateway 연동

이 저장소는 Hermes 네이티브 플러그인으로도 설치할 수 있다. 목적은 Slack 자격증명을 플러그인이나 스킬에 전달하지 않고, Hermes Gateway가 보내는 최종 응답을 읽기 좋은 Block Kit으로 렌더하는 것이다.

## 책임 경계

```text
Hermes agent
  → Slack 전용 system-prompt section
  → 의미 구조가 분명한 Markdown
  → Hermes SlackAdapter rich_blocks renderer
  → chat.postMessage(text + blocks)
  → Slack
```

- Hermes Gateway: `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, Socket Mode, 채널 라우팅, fallback `text`, 게시·재시도 담당
- `slack-blockkit-gateway` 플러그인: Slack 세션 전용 작성 규칙과 번들 스킬 등록
- `slack-blockkit` 스킬: Block Kit 선택 기준, 제한, 명시적 API 페이로드, 검증기 제공

플러그인은 Slack 토큰을 읽지 않고 `slack_sdk`나 HTTP 클라이언트를 사용하지 않는다. `plugin.yaml`에도 `requires_env`와 privileged capability가 없다.

## 설치

공개 저장소의 `plugin/`이 설치 가능한 플러그인 루트다. `plugin.yaml`, `__init__.py`, `LICENSE`, `skill/slack-blockkit/`을 함께 유지한다.

Git 저장소 설치:

```bash
hermes plugins install infograb/slack-blockkit-gateway/plugin \
  --enable
```

Release archive는 압축을 푼 version directory를 Hermes user plugin directory 아래에 둔 뒤 활성화한다. 프로젝트 로컬 plugin은 기본 비활성이므로 신뢰한 저장소에서만 project plugin opt-in을 사용한다.

## Slack 렌더러 활성화

Hermes 설정 명령으로 내장 Block Kit 렌더러를 켠다.

```bash
hermes config set platforms.slack.extra.rich_blocks true
hermes config set platforms.slack.extra.native_task_cards true
hermes config set platforms.slack.extra.feedback_buttons false
```

구조화된 `rich_blocks` 렌더러를 우선하려면 `markdown_blocks`는 끄거나 설정하지 않는다. 두 옵션이 모두 켜져 있으면 Hermes는 `markdown_blocks`를 먼저 선택한다.

`native_task_cards`는 도구 진행을 한 개의 갱신형 카드로 보여 주므로 권장 기본값으로 켠다. `feedback_buttons`는 모든 최종 응답에 컨트롤을 추가하지만 현재 처리는 클릭 로그 기록뿐이므로, 별도 피드백 분석을 운영하지 않으면 끈다.

설정 후 Gateway를 재시작한다.

```bash
hermes gateway restart
```

system-prompt section은 새 세션에서 고정된다. 기존 Slack 대화는 `/new` 또는 `/reset`으로 새 세션을 시작한 뒤 적용 여부를 확인한다.

Slack 토큰은 `hermes gateway setup`이 관리하는 기존 Gateway secret store에만 둔다. 토큰을 플러그인 설정, 스킬 파일, `mcp.json`, 저장소에 복사하지 않는다.

## 자동 동작

플러그인이 활성화되면 새 Slack 세션에만 다음 정책이 적용된다.

1. 최종 응답을 결론 우선 semantic Markdown으로 작성한다.
2. 일반 응답에서 `chat.postMessage` JSON을 노출하지 않는다.
3. Hermes SlackAdapter가 header, divider, nested list, code, quote, native table과 fallback text를 생성한다.
4. 선택·승인은 Hermes `clarify` 또는 approval 흐름을 사용한다. Slack 어댑터가 버튼과 resolved state를 처리한다.
5. 세부 Slack 제한이나 명시적 API 페이로드가 필요할 때 `skill_view("slack-blockkit-gateway:slack-blockkit")`을 불러온다.

채널별 `channel_skill_bindings`나 토큰-스킬 연결은 필요하지 않다. system-prompt section은 `platform == "slack"`인 새 세션에서만 내용을 반환한다.

## 자동 렌더 범위

Hermes의 공개 플러그인 API와 내장 Slack 렌더러로 자동 적용되는 범위:

- header와 section
- divider
- 중첩 목록
- fenced code와 quote
- Markdown pipe table → native `table`
- top-level fallback `text`
- `invalid_blocks` 발생 시 blocks 제거 재시도
- Hermes 내장 clarify/approval 버튼
- 선택적 feedback buttons와 native task cards

일반 텍스트 응답에서 자동 생성되지 않는 범위:

- `container`
- `data_table`
- `data_visualization`
- 임의의 custom actions

이 블록들은 `slack-blockkit`의 명시적 페이로드 작성 패턴으로 유지한다. Hermes의 현재 공개 플러그인 계약에는 outbound blocks 교체 훅이 없으므로, 자동화를 위해 private `SlackAdapter._maybe_blocks()`를 monkey-patch하거나 내장 Slack platform을 덮어쓰지 않는다.

## 확인

```bash
hermes plugins list
hermes plugins doctor <plugin-directory> --ci
```

Gateway 세션에서는 `/plugins`로 로드 상태를 확인한다. 새 Slack 세션에서 제목, 목록, 코드, 표가 포함된 응답을 요청하고 다음을 확인한다.

- API 응답이 성공한다.
- 메시지에 blocks와 의미 있는 fallback text가 함께 있다.
- 표가 native table로 보인다.
- blocks가 거부돼도 평문 응답이 남는다.

### 로컬 검증 결과

2026-08-27, Hermes Agent v0.20.5에서 다음을 확인했다.

- 저장소 루트 `hermes plugins doctor . --ci` 통과
- `plugin.yaml`, `__init__.py`, `skill/`만 임시 디렉터리에 복사한 standalone doctor 통과
- 번들 skill 검사 통과: Markdown 24개, JSON payload 10개, 공개 screenshot 0개
- Hermes 내장 `render_blocks()`에 제목·목록·코드·표가 있는 Markdown을 입력해 `header`, `section`, `divider`, `rich_text`, `table` 7개 블록 생성 확인

실제 xoxb Gateway 게시·클라이언트 렌더는 `[미검증]`이며 `references/gaps.md` A11로 추적한다.

## 출처

- Hermes Plugins: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Build a Hermes Plugin: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
- Hermes Slack: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack
- Hermes Event Hooks: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
