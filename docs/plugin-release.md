# Hermes Plugin Release Guide

`slack-blockkit-gateway` 공개 배포 절차다. 소스 저장소는 연구 볼트와 분리할 수 있으며, release archive는 공개 허용 목록만 포함한다.

## 사전 조건

- Python 3.11 이상
- Hermes Agent 0.20.5
- GitHub 저장소와 push 권한
- `gh` 인증
- 깨끗한 release commit

CI는 PyPI version 대신 Hermes v0.20.5의 정확한 upstream commit `9aa7530f7b53699e2c6d648ded8f6300503b3dc7`을 설치한다. Hermes 검증 기준을 올릴 때 이 SHA와 로컬 Plugin Doctor 결과를 함께 갱신한다.

## 공개 패키지 경계

포함:

- `plugin/plugin.yaml`
- `plugin/__init__.py`
- `plugin/LICENSE`
- `plugin/after-install.md`
- public `README.md`
- `plugin/skill/slack-blockkit/**`

제외:

- 연구 볼트의 `cases/`, `payloads/`, `reference/`, `verification/`
- 개인 DM·workspace 렌더 스크린샷
- 테스트와 CI 소스
- `.git`, 캐시, 임시 파일, `dist/`
- Slack token 형태 문자열, 실제 workspace ID, 로컬 사용자 절대 경로

## 전체 검증

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
hermes plugins doctor plugin --ci
python3 plugin/skill/slack-blockkit/scripts/check_package.py
python3 scripts/build-plugin-release.py --output dist
```

생성물:

```text
dist/
├── slack-blockkit-gateway-1.0.0.zip
├── slack-blockkit-gateway-1.0.0.tar.gz
└── SHA256SUMS
```

`tests/test_release_builder.py`는 ZIP/TAR의 파일 경계, 비밀 패턴, 실제 workspace ID, checksum, 재현 가능성을 검사한다.

## GitHub 저장소 준비

현재 작업 디렉터리에 Git metadata가 없다면 새 공개 저장소를 만든다.

```bash
git init
git add .
git commit -m "feat: release slack-blockkit-gateway 1.0.0"
git branch -M main
git remote add origin git@github.com:infograb/slack-blockkit-gateway.git
git push -u origin main
```

공개 전 `verification/screenshots/` 같은 private source-vault 디렉터리가 commit에 들어가지 않았는지 확인한다. 공개 plugin 전용 저장소를 만들 때는 release archive의 압축 해제 결과를 초기 소스로 사용하는 것이 가장 안전하다.

## 태그와 GitHub Release

```bash
git tag -s v1.0.0 -m "slack-blockkit-gateway v1.0.0"
git push origin v1.0.0
```

`.github/workflows/plugin-release.yml`은 full-SHA로 고정한 GitHub Actions와 Hermes commit으로 테스트·archive build를 반복한다. `v*` 태그에서는 GitHub OIDC build provenance를 발행하고 ZIP, TAR.GZ, `SHA256SUMS`를 Release에 첨부한다.

서명 태그를 사용할 수 없는 환경에서는 annotated tag를 사용하되 release notes에 서명 미사용을 명시한다.

Release 직후 provenance를 확인한다.

```bash
gh attestation verify dist/slack-blockkit-gateway-1.0.0.zip \
  --repo infograb/slack-blockkit-gateway
gh attestation verify dist/slack-blockkit-gateway-1.0.0.tar.gz \
  --repo infograb/slack-blockkit-gateway
```

`SHA256SUMS`는 손상 검사이며 배포자 인증을 대신하지 않는다.

## 설치 검증

릴리스 후 임시 Hermes home 또는 테스트 머신에서 pinned SHA 설치를 확인한다.

```bash
SHA=$(git rev-parse HEAD)
hermes plugins install infograb/slack-blockkit-gateway/plugin --ref "$SHA" --enable
hermes plugins doctor slack-blockkit-gateway --ci
```

Slack 설정:

```yaml
platforms:
  slack:
    extra:
      rich_blocks: true
```

Gateway 재시작 후 새 Slack 세션에서 제목·목록·코드·표 응답을 확인한다. 실제 API `ok:true`, blocks, fallback text와 table 렌더가 확인되기 전에는 live Gateway 검증을 완료로 표시하지 않는다.

## Community plugin index 제출

Hermes community index는 mutable tag나 branch 대신 정확한 40자리 commit SHA를 사용한다.

```bash
git rev-parse HEAD
```

제출 항목:

```json
{
  "name": "slack-blockkit-gateway",
  "description": "Render Hermes Slack gateway replies as rich Block Kit without exposing Slack credentials to the plugin.",
  "author": "InfoGrab",
  "tags": ["slack", "block-kit", "gateway", "skills"],
  "repo": "infograb/slack-blockkit-gateway",
  "subdir": "plugin",
  "ref": "<exact-40-character-commit-sha>"
}
```

`ref`는 release commit의 실제 값으로 교체한다. Git remote와 commit이 없는 현재 작업 디렉터리에서는 index entry를 확정하지 않는다.

## 버전 갱신

1. `plugin.yaml`의 `version`을 올린다.
2. 사용자 영향과 호환성을 README에 반영한다.
3. 전체 검증을 실행한다.
4. 새 archive와 checksum을 확인한다.
5. 같은 버전의 Git tag를 만든다.
6. 새 commit SHA로 community index PR을 갱신한다.

## 출시 중단 조건

다음 중 하나라도 있으면 tag를 만들지 않는다.

- Plugin Doctor 실패
- unit 또는 archive test 실패
- skill package validation 실패
- release archive에 screenshot, secret pattern, workspace ID, absolute user path 포함
- ZIP/TAR checksum 비결정성
- `plugin.yaml` version과 archive root 불일치
- LICENSE/author 누락
- 설치 문서와 실제 명령 불일치
