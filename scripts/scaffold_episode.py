#!/usr/bin/env python3
"""Find the video template library and scaffold an episode from it."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile


REPOSITORY = "https://github.com/hongye007/kvs-video-template.git"


def main() -> None:
    override = os.environ.get("KVS_VIDEO_TEMPLATE_DIR") or os.environ.get("KVS_GITHUB_VIDEO_TEMPLATE_DIR")
    default_root = Path.home() / "Documents/SourceHub/CommonHub/kvs-video-template"
    root = Path(override).expanduser() if override else default_root

    if not override and not (root.exists() or root.is_symlink()):
        root.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".kvs-template-clone-", dir=root.parent) as temporary:
            checkout = Path(temporary) / root.name
            try:
                subprocess.run(["git", "clone", "--", REPOSITORY, str(checkout)], check=True)
            except (OSError, subprocess.CalledProcessError) as exc:
                raise SystemExit(f"Could not clone {REPOSITORY} to {root}: {exc}") from exc
            try:
                checkout.rename(root)
            except OSError:
                if not root.is_dir():
                    raise

    script = root / "scripts/scaffold_episode.py"
    catalog = root / "catalog.json"
    if not script.is_file() or not catalog.is_file():
        raise SystemExit(f"Template checkout incomplete at {root}. Set KVS_VIDEO_TEMPLATE_DIR to a valid checkout.")

    if sys.argv[1:] == ["--catalog"]:
        print(catalog.read_text(encoding="utf-8"), end="")
        return

    os.execv(sys.executable, [sys.executable, str(script), "--scene", "github-trending-weekly", *sys.argv[1:]])


if __name__ == "__main__":
    main()
