#!/usr/bin/env python3
import subprocess
import venv
from pathlib import Path


def sync_media_encoder(source: Path, destination: Path) -> None:
    """Launch sync"""
    subprocess.run(
        [
            "rsync",
            "-avhP",
            "--info=progress2",
            "--human-readable",
            "--delete",
            "--exclude",
            ".venv",
            "--exclude",
            "__pycache__/",
            "--exclude",
            "*.pyc",
            "--exclude",
            "*.git",
            str(source),
            str(destination),
        ],
        check=True,
    )


def add_path_local_bin() -> None:
    """Add variable path : [ ~/.local/bin ]"""

    bashrc: Path = Path.home() / ".bashrc"
    path_local_bin = 'export PATH="$HOME/.local/bin:$PATH"\n'

    content_bashrc: str = bashrc.read_text(encoding="utf-8") if bashrc.exists() else ""

    if path_local_bin.strip() not in content_bashrc:
        with bashrc.open("a", encoding="utf-8") as file:
            file.write(path_local_bin)


def link_into_local_bin(destination: Path) -> None:
    """Check if link media_encoder.py into ~/.local/bin"""

    target: Path = destination / "media_encoder" / "src" / "media_encoder.py"
    link: Path = destination / "media_encoder.py"
    link.symlink_to(target)


def create_venv(destination: Path) -> None:
    """Create environment"""
    venv.create(destination / "media_encoder" / ".venv", clear=True, with_pip=True)


def install_library() -> None:
    """Install library of requirements.txt"""

    path_me: Path = Path.home() / ".local" / "bin" / "media_encoder"
    python_venv: Path = path_me / ".venv" / "bin" / "python"
    requirements_txt: Path = path_me / "requirements.txt"
    subprocess.run([python_venv, "-m", "pip", "install", "-r", requirements_txt])
