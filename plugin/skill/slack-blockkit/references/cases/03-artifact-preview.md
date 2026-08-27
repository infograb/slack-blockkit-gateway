# 03. 산출물 미리보기 (Artifact Preview)

## 언제 쓰는가

에이전트가 만든 산출물 — 코드, 로그, 리포트, 이미지, 문서, 대시보드 스크린샷 — 을 사람이 슬랙 안에서 바로 확인(또는 한 클릭에 열기)해야 할 때.

## 산출물 종류별 권장 수단

| 산출물 | 1순위 | 2순위 | 검증 |
|---|---|---|---|
| 코드 / 로그 / 긴 텍스트 | **스니펫 업로드** (`filesUploadV2` + `snippet_type`) | ``` 코드펜스 (짧을 때만) | [실측 ✅ T25] |
| 이미지/차트 렌더 | **파일 업로드** (슬랙 호스팅) | image 블록 + 외부 URL | [실측 ✅ — 단, 외부 URL 깨짐 사례 T04] |
| 짧은 diff/패치 | section/markdown 안 ``` 펜스 | 스니펫 | [실측 ✅ T13] |
| 외부 시스템 문서/PR/대시보드 | **URL 버튼** ("리포트 열기 ↗") | 인라인 링크 | [실측 ✅ T06] |
| 자기 서비스 링크 | 커스텀 언펄 (`chat.unfurl`) | URL 버튼 | [문서 — 앱 필요] |
| 대형 산출물 (HTML 프로토타입 등) | 외부 호스팅 + URL 버튼 | 캔버스 (슬랙 문서) | [미검증 — canvas API는 앱/플랜 의존] |

## 권장 형태 1: 스니펫 업로드 (코드/로그의 정석)

```
filesUploadV2({
  channel_id, thread_ts,
  initial_comment: '요약 한 줄 + 무엇을 볼지',
  file_uploads: [{ content, filename: 'hello.py', snippet_type: 'python', title }]
})
```

- 슬랙이 **구문 강조 프리뷰를 접힌 상태로** 렌더하고 클릭하면 전문이 열린다. 긴 텍스트의 네이티브 "접기"이기도 하다 (`05` 케이스).
- 스니펫은 1MB까지 `[문서]`. `files.upload`는 2025-11-12 종료 — `getUploadURLExternal`+`completeUploadExternal`(SDK의 `uploadV2`)을 쓴다 `[문서]`.
- `[실측 ✅ T25 — python 스니펫 업로드·프리뷰 렌더 확인]`. 페이로드: `references/payloads/snippet-upload.js`

## 권장 형태 2: 이미지

- **파일로 업로드하면 슬랙이 호스팅하므로 가장 안정적.** 인라인 프리뷰 제한: 긴 변 25,000px 미만, 총 4,500만 화소 미만 `[문서 — slack.com 헬프]`.
- `image` 블록 + 외부 `image_url`은 **URL이 공개·안정적이어야 한다.** 실측에서 외부 이미지(thrillist CDN)가 로드되지 않고 alt 텍스트만 표시됨 `[실측 ✅ T04]`. 같은 메시지 안 슬랙 자체 CDN 이미지는 정상 렌더 `[실측 ✅ T03 accessory]`.
- 이미지 블록 제한: `image_url` 3000자, `alt_text` 2000자(필수), png/jpg/jpeg/gif `[문서]`. `slack_file` 객체로 방금 업로드한 파일을 참조할 수도 있다 `[문서]`.
- 섬네일이면 image 블록 대신 section `accessory` 이미지가 읽기 좋다 `[실측 ✅ T03]`.

## 권장 형태 3: 외부 링크를 버튼으로

"전체 리포트는 대시보드에서" 류는 `url` 버튼이 가장 단순하고 항상 동작한다 `[실측 ✅ T06]`. `block_actions` 백엔드 없이도 된다는 것이 버튼과의 결정적 차이.

## 권장 형태 4: 커스텀 언펄 (고급, 앱 필요)

자사 서비스 링크를 붙여넣었을 때 Jira/GitHub처럼 리치 카드로 펼치려면: 앱이 `link_shared` 이벤트를 받아 `chat.unfurl`로 미리보기를 반환한다. Sourcegraph는 여기에 flexpane(사이드바 상세)까지 연결했다 `[문서 — Sourcegraph 블로그]`. Work Objects(2025-10-22 GA)가 이 계열의 최신 메커니즘 `[문서]`.

- 봇/유저가 게시한 링크가 자동 언펄되는지는 환경 의존 — 실측에서 `unfurl_links: true`로 GitHub 링크를 게시했으나 언펄되지 않음 (GitHub 앱 미설치 워크스페이스) `[실측 ✅ T29]`. **언펄은 도메인 소유 앱이 있어야 일어난다고 보는 것이 안전.**

## 스레드 동작

- 산출물 미리보기 자체가 길면(스니펫 여러 개) **부모 = 요약 + 대표 산출물 1개, 스레드 답글 = 나머지 산출물**.
- `thread_ts`를 주면 파일이 스레드 안에 직접 업로드된다 `[실측 ✅ T25]`.
- 산출물이 재생성되면 새 파일을 올리고, 부모 카드를 `chat.update`로 최신 링크/버전으로 갱신.

## 주의점

- `file` 블록(리모트 파일 표시)은 앱이 직접 게시할 수 없다 — 조회 전용 `[문서]`. 파일은 항상 업로드 API로.
- video 블록은 `links.embed:write` 스코프 + unfurl 도메인 등록 + 임베더블 iFrame이 필요 — 실측에서 스코프 부재로 거부됨 `[실측 ✅ T15]`. 일반 에이전트에는 비추천, 유튜브 등은 그냥 링크로.
- 스니펫 `initial_comment`가 사실상 캡션이다 — 무엇인지 한 줄을 반드시 넣는다.

## 검증 상태

- 스니펫 업로드·image·URL 버튼·언펄 부재: `[실측 ✅ T04, T06, T25, T29]`
- 커스텀 언펄·Work Objects·캔버스: `[문서]` (앱/플랜 필요, 미실측)

## 출처

- 파일 작업 가이드: https://docs.slack.dev/messaging/working-with-files
- files.upload 종료 공지: https://docs.slack.dev/reference/methods/files.upload
- 긴 텍스트 스니펫 우회(커뮤니티 정석): https://stackoverflow.com/questions/54048384/
- Sourcegraph Deep Search 언펄→flexpane: https://sourcegraph.com/blog/deep-search-slack-agent-lessons
- 인라인 프리뷰 픽셀 제한: https://slack.com/help/articles/201330736-Add-files-to-Slack
- 실측: `references/verified-matrix.md` T04, T06, T15, T25, T29
