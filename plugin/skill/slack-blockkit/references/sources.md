# 출처 (Sources)

> 인용 원칙: 공식 문서(docs.slack.dev) > 공식 changelog > 벤더 엔지니어링 블로그 > 커뮤니티(SO/블로그). 홍보성 주장은 사실로 쓰지 않고 "사례"로만 인용.

## Slack 공식 문서 — Block Kit 레퍼런스

- Block Kit 홈: https://docs.slack.dev/block-kit/
- 블록 총괄: https://docs.slack.dev/reference/block-kit/blocks/
- 개별 블록: actions https://docs.slack.dev/reference/block-kit/blocks/actions-block · alert https://docs.slack.dev/reference/block-kit/blocks/alert-block · card https://docs.slack.dev/reference/block-kit/blocks/card-block · carousel https://docs.slack.dev/reference/block-kit/blocks/carousel-block · container https://docs.slack.dev/reference/block-kit/blocks/container-block · context https://docs.slack.dev/reference/block-kit/blocks/context-block · context_actions https://docs.slack.dev/reference/block-kit/blocks/context-actions-block · data_table https://docs.slack.dev/reference/block-kit/blocks/data-table-block · data_visualization https://docs.slack.dev/reference/block-kit/blocks/data-visualization-block · divider https://docs.slack.dev/reference/block-kit/blocks/divider-block · file https://docs.slack.dev/reference/block-kit/blocks/file-block · header https://docs.slack.dev/reference/block-kit/blocks/header-block · image https://docs.slack.dev/reference/block-kit/blocks/image-block · input https://docs.slack.dev/reference/block-kit/blocks/input-block · markdown https://docs.slack.dev/reference/block-kit/blocks/markdown-block · plan https://docs.slack.dev/reference/block-kit/blocks/plan-block · rich_text https://docs.slack.dev/reference/block-kit/blocks/rich-text-block · section https://docs.slack.dev/reference/block-kit/blocks/section-block · table https://docs.slack.dev/reference/block-kit/blocks/table-block · task_card https://docs.slack.dev/reference/block-kit/blocks/task-card-block · video https://docs.slack.dev/reference/block-kit/blocks/video-block
- 엘리먼트 총괄: https://docs.slack.dev/reference/block-kit/block-elements/ (button https://docs.slack.dev/reference/block-kit/block-elements/button-element · checkboxes https://docs.slack.dev/reference/block-kit/block-elements/checkboxes-element · overflow https://docs.slack.dev/reference/block-kit/block-elements/overflow-menu-element · select https://docs.slack.dev/reference/block-kit/block-elements/select-menu-element · multi-select https://docs.slack.dev/reference/block-kit/block-elements/multi-select-menu-element · feedback_buttons https://docs.slack.dev/reference/block-kit/block-elements/feedback-buttons-element · icon_button https://docs.slack.dev/reference/block-kit/block-elements/icon-button-element · radio https://docs.slack.dev/reference/block-kit/block-elements/radio-button-group-element · datepicker https://docs.slack.dev/reference/block-kit/block-elements/date-picker-element · timepicker https://docs.slack.dev/reference/block-kit/block-elements/time-picker-element · datetimepicker https://docs.slack.dev/reference/block-kit/block-elements/datetime-picker-element · plain_text_input https://docs.slack.dev/reference/block-kit/block-elements/plain-text-input-element · rich_text_input https://docs.slack.dev/reference/block-kit/block-elements/rich-text-input-element · file_input https://docs.slack.dev/reference/block-kit/block-elements/file-input-element · workflow_button https://docs.slack.dev/reference/block-kit/block-elements/workflow-button-element · url source https://docs.slack.dev/reference/block-kit/block-elements/url-source-element)
- composition: text https://docs.slack.dev/reference/block-kit/composition-objects/text-object · confirm https://docs.slack.dev/reference/block-kit/composition-objects/confirmation-dialog-object · option https://docs.slack.dev/reference/block-kit/composition-objects/option-object · option group https://docs.slack.dev/reference/block-kit/composition-objects/option-group-object
- mrkdwn 포맷팅: https://docs.slack.dev/messaging/formatting-message-text
- interaction payload: https://docs.slack.dev/reference/interaction-payloads/block_actions-payload
- surfaces: https://docs.slack.dev/surfaces/modals
- 파일: https://docs.slack.dev/messaging/working-with-files · https://docs.slack.dev/reference/methods/files.upload

## Slack 공식 문서 — AI/에이전트

- AI 허브: https://docs.slack.dev/ai/
- 에이전트 개발: https://docs.slack.dev/ai/developing-agents
- 에이전트 거버넌스: https://docs.slack.dev/ai/agent-governance
- 에이전트 디자인 원칙: https://docs.slack.dev/concepts/agent-design , https://docs.slack.dev/ai/agents
- 디자인 가이드: https://docs.slack.dev/concepts/designing-with-block-kit , https://docs.slack.dev/concepts/app-design
- 스트리밍 메서드: https://docs.slack.dev/reference/methods/chat.startStream/ · https://docs.slack.dev/reference/methods/chat.appendStream/ · https://docs.slack.dev/reference/methods/chat.stopStream/
- 상태: https://docs.slack.dev/reference/methods/assistant.threads.setStatus/ · https://docs.slack.dev/reference/methods/agents.sessions.setStatus · https://docs.slack.dev/ai/agent-sessions
- suggested prompts: https://docs.slack.dev/reference/methods/assistant.threads.setSuggestedPrompts/
- 메시지 메타데이터: https://docs.slack.dev/messaging/message-metadata/
- Marketplace 정책: https://docs.slack.dev/slack-marketplace/slack-marketplace-app-guidelines-and-requirements

## Slack changelog (시점 근거)

- 2018 메시지 40k 잘림: https://docs.slack.dev/changelog/2018-truncating-really-long-messages
- 2023-09-29 rich_text: https://docs.slack.dev/changelog/2023/09/29/block-kit
- 2024-09-16 Agents & AI Apps: https://docs.slack.dev/changelog/2024/09/16/apps
- 2025-02-03 markdown 블록: https://docs.slack.dev/changelog/2025/02/03/block-kit-markdown
- 2025-08-14 table 블록: https://docs.slack.dev/changelog/2025/08/14/block-kit-table-block
- 2025-10-07 스트리밍+feedback: https://docs.slack.dev/changelog/2025/10/7/chat-streaming
- 2025-10-22 Work Objects: https://docs.slack.dev/changelog/2025/10/22/work-objects
- 2026-02-11 plan/task_card: https://docs.slack.dev/changelog/2026/02/11/task-cards-plan-blocks
- 2026-03-05 setStatus 스코프: https://docs.slack.dev/changelog/2026/03/05/set-status-scope-update
- 2026-03-06 rich text 확장: https://docs.slack.dev/changelog/2026/03/06/block-kit-rich-text
- 2026-04-16 alert/card/carousel: https://docs.slack.dev/changelog/2026/04/16/block-kit-new-blocks
- 2026-05-20 data_table: https://docs.slack.dev/changelog/2026/05/20/block-kit-more-new-blocks
- 2026-06-16 data_visualization: https://docs.slack.dev/changelog/2026/06/16/block-kit-data-visualization-block
- 2026-06-29 container: https://docs.slack.dev/changelog/2026/06/29/block-kit-container-block
- 2026-06-30 agent_view: https://docs.slack.dev/changelog/2026/06/30/agent-messages-tab
- 2026-08-20 Agent Sessions/stop/Slack Code: https://docs.slack.dev/changelog/2026/08/20/agent-updates · https://docs.slack.dev/changelog/2026/08/20/slack-code

## 프로덕션 패턴 (벤더·커뮤니티)

- HumanLayer 승인 카드 실물 스크린샷: https://github.com/humanlayer/humanlayer/blob/main/docs/images/slack-conversation.png · 문서(아카이브): https://web.archive.org/web/2025/https://humanlayer.dev/docs/channels/slack
- LangSmith Fleet 슬랙 앱: https://docs.langchain.com/langsmith/fleet/slack-app
- GitHub Actions slack-approval: https://github.com/marketplace/actions/slack-approval
- n8n Send and Wait 패턴 해설: https://humangent.io/blog/n8n-slack-approval-workflow
- Wrangle 승인 워크플로: https://www.wrangle.io/post/managing-approval-workflows-in-slack
- StackAI HITL 설계: https://www.stackai.com/insights/human-in-the-loop-ai-agents-how-to-design-approval-workflows-for-safe-and-scalable-automation
- Sleuth reacji 배포 승인: https://www.sleuth.io/post/approve-deploys-via-slack/
- AOF approval workflow: https://docs.aof.sh/docs/guides/approval-workflow
- Slack 남부 에스컬레이션 봇: https://slack.engineering/empowering-engineers-with-ai/
- CopilotKit 슬랙 채널: https://docs.copilotkit.ai/slack/langgraph-python/interactive
- CircleCI 승인 봇 구현기: https://medium.com/mj-studio/approve-your-circle-ci-jobs-manually-with-slack-481662ece925
- incident.io 모달 운영: https://incident.io/blog/slack-previews
- PagerDuty 스레드 전략: https://www.pagerduty.com/blog/incident-management-response/pagerdutys-slack-app-just-got-a-whole-lot-better-and-were-just-getting-started/
- Sourcegraph Deep Search 교훈: https://sourcegraph.com/blog/deep-search-slack-agent-lessons
- Linear 슬랙 연동: https://linear.app/docs/slack
- 알림 디자인(Knock): https://knock.app/blog/the-guide-to-designing-slack-notifications
- ephemeral 패턴(Knock): https://knock.app/blog/using-slack-ephemeral-messages-in-product-notifications
- Beep Boop 교훈: https://medium.com/slack-developer-blog/lessons-learned-from-beep-boops-new-slack-bot-bd250e8d9887
- 공식 Block Kit 템플릿 예시 모음: https://pkg.go.dev/github.com/slack-go/slack/examples/blocks
- Block Kit 소개(2019 배경): https://www.smashingmagazine.com/2019/03/block-kit-slack-collaboration-ui

## 커뮤니티 Q&A (비공식 관측 — [미검증] 표기 원칙)

- 긴 메시지/자동 분할: https://stackoverflow.com/questions/54048384/
- 블록 메시지 접기 불가 논의: https://stackoverflow.com/questions/57101340/intentionally-collapsing-long-messages-with-slack-api · https://stackoverflow.com/questions/67798323/i-want-to-show-show-more-in-slack-messages
- 표 렌더 핵(2025 이전): https://stackoverflow.com/questions/59006831/how-to-render-tables-in-slack
- 봇 링크 언펄: https://stackoverflow.com/questions/64262646/
- markdown 블록 12,000자 관측: https://github.com/slackapi/bolt-js/issues/2509
- typing indicator 부재: https://github.com/slackapi/bolt-js/issues/885
- ephemeral+DM 패턴: https://github.com/slackapi/bolt-js/issues/1030
- Jira→Slack 접기 레시피: https://community.atlassian.com/forums/Jira-questions/Collapsed-Message-to-Slack-Channel/qaq-p/2988168
- Slack 파일 프리뷰 픽셀 제한: https://slack.com/help/articles/201330736-Add-files-to-Slack

## 실측 기반 (1차)

- InfoGrab 테스트 워크스페이스 실측 T01~T42 (2026-08-24) — 공개 패키지에는 `references/verified-matrix.md`의 텍스트 결과만 포함

## Hermes Agent (공식)

- Plugins: https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins
- Build a Hermes Plugin: https://hermes-agent.nousresearch.com/docs/developer-guide/plugins
- Slack Gateway: https://hermes-agent.nousresearch.com/docs/user-guide/messaging/slack
- Event Hooks: https://hermes-agent.nousresearch.com/docs/user-guide/features/hooks
- Slack Block Kit renderer source: https://github.com/NousResearch/hermes-agent/blob/main/plugins/platforms/slack/block_kit.py
- Slack Gateway adapter source: https://github.com/NousResearch/hermes-agent/blob/main/plugins/platforms/slack/adapter.py
