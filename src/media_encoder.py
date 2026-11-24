#!/usr/bin/env -S ${HOME}/.local/bin/media_encoder/.venv/bin/python
# verif all video and encode
import subprocess
from pathlib import Path

from colorama import Fore, Style

from utils.utils_media_encoder import (
    clear_screen,
    command_ffmpeg_check_media,
    command_ffmpeg_encode_media,
    create_all_paths,
    create_list_media,
    menu_media_encoder,
)


class MediaEncoder:
    """Check all media in folder before encoding."""

    def __init__(self) -> None:
        self.media_encoder: Path = Path.home() / "media_encoder"
        self.media_final: Path = self.media_encoder / "media_final"
        self.media_error: Path = self.media_encoder / "media_error"

    def check_media(self) -> None:
        """Check all media if ok before encode"""

        list_media: list[Path] = create_list_media()
        color_red: str = f"{Fore.LIGHTRED_EX}"
        color_green: str = f"{Fore.LIGHTGREEN_EX}"
        color_white: str = f"{Fore.LIGHTWHITE_EX}"
        color_cyan: str = f"{Fore.LIGHTCYAN_EX}"
        color_yellow: str = f"{Fore.LIGHTYELLOW_EX}"
        reset_color: str = f"{Style.RESET_ALL}"

        print(f"\n{'=' * 100}\n[ 1 | Starting ] Check medias\n{'=' * 100}\n")

        if not list_media:
            print(
                color_yellow,
                "[ X ] .. Not medias into directory to check.\n",
                reset_color,
            )

        for index, media in enumerate(list_media, start=1):
            log_media_error: Path = self.media_error / f"{media.stem}.log"

            print(f"{color_cyan}[ {index}/{len(list_media)} ] .. {media}{reset_color}")

            with log_media_error.open("w") as log_file:
                check_media_command: subprocess.CompletedProcess[str] = subprocess.run(
                    command_ffmpeg_check_media(str(media)),
                    text=True,
                    stderr=log_file,
                )

            if (
                log_media_error.stat().st_size != 0
                or check_media_command.returncode != 0
            ):
                print(color_red, " .. [ Media in Error ]", reset_color)
                media.replace(self.media_error / media.name)
                print(color_red, " .. Moving to folder media_error\n", reset_color)

            else:
                print(color_green, " .. [ Media valided ]", reset_color)
                media.replace(self.media_encoder / "media_final" / media.name)
                print(color_white, " .. Moving to folder media_final\n", reset_color)
                log_media_error.unlink()

    def encode_media(self) -> None:
        """Start encode all medias"""

        print(f"\n{'=' * 100}\n[ 2 | Starting ] Encode medias\n{'=' * 100}\n")

        list_medias_mkv: list[Path] = sorted(
            media
            for media in (self.media_encoder / "media_final").glob("*.mkv")
            if media.is_file()
        )

        if not list_medias_mkv:
            print(
                Fore.LIGHTYELLOW_EX,
                "[ X ] .. There are not medias into directory to encode.\n",
                Style.RESET_ALL,
            )

        for index_media, media in enumerate(list_medias_mkv, start=1):
            destination: Path = media.with_name(f"{media.stem}_h265.mp4")

            if destination.exists():
                print(
                    Fore.LIGHTYELLOW_EX,
                    f"[x] Media already encoded  : {destination}",
                    Style.RESET_ALL,
                    sep="",
                )
                continue

            print(
                Fore.LIGHTCYAN_EX,
                f"\n[ {index_media}/{len(list_medias_mkv)} ]",
                f".. {media}",
                f"\n{'-' * 100}",
                Style.RESET_ALL,
                sep="",
            )

            subprocess.run(
                command_ffmpeg_encode_media(str(media), str(destination)),
                check=False,
            )

    def start_media_encoder(self) -> None:
        """Starting class workflow"""

        # Clean screen
        clear_screen()

        # Create all path to works
        create_all_paths()

        while True:
            match menu_media_encoder():
                case 1:
                    clear_screen()
                    self.check_media()
                case 2:
                    clear_screen()
                    self.encode_media()
                case 3:
                    clear_screen()
                    self.check_media()
                    self.encode_media()
                case 4:
                    break


if __name__ == "__main__":
    media_encoder = MediaEncoder()
    media_encoder.start_media_encoder()
