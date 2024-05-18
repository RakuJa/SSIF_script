import logging
import sys
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from src.SSIF_script import SSIF_script

BASE_URL: str = "https://github.com/"
BLACKLIST: list[str] = ["Learn how we count contributions"]


def start() -> None:
    while True:
        name = input("Enter account name to search for contributions : ")
        full_url = BASE_URL + name

        page = requests.get(full_url, timeout=60)

        if page.status_code == HTTPStatus.OK:
            # 200 = ok, Profile found
            logging.debug("Profile found, extrapolating content.. \n")
        elif page.status_code == HTTPStatus.NOT_FOUND:
            logging.warning("Profile not found..  \n")

        soup = BeautifulSoup(page.content, "html.parser")
        text = soup.findAll(text=True)
        contribution_list = SSIF_script.parse_txt_lines(text, "contributions")
        for element in contribution_list:
            for blacklist_el in BLACKLIST:
                if blacklist_el in element:
                    # remove string that contains blacklisted substrings
                    contribution_list.remove(element)

        for remaining_element in contribution_list:
            # print the stripped vector one element each
            print(remaining_element)

        user_input = input("Search for another user contributions? Y/N : ")
        if user_input.upper() == "N":
            sys.exit()
