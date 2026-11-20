#!/usr/bin/env python3
# Update media_encoder


from utils_update import (
    add_path_local_bin,
    create_path,
    create_venv,
    install_library,
    link_into_local_bin,
    sync_media_encoder,
)


def install_program() -> None:
    """Install program to ~/.local/bin"""

    # Create path
    create_path()

    # Launch sync
    sync_media_encoder()

    # create link into ~/.local/bin
    link_into_local_bin()

    # Add_path_local_bin
    add_path_local_bin()

    # Create environment
    create_venv()

    # Install  library of requirements.txt
    install_library()


if __name__ == "__main__":
    install_program()
