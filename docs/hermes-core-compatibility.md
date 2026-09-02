# Hermes core compatibility patch

`slack-blockkit-gateway` itself does not own Slack credentials or replace Hermes' Slack platform adapter. Two issues found during xoxb E2E therefore require a Hermes core change:

1. `hermes send` standalone delivery used fallback `text` only and dropped blocks produced by the Slack renderer.
2. native Task Card progress supplied both `chunks` and `markdown_text` to `chat.appendStream`, which Slack rejects with `cannot_provide_both_markdown_text_and_chunks`.

Both issues are still present in Hermes v0.21.0 (upstream `c5c9aa8d44`), so this patch remains required.

The reviewed patch is stored at:

```text
patches/hermes-slack-rich-blocks.patch
```

It adds standalone Block Kit rendering with text fallback, makes Task Card stream fields mutually exclusive, and adds regression tests.

Version history:

- v0.20.x base: generated from local Hermes commit `34db0e9619` (`fix(slack): render standalone Block Kit and repair task streams`).
- v0.21.0 base (current): regenerated from rebased commit `3f00c37cea` on upstream main `c5c9aa8d44` (Hermes v0.21.0, 2026.8.31). One context conflict from the rebase (upstream-added `**unfurl_kwargs` in the standalone payload) was resolved by preserving both `unfurl_kwargs` and the new `blocks` key. The file is now a standard unified diff that `git apply` accepts directly.

## Verification performed

Against Hermes v0.21.0 (upstream `c5c9aa8d44`):

- `git apply --check patches/hermes-slack-rich-blocks.patch`: OK
- `tests/gateway/test_slack.py` + `tests/tools/test_send_message_slack.py`: 239 passed

Against the original v0.20.x base (historical):

- `tests/tools/test_send_message_slack.py`: 4 passed
- `tests/gateway/test_slack.py`: 166 passed
- combined relevant suite: 170 passed
- actual standalone xoxb post: API `ok:true`, readback contained `header`, `table`, `rich_text`, `context_actions`
- no new `invalid_blocks`, `msg_blocks_too_long`, or `msg_too_long` in the verification interval

Note: the v0.21.0 verification above is a code/test-level check. A live standalone xoxb post against v0.21.0 has not been re-run.

## Apply to a compatible Hermes checkout

```bash
git apply --check /path/to/slack-blockkit-gateway/patches/hermes-slack-rich-blocks.patch
git apply /path/to/slack-blockkit-gateway/patches/hermes-slack-rich-blocks.patch
```

The patch targets Hermes v0.21.0 (`c5c9aa8d44`). On other revisions, expect context drift in `plugins/platforms/slack/adapter.py` and rebase instead of forcing the apply.

Run the two regression suites before deploying. A long-running Gateway must be restarted from outside its own process before the Task Card fix becomes active. Applying the patch dirties the Hermes checkout, which blocks unattended `hermes update` runs; prefer carrying it on a dedicated branch and rebasing after each update until the fix lands in core.

## Responsibility boundary

This patch is kept in the repository as compatibility evidence and a reproducible handoff. The plugin must not monkey-patch private SlackAdapter methods at runtime. The durable fix belongs in Hermes core or an official outbound-block hook.
