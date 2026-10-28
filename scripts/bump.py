#!/usr/bin/env python3
"""Point Formula/repo-companion.rb at a new upstream release.

Usage:
    scripts/bump.py v0.3.0
    scripts/bump.py v0.3.0 --pr

The formula carries one URL and SHA-256 per supported platform. This script
downloads the release's checksums.txt, rewrites the four stanzas, and leaves the
result in the working tree. With --pr it also commits on a branch, pushes it,
and opens the pull request with gh.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = "repocompanion/companion"
ROOT = Path(__file__).resolve().parent.parent
FORMULA = ROOT / "Formula" / "repo-companion.rb"
PLATFORMS = ("darwin_amd64", "darwin_arm64", "linux_amd64", "linux_arm64")

URL_TEMPLATE = (
    'url "https://github.com/{repo}/releases/download/v{version}/'
    'companion_{version}_{platform}.tar.gz"'
)
URL_RE = re.compile(
    r'^url "https://github\.com/repocompanion/companion/releases/download/'
    r'v[^/"]+/companion_[^_"]+_(darwin|linux)_(amd64|arm64)\.tar\.gz"$'
)
SHA_RE = re.compile(r'^(\s*)sha256 "([0-9a-f]{64})"$')
VERSION_RE = re.compile(r"^v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def fail(message: str) -> "NoReturn":
    sys.exit(f"error: {message}")


def normalize_tag(raw: str) -> str:
    tag = raw.strip()
    if not VERSION_RE.fullmatch(tag):
        fail(f"expected a version like v0.3.0, got {raw!r}")
    return tag[1:] if tag.startswith("v") else tag


def run(*cmd: str) -> str:
    try:
        return subprocess.run(
            cmd, check=True, text=True, capture_output=True
        ).stdout
    except FileNotFoundError:
        fail(f"{cmd[0]} is not installed")
    except subprocess.CalledProcessError as exc:
        fail(f"{' '.join(cmd)} failed:\n{exc.stderr.strip()}")


def fetch_checksums(version: str) -> str:
    url = (
        f"https://github.com/{REPO}/releases/download/v{version}/checksums.txt"
    )
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode()
    except urllib.error.HTTPError as exc:
        fail(f"could not download {url}: HTTP {exc.code} (does the tag exist?)")
    except urllib.error.URLError as exc:
        fail(f"could not download {url}: {exc.reason}")


def parse_checksums(text: str, version: str) -> dict[str, str]:
    expected = {f"companion_{version}_{p}.tar.gz": p for p in PLATFORMS}
    checksums: dict[str, str] = {}
    for line in text.splitlines():
        fields = line.split()
        if len(fields) != 2:
            continue
        checksum, name = fields
        platform = expected.get(name)
        if platform is None:
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", checksum):
            fail(f"{name} has an unexpected checksum {checksum!r}")
        checksums[platform] = checksum
    missing = [name for name in expected if expected[name] not in checksums]
    if missing:
        fail("checksums.txt is missing: " + ", ".join(sorted(missing)))
    return checksums


def rewrite(text: str, version: str, checksums: dict[str, str]) -> str:
    out: list[str] = []
    pending: str | None = None
    seen: set[str] = set()
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\n")
        url_match = URL_RE.match(body.strip())
        if url_match:
            platform = f"{url_match.group(1)}_{url_match.group(2)}"
            if pending is not None or platform in seen:
                fail(f"unexpected second url stanza for {platform}")
            indent = body[: len(body) - len(body.lstrip())]
            out.append(
                indent
                + URL_TEMPLATE.format(repo=REPO, version=version, platform=platform)
                + "\n"
            )
            pending = platform
            continue
        if pending is not None:
            sha_match = SHA_RE.match(body)
            if sha_match:
                out.append(f'{sha_match.group(1)}sha256 "{checksums[pending]}"\n')
                seen.add(pending)
                pending = None
                continue
            if body.strip():
                fail(f"expected a sha256 line after the {pending} url")
        out.append(line)
    if pending is not None:
        fail(f"the {pending} url has no sha256 line")
    missing = [platform for platform in PLATFORMS if platform not in seen]
    if missing:
        fail("the formula has no stanza for: " + ", ".join(missing))
    return "".join(out)


def open_pr(version: str) -> None:
    branch = f"bump/{version}"
    formula_path = str(FORMULA.relative_to(ROOT))
    run("git", "switch", "-c", branch)
    run("git", "add", formula_path)
    run("git", "commit", "-m", f"chore: bump repo-companion to {version}")
    run("git", "push", "-u", "origin", branch)
    body = (
        f"Bumps the formula to the upstream `v{version}` release.\n\n"
        "Checksums come from the release's `checksums.txt`. CI runs "
        "`brew audit --strict --online`, `brew style`, `brew livecheck`, and "
        "install tests on macOS and Linux.\n"
    )
    url = run(
        "gh", "pr", "create",
        "--title", f"repo-companion {version}",
        "--body", body,
    )
    print(url.strip())


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Point Formula/repo-companion.rb at a new upstream release."
    )
    parser.add_argument("tag", help="release tag, for example v0.3.0")
    parser.add_argument(
        "--checksums",
        type=Path,
        help="use a local checksums.txt instead of downloading the release's",
    )
    parser.add_argument(
        "--pr",
        action="store_true",
        help="commit on a branch, push it, and open the pull request",
    )
    args = parser.parse_args(argv)

    version = normalize_tag(args.tag)
    if not FORMULA.exists():
        fail(f"{FORMULA} does not exist")
    if args.pr and run("git", "status", "--porcelain").strip():
        fail("the working tree is dirty; commit or stash first")

    checksum_text = (
        args.checksums.read_text() if args.checksums else fetch_checksums(version)
    )
    checksums = parse_checksums(checksum_text, version)

    original = FORMULA.read_text()
    updated = rewrite(original, version, checksums)
    if updated == original:
        print(f"repo-companion is already at {version}; nothing to do.")
        return 0

    FORMULA.write_text(updated)
    print(f"updated Formula/repo-companion.rb to {version}")
    for platform in PLATFORMS:
        print(f"  {platform:<14} {checksums[platform]}")

    if args.pr:
        open_pr(version)
        return 0

    print("\nnext:")
    print("  git diff Formula/repo-companion.rb")
    print("  brew audit --strict --online repocompanion/tap/repo-companion")
    print("  brew style repocompanion/tap/repo-companion")
    print("  brew reinstall repocompanion/tap/repo-companion")
    print("  brew test repo-companion")
    print("  git commit -am 'chore: bump repo-companion to <version>' && git push")
    print("  or rerun with --pr to do the commit, push, and PR")
    return 0


if __name__ == "__main__":
    sys.exit(main())
