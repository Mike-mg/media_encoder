#!/usr/bin/env python3
# Update encoder mp4 h265 system

import subprocess
from pathlib import Path

subprocess.run("clear", check=False)


def install_program() -> None:
    """Install program to ~/.local/bin"""
    source: Path = Path.home() / "dev_s" / "python" / "media_encoder"
    destination: Path = Path.home() / ".local" / "bin"
    bashrc: Path = Path.home() / ".bashrc"

    if not destination.exists():
        destination.mkdir(parents=True, exist_ok=True)
        destination.chmod(0o755)

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
            str(source),
            str(destination),
        ]
    )

    if not Path(destination / "media_encoder.py").exists():
        subprocess.run(
            [
                "ln",
                "-s",
                f"{destination / 'media_encoder' / 'media_encoder.py'}",
                str(destination),
            ]
        )

    if not (Path.home() / ".local" / "bin" / "media_encoder" / ".venv").exists():
        subprocess.run(
            [
                "python3",
                "-m",
                "venv",
                str(Path.home() / ".local" / "bin" / "media_encoder" / ".venv"),
            ]
        )

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
        print("colorama non installé")
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

    path_local_bin = 'export PATH="$HOME/.local/bin:$PATH"\n'

    content_bashrc: str = bashrc.read_text(encoding="utf-8") if bashrc.exists() else ""

    if path_local_bin.strip() not in content_bashrc:
        with bashrc.open("a", encoding="utf-8") as file:
            file.write(path_local_bin)

    subprocess.run(["bash"])


if __name__ == "__main__":
    install_program()
