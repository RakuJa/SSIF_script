import sys

import requests
from bs4 import BeautifulSoup

from src.SSIF_script import SSIF_script

BASE_URL = 'https://github.com/'
BLACKLIST = ["Learn how we count contributions"]


def start():
    while True:
        name = input("Enter account name to search for contributions : ")
        full_url = BASE_URL + name

        page = requests.get(full_url)

        print(page.status_code)
        if page.status_code == 200:
            # 200 = ok, Profile found
            print("Profile found, extrapolating content.. \n")
        if page.status_code == 404:
            print("Profile not found..  \n")

        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.findAll(text=True)
        contribution_list = SSIF_script.parse_txt_data(text, "contributions")
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
