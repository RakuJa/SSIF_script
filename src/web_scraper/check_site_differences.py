import logging
import sys
import time
from http import HTTPStatus
from pathlib import Path

import requests
from bs4 import BeautifulSoup

FOLDER: str = "data"
BASE_URL: str = "https://www.math.unipd.it/"
REMOTE_FILE_PATH: Path = Path(FOLDER) / "temp.ignore"
BLACKLIST_PATH_CHAR: list[str] = [
    "*",
    ".",
    "/",
    "'",
    "[",
    "]",
    ":",
    ";",
    "|",
    ",",
    "<",
    ">",
]
WHITELISTED_CHAR: str = "_"

logger = logging.getLogger(__name__)


def start() -> None:
    minutes_to_wait = 0
    site = input("Input full url: ")

    if site is None or site == "":
        site = BASE_URL
    local_file_name = site

    # Remove every char that might not work in certain os (coff coff windows)
    for forbidden_char in BLACKLIST_PATH_CHAR:
        local_file_name = local_file_name.replace(forbidden_char, WHITELISTED_CHAR)

    # Add file extension
    local_file_name = local_file_name + ".ignore"

    # Create valid path to folder
    local_file_path: Path = Path(FOLDER) / local_file_name
    try:
        default_folder_setup(local_file_path)
    except (OSError, NotADirectoryError) as e:
        print(e)
    keep_searching = input(
        "Do you want to keep searching for differences every n minutes? Y/N :",
    )
    if keep_searching.upper() == "Y":
        minutes_to_wait = int(
            input("Enter a number for the minutes to wait for update: "),
        )

    while True:
        # Be sure that data folder is setup
        try:
            default_folder_setup(local_file_path)
        except (OSError, NotADirectoryError) as e:
            print(e)
            input("Exception encountered... press Enter to retry to execution")
            continue
        # End of data folder checks and/or creation

        page = requests.get(site, timeout=60)

        print(page.status_code)
        if page.status_code == HTTPStatus.OK:
            # 200 = ok, Profile found
            print("Site found, extrapolating content.. \n")
        if page.status_code == HTTPStatus.NOT_FOUND:
            print("Site not found..  \n")

        soup = BeautifulSoup(page.content, "html.parser")

        remote_site: str = str(soup)
        with REMOTE_FILE_PATH.open("w") as f:
            f.write(remote_site)

        if local_file_path.stat().st_size == 0:
            with local_file_path.open("w") as f:
                f.write(remote_site)

        diff: str = check_file_diff(local_file_path, REMOTE_FILE_PATH)
        if diff == "":
            print("The site is the same as ever.. \n")
        else:
            print("The site updated! Here's the list of differences: \n")
            print(diff)
            user_input = input("Update local site version? Y/N : ")
            if user_input.upper() == "Y":
                with local_file_path.open("w") as f:
                    f.write(remote_site)

        if minutes_to_wait != 0:
            seconds = minutes_to_wait * 60
            print(f"Waiting {minutes_to_wait} minutes before next iteration")
            time.sleep(seconds)
        else:
            user_input = input("Search again? Y/N : ")
            if user_input.upper() == "N":
                sys.exit()


def check_file_diff(first_file: Path, second_file: Path) -> str:
    with first_file.open() as file1, second_file.open() as file2:
        diff = set(file1).symmetric_difference(file2)
        diff.discard("\n")
    return ", ".join(diff)


def default_folder_setup(local_file_path: Path) -> None:
    folder_path = Path(FOLDER)

    if folder_path.is_file():
        try:
            folder_path.unlink()
        except OSError:
            error: str = (
                "Default data path already exists as a file and"
                " we encountered errors while deleting it, delete it!"
            )
            logger.warning(error)
            raise NotADirectoryError(error) from None
    if not folder_path.exists():
        try:
            folder_path.mkdir()
        except OSError:
            error: str = "Creation of default data directory has failed"
            logger.warning(error)
            raise OSError(error) from None
    # If path is a directory we delete it
    if local_file_path.exists() and not local_file_path.is_file():
        local_file_path.rmdir()
    if not local_file_path.exists():
        with local_file_path.open("w") as f:
            f.close()
