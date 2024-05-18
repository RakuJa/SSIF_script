import os
import sys
from itertools import chain
from os import listdir
from pathlib import Path

from src import interface

tutorial_name = "SSIF_tutorial.md"


def pdf_to_text(file_path: Path) -> str:
    import io

    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
    from pdfminer.pdfpage import PDFPage

    with file_path.open("rb") as fp:
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the document.

        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            data = retstr.getvalue()

    return data


def parse_pdf(file_path: Path, string_to_search: str) -> list:
    txt_dump = file_path / ".txt"
    with Path(txt_dump).open("a") as f:
        print(pdf_to_text(file_path), file=f)

    occ = parse_txt(txt_dump, string_to_search)
    txt_dump.unlink(missing_ok=True)
    return occ


def parse_txt_lines(lines: list[str], string_to_search: str) -> list[str]:
    return [line for line in lines if line.find(string_to_search) != -1]


def parse_txt(file_path: Path, string_to_search: str) -> list[str]:
    with file_path.open(encoding="utf-8") as f:
        return parse_txt_lines(f.readlines(), string_to_search)


def parse_file(file_path: Path, string_to_search: str) -> list[str]:
    """
    Parses a given file checking for the given string. It will fall back to .txt
    """
    if file_path.suffix.lower() == ".pdf":
        return parse_pdf(file_path, string_to_search)
    return parse_txt(file_path, string_to_search)


def take_all_files(my_path: Path) -> list:
    return [f for f in listdir(my_path) if (my_path / f).is_file()]


def take_file_input() -> list:
    keep_taking_input = True
    file_list = []
    while keep_taking_input:
        file_name = input("Enter file path, Empty line to stop input ")
        if file_name == "ALL":
            file_list = take_all_files(Path.cwd())
        elif file_name == "":
            keep_taking_input = False
        else:
            file_list.append(file_name)
    return list(set(file_list))  # remove duplicates


def print_instructions() -> None:
    text: str = (
        "[1] Tutorial \n" "[2] Continua esecuzione \n" "[7] Credits   [9] Exit \n"
    )
    print(interface.bordered(text))


def require_input() -> str:
    choice = input("Enter Your Choice in the Keyboard [1,2,7,9] : ")
    return choice.upper()


def start() -> None:
    print_instructions()
    keep_asking_input = True
    while keep_asking_input:
        choice = require_input()
        if choice in ("1", "TUTORIAL"):
            interface.print_file(tutorial_name)
        elif choice in ("2", "CONTINUE"):
            keep_asking_input = False
        elif choice in ("7", "CREDITS"):
            print("https://github.com/RakuJa")
        elif choice in ("9", "EXIT"):
            sys.exit()

    options = input("Enter options like this : -v -f or press enter")

    write_to_file = options.find("-f") != -1

    verbose = options.find("-v") != -1

    file_list = take_file_input()
    to_search = input("Enter string to search ")

    print("\n Search started.... \n")
    occurrences_list = []
    for file_name in file_list:
        if verbose:
            print("\n Starting search in " + file_name + "\n")
        tmp = parse_file(file_name, to_search)
        if tmp is not None:
            occurrences_list.append(tmp)
        if verbose:
            print("\n" + file_name + " Searched...." + "\n")
    if verbose:
        print("\n" + "Search over........." + "\n")

    flattened_list = list(chain(*occurrences_list))
    prepare_string = (
        "Found in "
        + str(len(occurrences_list))
        + " files \n"
        + "Found "
        + str(len(flattened_list))
        + " occurrences of the string \n"
        + "Here's the list \n"
    )
    print(prepare_string)
    print(*flattened_list, sep=" \n")

    if write_to_file:
        with Path("results.txt").open("a") as f:
            print(prepare_string, file=f)
            print(*flattened_list, sep=" \n", file=f)

    x = input(" Would you like to restart the script? Y/N")
    if x.upper() == "Y":
        os.startfile(__file__)  # noqa
        sys.exit()
