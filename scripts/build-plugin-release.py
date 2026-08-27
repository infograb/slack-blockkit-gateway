#!/usr/bin/env python3
"""Build reproducible, public-safe Hermes plugin release archives."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import stat
from typing import Iterable
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugin"
MANIFEST = PLUGIN_ROOT / "plugin.yaml"
SOURCE_FILES = {
    PLUGIN_ROOT / "plugin.yaml": Path("plugin.yaml"),
    PLUGIN_ROOT / "__init__.py": Path("__init__.py"),
    PLUGIN_ROOT / "LICENSE": Path("LICENSE"),
    PLUGIN_ROOT / "after-install.md": Path("after-install.md"),
    ROOT / "docs/hermes-plugin.md": Path("README.md"),
}
SKILL_ROOT = PLUGIN_ROOT / "skill/slack-blockkit"
TEXT_SUFFIXES = {".md", ".txt", ".py", ".yaml", ".yml", ".json", ".js"}
FORBIDDEN_NAMES = {".DS_Store", "__pycache__"}
FORBIDDEN_PARTS = {"tests", "verification", "screenshots", "__pycache__", ".git", "dist"}
SECRET_RE = re.compile(r"(?:xox[a-z]|xapp)-[A-Za-z0-9-]{10,}")
WORKSPACE_ID_RE = re.compile(r"\bT[A-Z0-9]{8,}\b")
ABSOLUTE_HOME_RE = re.compile(
    r"(?:/Users/[^/\s]+/|/home/[^/\s]+/|[A-Za-z]:[\\/]+Users[\\/]+[^\\/\s]+[\\/])"
)
VERSION_RE = re.compile(r"(?m)^version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$")
NAME_RE = re.compile(r"(?m)^name:\s*([a-z0-9-]+)\s*$")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)

SourceFile = tuple[Path, Path]
FrozenFile = tuple[Path, bytes]


def manifest_value(pattern: re.Pattern[str], label: str, text: str) -> str:
    match = pattern.search(text)
    if not match:
        raise ValueError(f"plugin.yaml missing valid {label}")
    return match.group(1)


def public_files() -> list[tuple[Path, Path]]:
    files: list[tuple[Path, Path]] = []
    for source, destination in SOURCE_FILES.items():
        if source.is_symlink():
            raise ValueError(
                f"release files must not be symlinks: {source}"
            )
        if not source.is_file():
            raise FileNotFoundError(f"required release file missing: {source}")
        files.append((source, destination))

    if not SKILL_ROOT.is_dir():
        raise FileNotFoundError(
            "required release directory missing: plugin/skill/slack-blockkit"
        )
    for source in sorted(SKILL_ROOT.rglob("*")):
        if source.is_dir():
            continue
        relative = source.relative_to(PLUGIN_ROOT)
        if source.is_symlink():
            raise ValueError(f"release files must not be symlinks: {relative}")
        if source.name in FORBIDDEN_NAMES or any(part in FORBIDDEN_PARTS for part in relative.parts):
            continue
        files.append((source, relative))
    return sorted(files, key=lambda item: item[1].as_posix())

def freeze_public_files(files: Iterable[SourceFile]) -> list[FrozenFile]:
    frozen: list[FrozenFile] = []
    for source, destination in files:
        before = os.stat(source, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise ValueError(f"release source is not a regular file: {source}")
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        descriptor = os.open(source, flags)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode) or not os.path.samestat(before, opened):
                raise ValueError(f"release source changed during capture: {source}")
            data = bytearray()
            while chunk := os.read(descriptor, 1024 * 1024):
                data.extend(chunk)
        finally:
            os.close(descriptor)
        frozen.append((destination, bytes(data)))
    return frozen


def scan_public_content(files: Iterable[FrozenFile]) -> None:
    errors: list[str] = []
    for destination, data in files:
        if destination.suffix.lower() not in TEXT_SUFFIXES and destination.name != "LICENSE":
            errors.append(f"unexpected binary/non-text release file: {destination}")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"release file is not UTF-8 text: {destination}")
            continue
        if SECRET_RE.search(text):
            errors.append(f"Slack token-shaped secret found: {destination}")
        if WORKSPACE_ID_RE.search(text):
            errors.append(f"Slack workspace ID found: {destination}")
        if ABSOLUTE_HOME_RE.search(text):
            errors.append(f"absolute user path found: {destination}")
    if errors:
        raise ValueError("public release scan failed:\n- " + "\n- ".join(errors))


def mode_for(path: Path) -> int:
    if path.suffix == ".py" and "scripts" in path.parts:
        return 0o755
    return 0o644


def write_zip(path: Path, archive_root: str, files: list[FrozenFile]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative, data in files:
            name = f"{archive_root}/{relative.as_posix()}"
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100000 | mode_for(relative)) << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def write_tar(path: Path, archive_root: str, files: list[FrozenFile]) -> None:
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=9) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as archive:
                for relative, data in files:
                    info = tarfile.TarInfo(f"{archive_root}/{relative.as_posix()}")
                    info.size = len(data)
                    info.mode = mode_for(relative)
                    info.mtime = 0
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    archive.addfile(info, io.BytesIO(data))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def run_skill_check() -> None:
    result = subprocess.run(
        [sys.executable, str(SKILL_ROOT / "scripts/check_package.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)


def build(output: Path) -> tuple[Path, Path, Path]:
    run_skill_check()
    source_files = public_files()
    files = freeze_public_files(source_files)
    scan_public_content(files)
    manifest_text = next(
        data.decode("utf-8")
        for relative, data in files
        if relative == Path("plugin.yaml")
    )
    name = manifest_value(NAME_RE, "name", manifest_text)
    version = manifest_value(VERSION_RE, "version", manifest_text)
    archive_root = f"{name}-{version}"

    output.mkdir(parents=True, exist_ok=True)
    zip_path = output / f"{archive_root}.zip"
    tar_path = output / f"{archive_root}.tar.gz"
    sums_path = output / "SHA256SUMS"
    for path in (zip_path, tar_path, sums_path):
        path.unlink(missing_ok=True)

    write_zip(zip_path, archive_root, files)
    write_tar(tar_path, archive_root, files)
    sums_path.write_text(
        f"{digest(tar_path)}  {tar_path.name}\n{digest(zip_path)}  {zip_path.name}\n",
        encoding="utf-8",
    )
    return zip_path, tar_path, sums_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    try:
        artifacts = build(args.output.resolve())
    except Exception as error:
        print(f"ERROR {error}", file=sys.stderr)
        return 1
    for artifact in artifacts:
        print(f"OK {artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
