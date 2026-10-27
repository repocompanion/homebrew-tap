# Repo Companion — Homebrew tap

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

The formula is updated by hand after each upstream release, from the release
`checksums.txt`. See the upstream
[release process](https://github.com/repocompanion/companion/blob/main/VERSIONING.md#release-process).

To bump it:

1. Open the release's `checksums.txt` and copy the four archive checksums
   (`darwin_amd64`, `darwin_arm64`, `linux_amd64`, `linux_arm64`).
2. Update the four `url` stanzas and their `sha256` values in
   `Formula/repo-companion.rb`. The version is inferred from the URLs, so there
   is no separate `version` line to change.
3. Check it locally, then commit and push:

   ```bash
   brew audit --strict --online repocompanion/tap/repo-companion
   brew style repocompanion/tap/repo-companion
   brew reinstall repocompanion/tap/repo-companion
   brew test repo-companion
   ```

The formula is distributed under the same Apache-2.0 license as the upstream
project.
