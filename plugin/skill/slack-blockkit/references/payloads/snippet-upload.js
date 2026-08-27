// 통합 예시: 독립 실행 프로그램이 아니다.
// 호스트가 @slack/web-api의 인증된 WebClient를 `client`로 제공해야 한다.
// 필요 권한: files:write. 채널 루트에 올릴 때는 thread_ts를 제거한다.
// 스니펫 업로드 — 긴 코드/로그 산출물의 정석 (실측 T25)
// files.upload는 2025-11-12 종료 → SDK filesUploadV2(내부적으로 getUploadURLExternal+completeUploadExternal) 사용
await client.filesUploadV2({
  channel_id: '<CHANNEL_ID>',
  thread_ts: '<THREAD_TS>',        // 스레드 안에 넣을 때
  initial_comment: '배포 로그 — 실패 구간은 42행부터',
  file_uploads: [
    {
      content: 'def hello():\n    print("blockkit")\n\nhello()\n',
      filename: 'deploy-log.py',
      snippet_type: 'python',       // 구문 강조 프리뷰
      title: 'deploy-log.py — 에이전트 생성 산출물'
    }
  ]
});
// 제한: 스니펫 1MB. 슬랙이 프리뷰를 접어서 보여주고 클릭 시 전문 열림.
