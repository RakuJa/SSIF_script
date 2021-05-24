import os
import sys

import requests
from bs4 import BeautifulSoup

FOLDER = "data"
# BASE_URL = 'https://www.math.unipd.it/~rcardin/sweb/2021/'
BASE_URL = 'https://www.math.unipd.it/'
REMOTE_FILE_PATH = os.path.join(FOLDER, "temp.ignore")


def start():
    site = input("Input full url: ")

    if site is None or site == "":
        site = BASE_URL

    local_file_name = site.replace("/", "|")
    local_file_name = local_file_name + ".ignore"
    local_file_path = os.path.join(FOLDER, local_file_name)

    ask_update_or_create_local_file(local_file_path)

    while True:

        page = requests.get(site)

        print(page.status_code)
        if page.status_code == 200:
            # 200 = ok, Profile found
            print("Site found, extrapolating content.. \n")
        if page.status_code == 404:
            print("Site not found..  \n")

        soup = BeautifulSoup(page.content, 'html.parser')

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

        user_input = input("Search again? Y/N : ")
        if user_input.upper() == "N":
            sys.exit()


def ask_update_or_create_local_file(local_file_path: str) -> None:
    if os.path.exists(local_file_path) and os.path.isfile(local_file_path):
        if os.stat(local_file_path).st_size != 0:
            need_update_local = input("Update site local version? Y/N : ")
            if need_update_local.upper() == "Y":
                with open(local_file_path, "w") as f:
                    f.close()
    else:
        with open(local_file_path, "w") as f:
            f.close()


def check_file_diff(first_file: str, second_file: str) -> str:
    with open(first_file, 'r') as file1:
        with open(second_file, 'r') as file2:
            diff = set(file1).symmetric_difference(file2)

    diff.discard('\n')
    diff = ", ".join(diff)
    return diff
