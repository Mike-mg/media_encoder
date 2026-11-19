#!/usr/bin/env python3
import subprocess
from pathlib import Path


def sync_media_encoder(source: Path, destination: Path) -> None:
    """Launch sync"""
    subprocess.run(
        [
            "rsync",
            "-avhP",
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

    if not Path(destination / "media_encoder.py").exists():
        subprocess.run(
            [
                "ln",
                "-sf",
                f"{destination / 'media_encoder' / 'src' / 'media_encoder.py'}",
                str(destination),
            ],
            check=True,
        )


def create_venv() -> None:
    """Create environment"""
    subprocess.run(
        [
            "python3",
            "-m",
            "venv",
            "--clear",
            str(Path.home() / ".local" / "bin" / "media_encoder" / ".venv"),
        ],
        check=True,
    )


def install_library() -> None:
    """Install library of requirements.txt"""

    subprocess.run(
        [
            str(
                Path.home()
                / ".local"
                / "bin"
                / "media_encoder"
                / ".venv"
                / "bin"
                / "pip"
            ),
            "install",
            "-r",
            Path(Path.home() / ".local" / "bin" / "media_encoder" / "requirements.txt"),
        ],
        check=True,
    )
