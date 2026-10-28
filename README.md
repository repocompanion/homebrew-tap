# Repo Companion — Homebrew tap

[![CI](https://github.com/repocompanion/homebrew-tap/actions/workflows/ci.yml/badge.svg)](https://github.com/repocompanion/homebrew-tap/actions/workflows/ci.yml)

Homebrew formula for [Repo Companion](https://repocompanion.com), a Git-backed
documentation store and guidance layer for coding agents and their humans.

The formula installs the `companion` CLI (macOS Intel/Apple Silicon and Linux
x86_64/arm64) from the release archives published in
[repocompanion/companion](https://github.com/repocompanion/companion/releases).

## Install

```bash
brew install repocompanion/tap/repo-companion
companion version
```

The formula is named `repo-companion`; the binary it installs is `companion`.

Installing with a fully qualified name trusts only this formula. If you tap the
repository first and install by short name, trust the formula explicitly:

```bash
brew tap repocompanion/tap
brew trust --formula repocompanion/tap/repo-companion
brew install repo-companion
```

## Upgrade and uninstall

```bash
brew upgrade repo-companion
brew uninstall repo-companion
```

## Optional tools

Repo Companion works without either, but these improve the experience:

```bash
brew install universal-ctags   # non-Go symbol indexing
brew install gh                # token source for GitHub PR operations
```

## Maintenance

A new upstream release means one formula bump. The version is inferred from the
four release URLs, so there is no separate `version` line to edit.

```bash
scripts/bump.py v0.3.0        # rewrite the URLs and SHA-256s from checksums.txt
scripts/bump.py v0.3.0 --pr   # the same, then branch, commit, push, and open a PR
```

The script downloads the release's
[`checksums.txt`](https://github.com/repocompanion/companion/releases/latest),
maps each archive to its stanza, and refuses to guess when a platform is
missing. `--checksums path/to/checksums.txt` uses a local file instead of
downloading one.

Check it before pushing (CI runs the same checks on macOS and Linux):

```bash
brew audit --strict --online repocompanion/tap/repo-companion
brew style repocompanion/tap/repo-companion
brew reinstall repocompanion/tap/repo-companion
brew test repo-companion
```

`main` is protected: changes land through a pull request and the
`macos-latest` and `ubuntu-latest` checks must pass. `scripts/bump.py --pr`
does the branch, commit, push, and PR in one step.

CI runs on every pull request and on pushes that touch `Formula/**` or the
workflow. A weekly scheduled run also fails when the tap is behind the latest
GitHub release, which is the "forgot to bump" alarm. `livecheck` reads the
latest release, so prereleases are ignored.
