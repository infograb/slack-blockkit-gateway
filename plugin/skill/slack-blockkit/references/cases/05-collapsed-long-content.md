# 05. 긴 목록·긴 텍스트 접기 (Collapsed / Long Content)

## 언제 쓰는가

에이전트 출력이 화면을 잡아먹을 때 — 검색 결과 30건, 로그 200줄, 파일 diff 전문, 하위 작업 목록. **슬랙에는 전통적으로 네이티브 접기가 없었으나, 2026-06-29 `container` 블록으로 공식 지원이 생겼다** `[문서 — changelog]`.

## 1순위: container 블록 (네이티브 접기) `[실측 ✅ T30]`

```
{
  "type": "container",
  "title": "검색 결과 30건 — 펼쳐 보기",
  "is_collapsible": true,
  "default_collapsed": true,
  "child_blocks": [ ...최대 10개 블록... ]
}
```

- **기본 접힘 상태로 렌더되고, 사람이 셰브론을 눌러 펼친다.** 게시→접힘 렌더→클릭→펼침까지 전 과정 실측 `[실측 ✅ T30]`.
- 제한: `title` 150자, `child_blocks` 최대 10개. 자식으로 actions, context, divider, file, header, image, input, rich_text, section, table, video 가능 `[문서]`.
- width: `narrow`/`standard`/`wide`/`full` `[문서]`.
- 주의: 자식 10개 제한이 있어 **30건 목록이면 container 안에 rich_text 리스트 1개로 묶어 넣는 식**으로 설계한다 (블록 10개 제한은 항목 10개 제한이 아님).

## 2순위: 요약 + 스레드 상세 (Thread-as-detail)

부모 메시지에는 요약·Top-N만, 전체 목록은 스레드 답글로. PagerDuty(채널 홍수 방지), Wrangle(승인 상세), Sourcegraph(후속 Q&A)가 쓰는 검증된 운영 패턴이다 `[문서]`.

```
부모:  🔍 "배포 실패" 검색 결과 30건 — 상위 3건
       1. … 2. … 3. …
       (스레드에 전체 30건)
답글:  4~30건 전체 목록 (여러 메시지로 분할 가능)
```

## 3순위: 스니펫 업로드 (File spillover)

로그·JSON·diff 같은 원문은 파일로 올리면 슬랙이 **프리뷰를 접어서** 보여준다 `[실측 ✅ T25]`. 1MB까지 `[문서]`. `03-artifact-preview.md` 참조.

## 그 외 대안 (비교표)

| 방법 | 적합 | 한계 | 검증 |
|---|---|---|---|
| container 블록 | 목록·보조 정보 접기 | 자식 10개 | [실측 ✅] |
| 스레드 상세 | 대화 맥락 유지 | 스레드를 열어야 함 | [실측 ✅(운영 패턴)] |
| 스니펫 | 원문 텍스트/코드 | 인라인 가독성 낮음 | [실측 ✅ T25] |
| `section`의 `expand:false` (기본) | AI Assistant 앱의 장문 | 클라이언트가 'see more'로 자동 접음. 임계값 미공개 | [문서] — `expand:true`는 수락 확인 `[실측 ✅ T41]`, 접힘 트리거는 [미검증] |
| 모달 "자세히 보기" 버튼 | 100블록까지 필요 | 백엔드 필수 | [문서] |
| 메시지 분할 | 순차 로그 | 알림 피로 | [문서] |
| 요약 + 외부 링크 | 대시보드 있는 경우 | 슬랙 이탈 | [문서 — Sourcegraph TL;DR 패턴] |
| ``` 코드펜스 | diff/로그 짧을 때 | 시각적으로만 작음 | [문서 — 커뮤니티] |

## 스레드 동작

- 접기의 목적은 **채널을 스캔 가능하게 유지하는 것**. 부모 메시지는 항상 "결론·요약·다음 액션"만 보이게 설계한다.
- container 안 내용이 갱신되면 `chat.update`로 title의 건수를 맞춘다("검색 결과 30건").
- 완료 후에는 verbose한 상태 메시지를 짧은 기록으로 압축하는 condense-on-completion 패턴 (`01` 케이스의 resolved state와 동일) `[문서]`.

## 주의점

- **메시지 하드 한도**: blocks 50개 `[실측 ✅ T17]`, section 텍스트 3000자 `[실측 ✅ T16]`, 메시지 text 40,000자(초과 시 `message_truncated` 경고와 함께 잘림) `[문서]`. 실측으로 4,024자는 온전히 저장됨 `[실측 ✅ T19]`.
- 커뮤니티에 "~4,000자 자동 분할" 관측이 있으나 비공식 `[미검증 — SO 관측치]`.
- 긴 평문(text)은 클라이언트가 "Show more"로 접어 보여주지만(실측 화면에서 확인), **블록 메시지의 접힘은 container가 유일한 공식 수단**이다.
- markdown 블록 합산 12,000자 `[문서]`.

## 검증 상태

- container 접기 전 과정: `[실측 ✅ T30]`
- 스니펫·50블록·3000자·4024자 저장: `[실측 ✅ T16~T19, T25]`
- expand 자동 접힘 임계값: `[미검증]` (클라이언트가 결정, 공식 임계값 없음)

## 출처

- container 블록: https://docs.slack.dev/reference/block-kit/blocks/container-block , https://docs.slack.dev/changelog/2026/06/29/block-kit-container-block
- section expand: https://docs.slack.dev/reference/block-kit/blocks/section-block
- PagerDuty 스레드 전략: https://www.pagerduty.com/blog/incident-management-response/pagerdutys-slack-app-just-got-a-whole-lot-better-and-were-just-getting-started/
- 긴 메시지 우회 총정리(SO): https://stackoverflow.com/questions/54048384/
- 실측: `references/verified-matrix.md` T16~T20, T25, T30, T41
