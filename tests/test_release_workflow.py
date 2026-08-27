from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/plugin-release.yml"
USES_RE = re.compile(r"(?m)^\s*- uses:\s*([^@\s]+)@([^\s#]+)")
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ReleaseWorkflowTest(unittest.TestCase):
    def test_actions_are_pinned_to_full_commit_shas(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        uses = USES_RE.findall(text)
        self.assertTrue(uses)
        for action, reference in uses:
            self.assertRegex(reference, FULL_SHA_RE, action)

    def test_tag_release_has_provenance_and_repository_context(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("actions/attest-build-provenance", text)
        self.assertIn("attestations: write", text)
        self.assertIn("id-token: write", text)
        self.assertIn("subject-path:", text)
        self.assertIn('--repo "${GITHUB_REPOSITORY}"', text)
        self.assertIn('yaml.safe_load(open("plugin/plugin.yaml"))["version"]', text)


    def test_oidc_authority_is_isolated_from_build_code(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        verify_job = text.split("  verify:", 1)[1].split("  attest:", 1)[0]
        self.assertNotIn("id-token: write", verify_job)
        self.assertNotIn("attestations: write", verify_job)

        attest_job = text.split("  attest:", 1)[1].split("  release:", 1)[0]
        self.assertIn("needs: verify", attest_job)
        self.assertIn("id-token: write", attest_job)
        self.assertIn("attestations: write", attest_job)

    def test_hermes_is_installed_from_pinned_editable_checkout(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("git clone --filter=blob:none", text)
        self.assertIn('checkout "${HERMES_REF}"', text)
        self.assertIn("python -m pip install -e /tmp/hermes-agent", text)
        self.assertNotIn("git+https://github.com/NousResearch/hermes-agent", text)

    def test_ci_scans_the_installable_plugin_subdirectory(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("hermes plugins doctor plugin --ci", text)
        self.assertIn('scan_plugin(Path("plugin")', text)
        self.assertIn('result.verdict != "safe"', text)

    def test_release_publication_is_idempotent(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('gh release view "${GITHUB_REF_NAME}"', text)
        self.assertIn("gh release upload", text)
        self.assertIn("--clobber", text)
        self.assertIn("gh release create", text)

if __name__ == "__main__":
    unittest.main()
