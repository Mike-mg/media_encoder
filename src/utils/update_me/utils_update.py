#!/usr/bin/env python3
import subprocess
from pathlib import Path


def add_path_local_bin() -> None:
    """Add variable path : [ ~/.local/bin ]"""

    bashrc: Path = Path.home() / ".bashrc"
    path_local_bin = 'export PATH="$HOME/.local/bin:$PATH"\n'

    content_bashrc: str = bashrc.read_text(encoding="utf-8") if bashrc.exists() else ""

    if path_local_bin.strip() not in content_bashrc:
        with bashrc.open("a", encoding="utf-8") as file:
            file.write(path_local_bin)

    subprocess.run(["bash"])


def check_install_library_colorama() -> None:
    """Check if library colorama installed"""

    return_error_module_colorama: subprocess.CompletedProcess[str] = subprocess.run(
        [
            Path.home() / ".local" / "bin" / "media_encoder" / ".venv" / "bin/pip",
            "show",
            "colorama",
        ],
        capture_output=True,
        errors="replace",
        encoding="utf-8",
        check=False,
    )

    if return_error_module_colorama.stderr:
        print("Library Colorama non installé")
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
                "colorama",
            ]
        )
    else:
        print("Library Colorama installé")


def link_into_local_bin(destination: Path) -> None:
    """Check if link media_encoder.py into ~/.local/bin"""

    if not Path(destination / "media_encoder.py").exists():
        subprocess.run(
            [
                "ln",
                "-s",
                f"{destination / 'media_encoder' / 'media_encoder.py'}",
                str(destination),
            ]
        )


def check_venv_created() -> None:
    """Check if environment created"""
    if not (Path.home() / ".local" / "bin" / "media_encoder" / ".venv").exists():
        subprocess.run(
            [
                "python3",
                "-m",
                "venv",
                str(Path.home() / ".local" / "bin" / "media_encoder" / ".venv"),
            ]
        )


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
        ]
    )
