#!/home/mike/.local/bin/media_encoder/.venv/bin/python3
# verif all video and encode
import subprocess
import sys
from pathlib import Path

from colorama import Fore, Style


class MediaEncoder:
    """Check all media in folder before encoding."""

    def __init__(self) -> None:
        self.dir_media: Path = Path.home() / "media_encoder"
        self.dir_media_error: Path = self.dir_media / "media_error"
        self.dir_media_final: Path = self.dir_media / "media_final"
        self.list_media: list[Path] = []
        self.list_works_path: tuple[str, ...] = (
            "media_final",
            "media_error",
            "media_pending",
        )
        self.thematics: tuple[str, ...] = (
            "animes",
            "dc_comics",
            "films",
            "marvel",
            "saga",
            "series",
        )
        self.message_error: str = ""

    def clear_screen(self) -> None:
        """Clear screen before start."""
        subprocess.run(["clear"], check=False)

    def create_all_paths(self) -> None:
        """Create all dirs."""
        self.dir_media.mkdir(parents=True, exist_ok=True)
        self.dir_media.chmod(0o755)

        for work_path in self.list_works_path:
            (self.dir_media / work_path).mkdir(exist_ok=True)
            (self.dir_media / work_path).chmod(0o755)

        for thematic in self.thematics:
            (self.dir_media_final / thematic).mkdir(exist_ok=True)
            (self.dir_media_final / thematic).chmod(0o755)

    def create_list_media(self) -> None:
        """Create list medias"""
        self.list_media.clear()

        if not any(
            media
            for media in self.dir_media.glob("*.mkv", case_sensitive=False)
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
                for media in self.dir_media.glob("*.mkv", case_sensitive=False)
                if media.is_file()
            ]
            for media in all_files_media:
                media_lower: Path = media.with_name(media.name.lower())
                if media != media_lower and not media_lower.exists():
                    media: Path = media.rename(media_lower)
                self.list_media.append(media)
            self.list_media.sort()

    def command_ffmpeg_ckeck_media(self, media: str) -> list[str]:
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

    def command_ffmpeg_encode_media(self, media: str, destination: str) -> list[str]:
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

    def check_media(self) -> None:
        """Check all media if ok before encode"""

        self.message_error = ""

        print(f"\n{'=' * 100}\n[ 1 | Starting ]  Check medias\n{'=' * 100}\n")
        self.create_list_media()

        for index_media, media in enumerate(self.list_media):
            log_media_error: Path = self.dir_media_error / f"{media.stem}.log"

            print(
                Fore.LIGHTCYAN_EX,
                f"[ {index_media + 1}/{len(self.list_media)} ]",
                f" .. {media}",
                Style.RESET_ALL,
                flush=True,
                sep="",
                end="",
            )
            result_command_ffmpeg: subprocess.CompletedProcess[str] = subprocess.run(
                self.command_ffmpeg_ckeck_media(str(media)),
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
                media.replace(self.dir_media_error / media.name)
                print(
                    Fore.LIGHTWHITE_EX,
                    ".. Moving to folder media error executed",
                    Style.RESET_ALL,
                )

            else:
                print(Fore.LIGHTGREEN_EX, " .. [ Media OK ]", Style.RESET_ALL, end="")

                if (self.dir_media_final / media.name).exists():
                    print(
                        Fore.LIGHTRED_EX,
                        ".. Moving impossible file exists to destination",
                        Style.RESET_ALL,
                    )
                else:
                    media.replace(self.dir_media_final / media.name)
                    print(
                        Fore.LIGHTWHITE_EX,
                        ".. Moving to folder media final executed",
                        Style.RESET_ALL,
                    )

    def encode_media(self) -> None:
        """Start encode all medias"""

        self.message_error = ""

        print(f"\n{'=' * 100}\n[ 2 | Starting ] Encode medias\n{'=' * 100}")

        if not any(
            media for media in self.dir_media_final.glob("*.mkv") if media.is_file()
        ):
            print(
                Fore.LIGHTYELLOW_EX,
                "\n[ X ] .. There are not medias into directory to encode.\n",
                Style.RESET_ALL,
                sep="",
            )
            return

        else:
            list_medias_mkv: list[Path] = list(self.dir_media_final.glob("*.mkv"))
            list_medias_mkv = sorted(list_medias_mkv)

            for index_media, media in enumerate(list_medias_mkv):
                destination: Path = media.with_name(f"{media.stem}_h265.mp4")

                print(
                    Fore.LIGHTCYAN_EX,
                    f"\n[ {index_media + 1}/{len(list_medias_mkv)} ]",
                    f".. {media}",
                    f"\n{'-' * 100}",
                    Style.RESET_ALL,
                )

                if destination.exists():
                    print(
                        Fore.LIGHTYELLOW_EX,
                        f"[x] Media already encoded  : {destination}\n",
                        Style.RESET_ALL,
                        sep="",
                    )
                    continue

                subprocess.run(
                    self.command_ffmpeg_encode_media(str(media), str(destination)),
                    check=False,
                )

    def menu_media_encoder(self) -> int | None:
        """Menu app"""

        list_menu: list[str] = [
            "Check medias",
            "Encode medias",
            "Check and encode medias",
            "Exit program",
        ]
        banner = "*** Menu Media Encoder ***"
        print(f"\n{'=' * len(banner)}\n{banner}\n{'=' * len(banner)}")
        print(f"{Fore.LIGHTRED_EX}{self.message_error}{Style.RESET_ALL}")
        for index, option_menu in enumerate(list_menu):
            print(f"[ {index + 1} ] {option_menu}")

        try:
            choice: int = int(input("\nEnter choice (1, 2, 3 or 4) > "))
            if choice not in range(1, 5):
                raise ValueError

            return choice

        except ValueError:
            self.clear_screen()
            self.message_error = "\n[ Error ] Enter a number 1, 2, 3, 4\n"

        except KeyboardInterrupt:
            print(
                Fore.LIGHTRED_EX,
                "\n\n.. Program interrupt by user\n".upper(),
                Style.RESET_ALL,
            )
            sys.exit(1)

    def start_media_encoder(self) -> None:
        """Starting class workflow"""
        self.clear_screen()
        self.create_all_paths()

        while True:
            match self.menu_media_encoder():
                case 1:
                    self.clear_screen()
                    self.check_media()
                case 2:
                    self.clear_screen()
                    self.encode_media()
                case 3:
                    self.clear_screen()
                    self.check_media()
                    self.encode_media()
                case 4:
                    break


if __name__ == "__main__":
    media_encoder = MediaEncoder()
    media_encoder.start_media_encoder()
