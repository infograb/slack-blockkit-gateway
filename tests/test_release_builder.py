from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts/build-plugin-release.py"
ARCHIVE_ROOT = "slack-blockkit-gateway-1.0.0"
REQUIRED = {
    f"{ARCHIVE_ROOT}/plugin.yaml",
    f"{ARCHIVE_ROOT}/__init__.py",
    f"{ARCHIVE_ROOT}/LICENSE",
    f"{ARCHIVE_ROOT}/README.md",
    f"{ARCHIVE_ROOT}/after-install.md",
    f"{ARCHIVE_ROOT}/skill/slack-blockkit/SKILL.md",
    f"{ARCHIVE_ROOT}/skill/slack-blockkit/scripts/check_package.py",
    f"{ARCHIVE_ROOT}/skill/slack-blockkit/scripts/validate_payload.py",
}
FORBIDDEN_PARTS = {
    "/tests/",
    "/verification/",
    "/references/screenshots/",
    "/__pycache__/",
    "/.git/",
    "/dist/",
    "/.DS_Store",
}
SECRET_PATTERN = re.compile(r"(?:xox[a-z]|xapp)-[A-Za-z0-9-]{10,}")
PRIVATE_IDENTIFIER = "T0" + "PRIVATE0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build(output: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(BUILDER), "--output", str(output)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

def load_builder_module():
    spec = importlib.util.spec_from_file_location("plugin_release_builder", BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load release builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseBuilderTest(unittest.TestCase):
    def test_builder_uses_public_plugin_subdirectory(self):
        builder = load_builder_module()
        self.assertEqual(builder.PLUGIN_ROOT, ROOT / "plugin")
        self.assertEqual(
            builder.SKILL_ROOT,
            ROOT / "plugin/skill/slack-blockkit",
        )

    def test_builds_public_safe_installable_archives(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            result = build(output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            zip_path = output / f"{ARCHIVE_ROOT}.zip"
            tar_path = output / f"{ARCHIVE_ROOT}.tar.gz"
            sums_path = output / "SHA256SUMS"
            self.assertTrue(zip_path.is_file())
            self.assertTrue(tar_path.is_file())
            self.assertTrue(sums_path.is_file())

            with zipfile.ZipFile(zip_path) as archive:
                names = set(archive.namelist())
                self.assertTrue(REQUIRED <= names)
                self.assertFalse(
                    [name for name in names if any(part in name for part in FORBIDDEN_PARTS)]
                )
                plugin_yaml = archive.read(f"{ARCHIVE_ROOT}/plugin.yaml").decode()
                self.assertIn("author: InfoGrab", plugin_yaml)
                self.assertIn("license: MIT", plugin_yaml)
                for name in names:
                    if Path(name).suffix not in {".md", ".txt", ".py", ".yaml", ".json", ".js"}:
                        continue
                    text = archive.read(name).decode("utf-8")
                    self.assertNotIn(PRIVATE_IDENTIFIER, text, name)
                    self.assertIsNone(SECRET_PATTERN.search(text), name)
                    self.assertNotIn("/Users/", text, name)

            with tarfile.open(tar_path, "r:gz") as archive:
                names = {member.name for member in archive.getmembers() if member.isfile()}
                self.assertTrue(REQUIRED <= names)
                self.assertFalse(
                    [name for name in names if any(part in name for part in FORBIDDEN_PARTS)]
                )

            expected_lines = {
                f"{sha256(tar_path)}  {tar_path.name}",
                f"{sha256(zip_path)}  {zip_path.name}",
            }
            self.assertEqual(set(sums_path.read_text().splitlines()), expected_lines)

    def test_public_scan_covers_slack_tokens_and_home_paths(self):
        builder = load_builder_module()

        for token in (
            "xox" + "b-1234567890-abcdefghijklmnop",
            "xox" + "c-1234567890-abcdefghijklmnop",
            "xapp" + "-1-ABCDEFGHIJ-abcdefghijklmnop",
        ):
            self.assertIsNotNone(builder.SECRET_RE.search(token), token)

        for path in (
            "/Users/alice/project/file.txt",
            "/home/alice/project/file.txt",
            "C:\\Users\\alice\\project\\file.txt",
            "D:/Users/alice/project/file.txt",
        ):
            self.assertIsNotNone(builder.ABSOLUTE_HOME_RE.search(path), path)

    def test_fixed_release_files_reject_symlinks(self):
        builder = load_builder_module()
        original = builder.SOURCE_FILES
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "private-source.txt"
            target.write_text("private")
            linked = Path(tmp) / "plugin.yaml"
            linked.symlink_to(target)
            builder.SOURCE_FILES = {linked: Path("plugin.yaml")}
            try:
                with self.assertRaisesRegex(ValueError, "symlink"):
                    builder.public_files()
            finally:
                builder.SOURCE_FILES = original

    def test_archives_use_frozen_scanned_bytes(self):
        builder = load_builder_module()
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "guide.md"
            source.write_text("safe release content")
            frozen = builder.freeze_public_files([(source, Path("guide.md"))])
            source.write_text("xapp" + "-1-ABCDEFGHIJ-abcdefghijklmnop")
            archive_path = Path(tmp) / "release.zip"
            builder.write_zip(archive_path, "plugin-1.0.0", frozen)
            with zipfile.ZipFile(archive_path) as archive:
                self.assertEqual(
                    archive.read("plugin-1.0.0/guide.md"),
                    b"safe release content",
                )

    def test_archives_are_reproducible(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_result = build(Path(first))
            second_result = build(Path(second))
            self.assertEqual(first_result.returncode, 0, first_result.stdout + first_result.stderr)
            self.assertEqual(second_result.returncode, 0, second_result.stdout + second_result.stderr)
            for filename in (
                f"{ARCHIVE_ROOT}.zip",
                f"{ARCHIVE_ROOT}.tar.gz",
            ):
                self.assertEqual(sha256(Path(first) / filename), sha256(Path(second) / filename))


if __name__ == "__main__":
    unittest.main()
