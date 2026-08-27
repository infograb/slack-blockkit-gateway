#!/usr/bin/env python3
"""Verify that the slack-blockkit skill is complete and self-contained."""

import json
from pathlib import Path
import re

from validate_payload import E, I, W, validate

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_SPAN = re.compile(r"`([^`\n]+)`")
RESOURCE_PREFIXES = ("references/", "scripts/", "agents/")
STALE_PREFIXES = ("verification/", "payloads/", "reference/", "blockkit-agent-guide/")


def inside_root(path: Path) -> bool:
    try:
        path.relative_to(ROOT)
    except ValueError:
        return False
    return True


def check_target(source: Path, raw_target: str, *, root_relative: bool) -> list[str]:
    target_text = raw_target.split("#", 1)[0].strip()
    if not target_text or target_text.startswith(("http://", "https://", "mailto:", "#")):
        return []
    base = ROOT if root_relative else source.parent
    target = (base / target_text).resolve()
    if not inside_root(target):
        return [f"{source.relative_to(ROOT)}: package 밖을 참조함: {raw_target}"]
    if not target.exists():
        return [f"{source.relative_to(ROOT)}: 없는 경로 참조: {raw_target}"]
    return []


def check_markdown(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for target in MARKDOWN_LINK.findall(text):
        target_text = target.split("#", 1)[0].strip()
        if not (
            target_text.startswith(("./", "../"))
            or Path(target_text).suffix in {".md", ".json", ".js", ".py", ".jpeg"}
        ):
            continue
        errors.extend(check_target(path, target, root_relative=False))

    for span in CODE_SPAN.findall(text):
        if span.startswith(STALE_PREFIXES):
            errors.append(f"{path.relative_to(ROOT)}: 이전 볼트 경로가 남음: {span}")
        if span.startswith(RESOURCE_PREFIXES):
            errors.extend(check_target(path, span, root_relative=True))

    return errors


def check_frontmatter() -> list[str]:
    skill = ROOT / "SKILL.md"
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return ["SKILL.md: YAML frontmatter가 없거나 닫히지 않음"]
    frontmatter = match.group(1)
    errors: list[str] = []
    if not re.search(r"(?m)^name:\s*slack-blockkit\s*$", frontmatter):
        errors.append("SKILL.md: name은 폴더명과 같은 slack-blockkit이어야 함")
    if not re.search(r"(?m)^description:\s*.+$", frontmatter):
        errors.append("SKILL.md: description이 없음")
    extra_keys = [
        line.split(":", 1)[0]
        for line in frontmatter.splitlines()
        if re.match(r"^[A-Za-z][A-Za-z0-9_-]*:", line)
        and not line.startswith(("name:", "description:"))
    ]
    if extra_keys:
        errors.append(f"SKILL.md: 허용하지 않은 frontmatter 키: {', '.join(extra_keys)}")
    return errors


def main() -> int:
    errors: list[str] = []
    required = [
        ROOT / "SKILL.md",
        ROOT / "agents/openai.yaml",
        ROOT / "scripts/validate_payload.py",
        ROOT / "references/cases/index.md",
        ROOT / "references/payloads/index.md",
        ROOT / "references/verified-matrix.md",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"필수 리소스 없음: {path.relative_to(ROOT)}")

    errors.extend(check_frontmatter())
    markdown_files = sorted(ROOT.rglob("*.md"))
    for path in markdown_files:
        errors.extend(check_markdown(path))

    payloads = sorted((ROOT / "references/payloads").glob("*.json"))
    if not payloads:
        errors.append("검증할 JSON 페이로드가 없음")
    else:
        for path in payloads:
            E.clear()
            W.clear()
            I.clear()
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"{path.relative_to(ROOT)}: JSON 파싱 실패 — {error}")
                continue
            validate(payload)
            for error in E:
                errors.append(f"{path.relative_to(ROOT)}: {error}")

    screenshots = sorted((ROOT / "references/screenshots").glob("*.jpeg"))
    if screenshots:
        errors.append(
            "공개 skill 패키지에는 개인 DM·워크스페이스 렌더 캡처를 포함하지 않음"
        )

    snippet = (ROOT / "references/payloads/snippet-upload.js").read_text(encoding="utf-8")
    for prerequisite in ("@slack/web-api", "files:write", "client"):
        if prerequisite not in snippet:
            errors.append(f"snippet-upload.js: 실행 전제 누락: {prerequisite}")

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"FAIL slack-blockkit package: {len(errors)} error(s)")
        return 1

    print(
        "OK slack-blockkit package: "
        f"{len(markdown_files)} markdown, {len(payloads)} payloads, "
        f"{len(screenshots)} public screenshots"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
