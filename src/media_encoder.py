#!/home/mike/.local/bin/media_encoder/.venv/bin/python
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
        self.media_error: Path = self.media_encoder / "media_error"

    def check_media(self) -> None:
        """Check all media if ok before encode"""

        print(f"\n{'=' * 100}\n[ 1 | Starting ]  Check medias\n{'=' * 100}\n")

        list_media: list[Path] = create_list_media()

        for index_media, media in enumerate(list_media, start=1):
            log_media_error: Path = self.media_error / f"{media.stem}.log"

            print(
                Fore.LIGHTCYAN_EX,
                f"[ {index_media}/{len(list_media)} ]",
                f" .. {media}",
                Style.RESET_ALL,
                flush=True,
                sep="",
                end="",
            )
            result_command_ffmpeg: subprocess.CompletedProcess[str] = subprocess.run(
                command_ffmpeg_check_media(str(media)),
                capture_output=True,
                errors="replace",
                encoding="utf-8",
                check=False,
            )
            if (
                result_command_ffmpeg.stderr.strip()
                or result_command_ffmpeg.returncode != 0
            ):
                print(Fore.LIGHTYELLOW_EX, " .. [ Media error ]", Style.RESET_ALL)
                log_media_error.write_text(
                    result_command_ffmpeg.stderr, encoding="utf-8"
                )
                media.replace(self.media_error / media.name)
                print(
                    Fore.LIGHTWHITE_EX,
                    ".. Moving to folder media error executed",
                    Style.RESET_ALL,
                )

            else:
                print(Fore.LIGHTGREEN_EX, " .. [ Media OK ]", Style.RESET_ALL, end="")

                if (self.media_encoder / "media_final" / media.name).exists():
                    print(
                        Fore.LIGHTRED_EX,
                        ".. Moving impossible file exists to destination",
                        Style.RESET_ALL,
                    )
                else:
                    media.replace(self.media_encoder / "media_final" / media.name)
                    print(
                        Fore.LIGHTWHITE_EX,
                        ".. Moving to folder media final executed",
                        Style.RESET_ALL,
                    )

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
                "\n[ X ] .. There are not medias into directory to encode.\n",
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
