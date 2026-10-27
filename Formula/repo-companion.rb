class RepoCompanion < Formula
  desc "Git-backed documentation and guidance for coding agents"
  homepage "https://repocompanion.com"
  version "0.2.0"
  license "Apache-2.0"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/repocompanion/companion/releases/download/v#{version}/companion_#{version}_darwin_arm64.tar.gz"
      sha256 "d87fd3fc7978109430bacafed1c6ff502cb1016001a380b226f8dc3ec41ba0e3"
    else
      url "https://github.com/repocompanion/companion/releases/download/v#{version}/companion_#{version}_darwin_amd64.tar.gz"
      sha256 "b71feddaf73e9bcc00399d55322e58e6a90288509a336e05e36067131e3d9996"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/repocompanion/companion/releases/download/v#{version}/companion_#{version}_linux_arm64.tar.gz"
      sha256 "8e092c806e0cf4af02499dc6dc3da73c026f8b83848135e2bc6d575a27ac0b8a"
    else
      url "https://github.com/repocompanion/companion/releases/download/v#{version}/companion_#{version}_linux_amd64.tar.gz"
      sha256 "267506e38b174e004bc496c738e19bb786d25a2e7a3d2cddefbd60e68356cdf2"
    end
  end

  def install
    bin.install "companion"
    generate_completions_from_executable(bin/"companion", "completion")
  end

  def caveats
    <<~EOS
      Optional: Universal Ctags adds non-Go symbol indexing.
        brew install universal-ctags

      GitHub PR operations need a token from COMPANION_FORGE_TOKEN,
      forge.token, or `gh auth token`.
    EOS
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/companion version")
  end
end
