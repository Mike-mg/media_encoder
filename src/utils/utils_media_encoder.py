# functions utils for media_encoder.py


import subprocess
import sys
from pathlib import Path

from colorama import Fore, Style


def clear_screen() -> None:
    """Clear screen before start."""
    subprocess.run(["clear"], check=False)


def command_ffmpeg_check_media(media: str) -> list[str]:
    """Command ffmpeg to execute check media"""
    return [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-err_detect",
        "explode",
        "-nostdin",
        "-i",
        media,
        "-map",
        "0:v",
        "-map",
        "0:a",
        "-f",
        "null",
        "-",
    ]


def command_ffmpeg_encode_media(media: str, destination: str) -> list[str]:
    return [
        "ffmpeg",
        "-nostdin",
        "-fflags",
        "+genpts",
        "-i",
        str(media),
        "-map",
        "0:v:0",
        "-c:v",
        "libx265",
        "-crf",
        "21",
        "-preset",
        "slow",
        "-pix_fmt",
        "yuv420p",
        "-tag:v",
        "hvc1",
        "-map",
        "0:a:0",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-ac",
        "2",
        "-af",
        "aresample=async=1:first_pts=0",
        "-map_chapters",
        "-1",
        "-y",
        str(destination),
    ]


def create_all_paths() -> None:
    """Create all dirs."""

    media_encoder: Path = Path.home() / "media_encoder"
    media_encoder.mkdir(parents=True, exist_ok=True)
    media_encoder.chmod(0o755)

    list_works_path: tuple[str, ...] = (
        "media_final",
        "media_error",
        "media_pending",
    )

    for work_path in list_works_path:
        (media_encoder / work_path).mkdir(exist_ok=True)
        (media_encoder / work_path).chmod(0o755)

    thematics: tuple[str, ...] = (
        "animes",
        "dc_comics",
        "films",
        "marvel",
        "saga",
        "series",
    )

    media_final: Path = media_encoder / "media_final"

    for thematic in thematics:
        (media_final / thematic).mkdir(exist_ok=True)
        (media_final / thematic).chmod(0o755)


def create_list_media() -> list[Path]:
    """Create list medias"""

    list_media: list[Path] = []
    path_media: Path = Path.home() / "media_encoder"

    if not any(
        media
        for media in path_media.glob("*.mkv", case_sensitive=False)
        if media.is_file()
    ):
        print(
            Fore.LIGHTYELLOW_EX,
            "[ X ] .. There are not medias into directory to check.\n",
            Style.RESET_ALL,
            sep="",
        )

    else:
        all_files_media: list[Path] = [
            media
            for media in path_media.glob("*.mkv", case_sensitive=False)
            if media.is_file()
        ]
        for media in all_files_media:
            media_lower: Path = media.with_name(media.name.lower())
            if media != media_lower and not media_lower.exists():
                media: Path = media.rename(media_lower)
            list_media.append(media)

    return sorted(list_media)


def menu_media_encoder(error_message_menu: str = "") -> int | None:
    """Menu app"""

    list_menu: list[str] = [
        "Check medias",
        "Encode medias",
        "Check and encode medias",
        "Exit program",
    ]
    banner = "*** Menu Media Encoder ***"
    print(f"\n{'=' * len(banner)}\n{banner}\n{'=' * len(banner)}")
    print(f"{Fore.LIGHTRED_EX}{error_message_menu}{Style.RESET_ALL}")
    for index, option_menu in enumerate(list_menu):
        print(f"[ {index + 1} ] {option_menu}")

    try:
        choice: int = int(input("\nEnter choice (1, 2, 3 or 4) > "))
        if choice not in range(1, 5):
            raise ValueError

        return choice

    except ValueError:
        clear_screen()
        return menu_media_encoder("\n[ Error ] Enter a number 1, 2, 3, 4\n")

    except KeyboardInterrupt:
        print(
            Fore.LIGHTRED_EX,
            "\n\n.. Program interrupt by user\n".upper(),
            Style.RESET_ALL,
        )
        sys.exit(1)
