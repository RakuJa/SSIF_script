import sys
from pathlib import Path

import interface
import markdown
from bs4 import BeautifulSoup
from file_merger import file_merger
from SSIF_script import SSIF_script
from web_scraper import github_contribution_counter as github_contrib_counter

from src.web_scraper import amazon_product_search, check_site_differences


def get_readme_full_path() -> Path:
    """
    Method used to get the readme full path, if the path will ever change
    modify this method or just don't call the readme reader function
    """
    return Path().resolve().parent / "README.md"


def print_readme() -> None:
    html: str = ""
    with get_readme_full_path().open() as readme_file:
        html = markdown.markdown(readme_file.read())
    parsed_html = BeautifulSoup(html, features="html.parser").findAll(string=True)
    print("\n")
    for line in parsed_html:
        if line and line != "\n":
            print(line)


def print_instructions() -> None:
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


def require_input() -> str:
    return input("Enter Your Choice in the Keyboard [1,2,3,5,6,7,8,9] : ").upper()


if __name__ == "__main__":

    print_instructions()

    while True:
        choice = require_input()
        if choice in ("1", "READ"):
            print_readme()
        elif choice in ("2", "MERGER"):
            file_merger.start()
        elif choice in ("3", "SSIF", "SEARCH"):
            SSIF_script.start()
        elif choice in ("4", "CONTRIBUTION", "GITHUB"):
            github_contrib_counter.start()
        elif choice in ("5", "AMAZON"):
            amazon_product_search.start()
        elif choice == "6":
            check_site_differences.start()
        elif choice in ("7", "CREDITS"):
            print("https://github.com/RakuJa")
        elif choice in ("8", "INSTRUCTIONS"):
            print_instructions()
        elif choice in ("9", "EXIT"):
            sys.exit()
