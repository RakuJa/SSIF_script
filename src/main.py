import os
import sys
import interface
import markdown

from file_merger import file_merger
from SSIF_script import SSIF_script
from src.web_scraper import amazon_product_search, check_site_differences
from web_scraper import github_contribution_counter as github_contrib_counter

from bs4 import BeautifulSoup
from pathlib import Path


def get_readme_full_path() -> str:
    """
    Method used to get the readme full path, if the path will ever change
    modify this method or just don't call the readme reader function
    """
    return os.path.join(Path().resolve().parent, "README.md")


def print_readme():
    html: str = ""
    with open(get_readme_full_path()) as readme_file:
        html = markdown.markdown(readme_file.read())
    parsed_html = BeautifulSoup(html, features="html.parser").findAll(text=True)
    print("\n")
    for line in parsed_html:
        if line and line != "\n":
            print(line)


def print_instructions():
    text = (
        "[1] Read Me \n"
        + "[2] File merger \n"
        + "[3] Search string in file \n"
        + "[4] Github contribution counter \n"
        + "[5] Amazon product finder \n"
        + "[6] Site differences \n"
        + "[7] Credits"
        + "[8] Instructions  "
        + "[9] Exit \n "
    )
    print(interface.bordered(text))


def require_input():
    return input("Enter Your Choice in the Keyboard [1,2,3,5,6,7,8,9] : ").upper()


if __name__ == "__main__":

    current_path = os.getcwd()

    file_merger_path = os.path.join("file_merger", "file_merger.py")
    file_merger_path = os.path.join(current_path, file_merger_path)

    ssif_path = os.path.join("SSIF_script", "SSIF_script.py")
    ssif_path = os.path.join(current_path, ssif_path)
    print_instructions()

    while True:
        choice = require_input()
        if choice == "1" or choice == "READ":
            print_readme()
        elif choice == "2" or choice == "MERGER":
            file_merger.start()
        elif choice == "3" or choice == "SSIF" or choice == "SEARCH":
            SSIF_script.start()
        elif choice == "4" or choice == "CONTRIBUTION" or choice == "GITHUB":
            github_contrib_counter.start()
        elif choice == "5" or choice == "AMAZON":
            amazon_product_search.start()
        elif choice == "6":
            check_site_differences.start()
        elif choice == "7" or choice == "CREDITS":
            print("https://github.com/RakuJa")
        elif choice == "8" or choice == "INSTRUCTIONS":
            print_instructions()
        elif choice == "9" or choice == "EXIT":
            sys.exit()
