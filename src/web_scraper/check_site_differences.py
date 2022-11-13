import os
import sys
import time

import requests
from bs4 import BeautifulSoup

FOLDER = "data"
BASE_URL = "https://www.math.unipd.it/"
REMOTE_FILE_PATH = os.path.join(FOLDER, "temp.ignore")
BLACKLIST_PATH_CHAR = ["*", ".", "/", "'", "[", "]", ":", ";", "|", ",", "<", ">"]
WHITELISTED_CHAR = "_"


def start():
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
    local_file_path = os.path.join(FOLDER, local_file_name)
    try:
        default_folder_setup(local_file_path)
    except (OSError, NotADirectoryError) as e:
        print(e)
    keep_searching = input(
        "Do you want to keep searching for differences every n minutes? Y/N :"
    )
    if keep_searching.upper() == "Y":
        minutes_to_wait = int(
            input("Enter a number for the minutes to wait for update: ")
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

        page = requests.get(site)

        print(page.status_code)
        if page.status_code == 200:
            # 200 = ok, Profile found
            print("Site found, extrapolating content.. \n")
        if page.status_code == 404:
            print("Site not found..  \n")

        soup = BeautifulSoup(page.content, "html.parser")

        remote_site: str = str(soup)
        with open(REMOTE_FILE_PATH, "w") as f:
            f.write(remote_site)

        if os.stat(local_file_path).st_size == 0:
            with open(local_file_path, "w") as f:
                f.write(remote_site)

        diff: str = check_file_diff(local_file_path, REMOTE_FILE_PATH)
        if diff == "":
            print("The site is the same as ever.. \n")
        else:
            print("The site updated! Here's the list of differences: \n")
            print(diff)
            user_input = input("Update local site version? Y/N : ")
            if user_input.upper() == "Y":
                with open(local_file_path, "w") as f:
                    f.write(remote_site)

        if minutes_to_wait != 0:
            seconds = minutes_to_wait * 60
            print("Waiting %s minutes before next iteration" % seconds)
            time.sleep(seconds)
        else:
            user_input = input("Search again? Y/N : ")
            if user_input.upper() == "N":
                sys.exit()


def check_file_diff(first_file: str, second_file: str) -> str:
    with open(first_file, "r") as file1:
        with open(second_file, "r") as file2:
            diff = set(file1).symmetric_difference(file2)

    diff.discard("\n")
    diff = ", ".join(diff)
    return diff


def default_folder_setup(local_file_path: str) -> None:
    if os.path.isfile(FOLDER):
        try:
            os.remove(FOLDER)
        except OSError:
            print("Could not delete data file")
            raise NotADirectoryError(
                "Default data path already exists as a file and"
                " we encountered errors while deleting it, delete it!"
            )
    if not os.path.exists(FOLDER):
        try:
            os.mkdir(FOLDER)
        except OSError:
            print("Creation of the directory has failed")
            raise OSError("Creation of default data directory has failed")
    # If path is a directory i delete it
    if os.path.exists(local_file_path) and not os.path.isfile(local_file_path):
        os.rmdir(local_file_path)
    if not os.path.exists(local_file_path):
        with open(local_file_path, "w") as f:
            f.close()
