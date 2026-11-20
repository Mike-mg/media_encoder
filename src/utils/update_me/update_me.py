#!/usr/bin/env python3
# Update media_encoder

from pathlib import Path

from utils_update import (
    add_path_local_bin,
    create_venv,
    install_library,
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

    # create link into ~/.local/bin
    link_into_local_bin(destination)

    # Add_path_local_bin
    add_path_local_bin()

    # Create environment
    create_venv(destination)

    # Install  library of requirements.txt
    install_library()


if __name__ == "__main__":
    install_program()
