# Hermes core compatibility patch

`slack-blockkit-gateway` itself does not own Slack credentials or replace Hermes' Slack platform adapter. Two issues found during xoxb E2E therefore require a Hermes core change:

1. `hermes send` standalone delivery used fallback `text` only and dropped blocks produced by the Slack renderer.
2. native Task Card progress supplied both `chunks` and `markdown_text` to `chat.appendStream`, which Slack rejects with `cannot_provide_both_markdown_text_and_chunks`.

The reviewed patch is stored at:

```text
patches/hermes-slack-rich-blocks.patch
```

It adds standalone Block Kit rendering with text fallback, makes Task Card stream fields mutually exclusive, and adds regression tests. It was generated from local Hermes commit `34db0e9619` (`fix(slack): render standalone Block Kit and repair task streams`).

## Verification performed

- `tests/tools/test_send_message_slack.py`: 4 passed
- `tests/gateway/test_slack.py`: 166 passed
- combined relevant suite: 170 passed
- actual standalone xoxb post: API `ok:true`, readback contained `header`, `table`, `rich_text`, `context_actions`
- no new `invalid_blocks`, `msg_blocks_too_long`, or `msg_too_long` in the verification interval

## Apply to a compatible Hermes checkout

```bash
git apply --check /path/to/slack-blockkit-gateway/patches/hermes-slack-rich-blocks.patch
git apply /path/to/slack-blockkit-gateway/patches/hermes-slack-rich-blocks.patch
```

Run the two regression suites before deploying. A long-running Gateway must be restarted from outside its own process before the Task Card fix becomes active.

## Responsibility boundary

This patch is kept in the repository as compatibility evidence and a reproducible handoff. The plugin must not monkey-patch private SlackAdapter methods at runtime. The durable fix belongs in Hermes core or an official outbound-block hook.
