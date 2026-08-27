"""Hermes gateway integration for the bundled Slack Block Kit skill."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


_ROOT = Path(__file__).resolve().parent
_SKILL_FILE = _ROOT / "skill" / "slack-blockkit" / "SKILL.md"

_SLACK_GATEWAY_GUIDANCE = """# Slack Block Kit gateway mode

This session is delivered through the Hermes Slack gateway.

- Write the final reply as semantic Markdown: conclusion first, short headings, compact lists, fenced code, and pipe tables only when they improve scanning.
- Do not emit chat.postMessage JSON unless the user explicitly asks for a Slack API payload. Hermes owns Socket Mode, credentials, text fallback, Block Kit rendering, delivery, retries, and message handles.
- The operator enables `platforms.slack.extra.rich_blocks: true`; keep the Markdown readable even when Hermes falls back to plain mrkdwn.
- Use Hermes `clarify` for choices or approvals. The Slack adapter renders those interactions as native Block Kit controls and handles their lifecycle.
- For Slack-specific limits, thread placement, accessibility, or explicit payload authoring, load `skill_view("slack-blockkit-gateway:slack-blockkit")` before drafting.
- Raw recipes for container, data_table, data_visualization, or custom actions are explicit-payload patterns. Do not claim Hermes automatically materializes them from a normal text reply.
"""


def _gateway_guidance(session_info: Mapping[str, Any]) -> str:
    platform = str(session_info.get("platform", "")).strip().lower()
    if platform != "slack":
        return ""
    return _SLACK_GATEWAY_GUIDANCE


def register(ctx) -> None:
    """Register the read-only skill and Slack-only prompt guidance."""
    ctx.register_skill(
        "slack-blockkit",
        _SKILL_FILE,
        description=(
            "Verified Slack Block Kit patterns, limits, payloads, and local "
            "validation for rich channel messages."
        ),
    )
    ctx.register_system_prompt_section(
        "slack-blockkit.gateway",
        _gateway_guidance,
        position="after_memory",
        max_chars=1800,
    )
