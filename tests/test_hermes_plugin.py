from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugin"
PLUGIN_FILE = PLUGIN_ROOT / "__init__.py"
SKILL_FILE = PLUGIN_ROOT / "skill/slack-blockkit/SKILL.md"


class FakePluginContext:
    def __init__(self) -> None:
        self.skills: list[dict] = []
        self.prompt_sections: list[dict] = []

    def register_skill(self, name, path, description="", frontmatter=None):
        self.skills.append(
            {
                "name": name,
                "path": Path(path),
                "description": description,
                "frontmatter": frontmatter,
            }
        )

    def register_system_prompt_section(
        self, section_id, content, *, position="after_memory", max_chars=2000
    ):
        self.prompt_sections.append(
            {
                "id": section_id,
                "content": content,
                "position": position,
                "max_chars": max_chars,
            }
        )


def load_plugin_module():
    spec = importlib.util.spec_from_file_location(
        "slack_blockkit_gateway_plugin", PLUGIN_FILE
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Hermes plugin module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HermesPluginContractTest(unittest.TestCase):
    def test_registers_bundled_skill_and_prompt_section(self):
        module = load_plugin_module()
        ctx = FakePluginContext()

        module.register(ctx)

        self.assertEqual(len(ctx.skills), 1)
        self.assertEqual(ctx.skills[0]["name"], "slack-blockkit")
        self.assertEqual(ctx.skills[0]["path"], SKILL_FILE)
        self.assertTrue(SKILL_FILE.is_file())

        self.assertEqual(len(ctx.prompt_sections), 1)
        section = ctx.prompt_sections[0]
        self.assertEqual(section["id"], "slack-blockkit.gateway")
        self.assertEqual(section["position"], "after_memory")
        self.assertLessEqual(section["max_chars"], 4000)
        self.assertTrue(callable(section["content"]))

    def test_prompt_is_slack_only_and_routes_to_gateway_renderer(self):
        module = load_plugin_module()
        ctx = FakePluginContext()
        module.register(ctx)
        render = ctx.prompt_sections[0]["content"]

        self.assertEqual(render({"platform": "telegram"}), "")
        self.assertEqual(render({"platform": "cli"}), "")

        guidance = render({"platform": "Slack"})
        self.assertIn("semantic Markdown", guidance)
        self.assertIn("rich_blocks", guidance)
        self.assertIn(
            'skill_view("slack-blockkit-gateway:slack-blockkit")', guidance
        )
        self.assertIn("Do not emit chat.postMessage JSON", guidance)
        self.assertIn("clarify", guidance)

    def test_manifest_has_no_slack_secret_or_privileged_capability_dependency(self):
        manifest = (PLUGIN_ROOT / "plugin.yaml").read_text(encoding="utf-8")

        self.assertIn("name: slack-blockkit-gateway", manifest)
        self.assertIn("manifest_version: 1", manifest)
        self.assertNotIn("manifest_version: 2", manifest)
        self.assertNotIn("requires_env", manifest)
        self.assertNotIn("SLACK_BOT_TOKEN", manifest)
        self.assertNotIn("SLACK_APP_TOKEN", manifest)
        self.assertNotIn("capabilities:", manifest)

    def test_plugin_install_surface_avoids_guard_patterns(self):
        guide = (
            PLUGIN_ROOT / "skill/slack-blockkit/references/hermes-gateway.md"
        ).read_text(encoding="utf-8")
        checker = (
            PLUGIN_ROOT / "skill/slack-blockkit/scripts/check_package.py"
        ).read_text(encoding="utf-8")

        self.assertNotIn("~/.hermes/config.yaml", guide)
        self.assertNotIn("~/.hermes/.env", guide)
        self.assertNotIn("subprocess", checker)

    def test_public_git_install_uses_supported_subdirectory_identifier(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "hermes plugins install infograb/slack-blockkit-gateway/plugin",
            readme,
        )
        self.assertNotIn("--subdir plugin", readme)

    def test_after_install_recommends_only_high_value_defaults(self):
        guidance = (PLUGIN_ROOT / "after-install.md").read_text(encoding="utf-8")
        self.assertIn(
            "platforms.slack.extra.rich_blocks true",
            guidance,
        )
        self.assertIn(
            "platforms.slack.extra.native_task_cards true",
            guidance,
        )
        self.assertIn(
            "platforms.slack.extra.feedback_buttons false",
            guidance,
        )


if __name__ == "__main__":
    unittest.main()
