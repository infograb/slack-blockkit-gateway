# 성능 검증

## 2026-08-27 실측

환경: macOS, Python 3.11 계열, Hermes Slack `render_blocks`/`sanitize_blocks`, `time.perf_counter`, `tracemalloc`. 네트워크 시간은 제외했다.

| 케이스 | 반복 | 평균 | p95 | p99 | peak memory |
|---|---:|---:|---:|---:|---:|
| 작은 Markdown | 2,000 | 0.0813 ms | 0.1166 ms | 0.1386 ms | 200.8 KiB |
| 중간 Markdown(표·목록·코드 반복) | 1,000 | 0.7743 ms | 0.8566 ms | 0.9262 ms | 197.6 KiB |
| table 최대형 100×20 생성 | 200 | 2.0122 ms | 2.0418 ms | 2.0487 ms | 217.6 KiB |
| 50-block sanitize | 2,000 | 0.0163 ms | 0.0176 ms | 0.0208 ms | 61.2 KiB |

## 판정

- renderer/sanitizer는 p95 2.1ms 이하로, Slack API 네트워크 왕복에 비해 무시 가능한 수준이다.
- 최대 table 생성의 peak memory도 218 KiB 미만이었다.
- 현 시점에서 CPU·메모리 병목은 관찰되지 않았다.
- 운영 병목 후보는 renderer가 아니라 Slack API rate limit, 네트워크, 이미지/파일 업로드, options-load 백엔드다.

## 회귀 기준

- 작은/중간 메시지 renderer p95가 10ms를 넘거나 이전 기준의 2배를 넘으면 조사한다.
- 최대 table 또는 50-block sanitize가 25ms를 넘으면 조사한다.
- fallback 재시도는 block 거부 때 HTTP 요청이 한 번 더 발생한다. 정상 payload에서는 재시도가 없어야 한다.
- 외부 select는 Options Load URL 왕복이 사용자 체감 성능을 좌우한다. 3초 이내 ACK와 캐시 전략을 별도로 운영한다.
