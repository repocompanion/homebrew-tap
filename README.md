# Repo Companion — Homebrew tap

Homebrew formula for [Repo Companion](https://repocompanion.com), a Git-backed
documentation store and guidance layer for coding agents and their humans.

The formula installs the `companion` CLI (macOS Intel/Apple Silicon and Linux
x86_64/arm64) from the signed-off release archives published in
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

The formula is updated by hand after each upstream release, from the release
`checksums.txt`. See the upstream
[release process](https://github.com/repocompanion/companion/blob/main/VERSIONING.md#release-process).

The formula is distributed under the same Apache-2.0 license as the upstream
project.
