#!/usr/bin/env python3
# Update encoder mp4 h265 system

from pathlib import Path

from .utils_update import (
    add_path_local_bin,
    check_install_library_colorama,
    check_venv_created,
    link_into_local_bin,
    sync_media_encoder,
)


def install_program() -> None:
    """Install program to ~/.local/bin"""

    source: Path = Path.home() / "dev_s" / "python" / "media_encoder"
    destination: Path = Path.home() / ".local" / "bin"

    if not destination.exists():
        destination.mkdir(parents=True, exist_ok=True)
        destination.chmod(0o755)

    # Launch sync
    sync_media_encoder(source, destination)

    # Link into ~/.local/bin
    link_into_local_bin(destination)

    # add_path_local_bin
    add_path_local_bin()

    # Check if environment created
    check_venv_created()

    # check_install_library_colorama
    check_install_library_colorama()


if __name__ == "__main__":
    install_program()
