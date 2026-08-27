# Recommended Slack defaults

Enable the two presentation features that improve normal Hermes Slack work:

```bash
hermes config set platforms.slack.extra.rich_blocks true
hermes config set platforms.slack.extra.native_task_cards true
```

Keep response feedback controls off unless you actively consume the feedback logs:

```bash
hermes config set platforms.slack.extra.feedback_buttons false
```

Why:

- `native_task_cards`: shows live tool work as one updating plan/task card inside the Slack thread. It reduces progress-message noise and Hermes falls back when the native Slack API is unavailable.
- `feedback_buttons`: adds Good Response / Bad Response controls to every final rich reply. Hermes currently acknowledges the click and writes it to logs; it does not aggregate, score, or remove the controls. Enable it only when those logs feed a review process.

Apply the renderer settings with:

```bash
hermes gateway restart
```

Start a new Slack session with `/new` or `/reset` so the plugin prompt section is loaded.
