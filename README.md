# Slack Block Kit Gateway for Hermes

Hermes Slack Gateway 응답을 읽기 좋은 Block Kit으로 렌더하는 네이티브 플러그인이다. 플러그인은 Slack 자격증명이나 네트워크에 접근하지 않는다. Hermes가 Socket Mode, 토큰, 채널 라우팅, fallback text, 게시와 재시도를 담당한다.

## 요구사항

- Hermes Agent 0.20.5 이상에서 검증
- Hermes Slack Gateway 설정 완료
- Python 3.11 이상

## 설치

### GitHub 저장소

```bash
hermes plugins install infograb/slack-blockkit-gateway/plugin --enable
```

재현 가능한 운영 설치는 40자리 commit SHA를 고정한다.

```bash
hermes plugins install infograb/slack-blockkit-gateway/plugin \
  --ref <40-character-commit-sha> \
  --enable
```

Release 페이지에서 사용할 archive와 `SHA256SUMS`를 함께 받는다. 선택한 archive의 한 줄만 검사한다.

GitHub release archive는 checksum보다 먼저 build provenance를 검증한다.

```bash
REPO=infograb/slack-blockkit-gateway
ARCHIVE=slack-blockkit-gateway-1.0.0.zip   # 또는 .tar.gz
gh attestation verify "$ARCHIVE" --repo "$REPO"
```

`SHA256SUMS`는 다운로드 손상 확인용이다. 배포자 인증은 위 attestation 검증이 담당한다.

### ZIP release

```bash
if command -v sha256sum >/dev/null; then
  grep '  slack-blockkit-gateway-1.0.0.zip$' SHA256SUMS | sha256sum -c -
else
  grep '  slack-blockkit-gateway-1.0.0.zip$' SHA256SUMS | shasum -a 256 -c -
fi
```

```bash
mkdir -p ~/.hermes/plugins
unzip slack-blockkit-gateway-1.0.0.zip -d ~/.hermes/plugins
hermes plugins enable slack-blockkit-gateway
```

### TAR.GZ release

```bash
if command -v sha256sum >/dev/null; then
  grep '  slack-blockkit-gateway-1.0.0.tar.gz$' SHA256SUMS | sha256sum -c -
else
  grep '  slack-blockkit-gateway-1.0.0.tar.gz$' SHA256SUMS | shasum -a 256 -c -
fi
```

```bash
mkdir -p ~/.hermes/plugins
tar -xzf slack-blockkit-gateway-1.0.0.tar.gz -C ~/.hermes/plugins
hermes plugins enable slack-blockkit-gateway
```

설치 후 manifest, import, skill registration을 검사한다.

```bash
hermes plugins doctor ~/.hermes/plugins/slack-blockkit-gateway-1.0.0 --ci
```

## Slack Block Kit 활성화

`~/.hermes/config.yaml`:

```yaml
platforms:
  slack:
    extra:
      rich_blocks: true
      native_task_cards: true   # 권장 기본값
      feedback_buttons: false   # 피드백 로그를 운영할 때만 활성화
```

구조화된 renderer를 사용할 때 `markdown_blocks`는 끄거나 설정하지 않는다. 두 옵션이 모두 켜지면 Hermes가 `markdown_blocks`를 먼저 선택한다.

- `native_task_cards`: 도구 진행을 한 개의 갱신형 plan/task 카드로 보여 채널 노이즈를 줄인다. Slack native API가 불가능하면 Hermes가 fallback한다.
- `feedback_buttons`: 모든 최종 rich reply에 Good/Bad 버튼을 붙인다. 현재 Hermes는 클릭을 로그로만 남기므로, 로그를 실제 품질 리뷰에 연결하지 않으면 UI만 복잡해진다.

```bash
hermes gateway restart
```

system prompt section은 새 세션에서 고정된다. 기존 Slack 대화에서는 `/new` 또는 `/reset`을 실행한다.

## 확인

Gateway에서 `/plugins`를 실행해 `slack-blockkit-gateway`가 로드됐는지 확인한다. 다음처럼 구조가 있는 응답을 요청한다.

```text
배포 결과를 표와 검증 요약으로 공유해줘.
```

정상 경로:

```text
semantic Markdown
  → Hermes SlackAdapter rich_blocks
  → chat.postMessage(text + blocks)
```

일반 응답은 API JSON이 아니라 Markdown이어야 한다. Hermes가 header, section, divider, nested list, code, quote, native table과 fallback text를 만든다.

## Plugin skill

세부 제한이나 명시적 Slack API payload가 필요할 때:

```text
skill_view("slack-blockkit-gateway:slack-blockkit")
```

선택·승인은 Hermes `clarify` 또는 approval 흐름을 사용한다. `container`, `data_table`, `data_visualization`, custom actions는 일반 Gateway 응답에서 자동 생성되지 않으며 명시적 payload 작성 모드로만 사용한다.

## 토큰 경계

Slack 자격증명은 기존 Hermes secret 위치에만 둔다.

```text
~/.hermes/.env
  SLACK_BOT_TOKEN=xoxb-...
  SLACK_APP_TOKEN=xapp-...
```

다음 위치에는 토큰을 넣지 않는다.

- `plugin.yaml`
- plugin settings
- skill 문서
- `mcp.json`
- Git 저장소
- release archive

플러그인은 `requires_env`, privileged capability, Slack SDK, HTTP client를 선언하지 않는다.

## 업데이트

고정하지 않은 Git 설치:

```bash
hermes plugins update slack-blockkit-gateway
hermes gateway restart
```

고정 설치는 새 commit SHA를 명시적으로 다시 설치한다.

```bash
hermes plugins install infograb/slack-blockkit-gateway/plugin \
  --force \
  --ref <new-40-character-commit-sha>
hermes gateway restart
```

Archive 설치는 새 파일의 checksum을 먼저 확인하고 이전 version directory를 명시적으로 교체한다.

```bash
rm -rf ~/.hermes/plugins/slack-blockkit-gateway-<old-version>
unzip slack-blockkit-gateway-<new-version>.zip -d ~/.hermes/plugins
hermes plugins enable slack-blockkit-gateway
hermes plugins doctor ~/.hermes/plugins/slack-blockkit-gateway-<new-version> --ci
hermes gateway restart
```

## 제거

```bash
hermes plugins remove slack-blockkit-gateway
hermes gateway restart
```

수동 archive 설치는 해당 디렉터리를 제거한다.

```bash
rm -rf ~/.hermes/plugins/slack-blockkit-gateway-1.0.0
hermes gateway restart
```

## 문제 해결

| 증상 | 확인 |
|---|---|
| plugin이 보이지 않음 | `hermes plugins list`, `hermes plugins enable slack-blockkit-gateway` |
| 등록 실패 | `hermes plugins doctor <plugin-directory> --ci` |
| Markdown만 보임 | `platforms.slack.extra.rich_blocks: true` 확인 |
| 기존 세션만 적용 안 됨 | Slack에서 `/new` 또는 `/reset` |
| 표가 monospace로 보임 | Slack table 제한 또는 renderer fallback 확인 |
| blocks가 거부됨 | Hermes 로그의 block rejection과 평문 재시도 확인 |
| Task Card가 평문으로 폴백 | `cannot_provide_both_markdown_text_and_chunks` 확인 후 `docs/hermes-core-compatibility.md`의 core patch 적용 |

리치 컨트롤 종합 payload는 `plugin/skill/slack-blockkit/references/payloads/rich-controls-message.json`, xoxb 검증 결과는 `verified-matrix.md` T43~T49, 성능 기준은 `performance.md`에 있다.

## 공개 패키지 정책

공개 archive에는 개인 DM·workspace 식별 정보가 들어 있는 렌더 스크린샷을 포함하지 않는다. T01~T49의 텍스트 검증 결과와 API 오류 원문은 `skill/slack-blockkit/references/verified-matrix.md`에 유지한다.

## 라이선스

MIT License. Copyright 2026 InfoGrab.
