from pathlib import Path
from typing import List

from PyPDF2 import PdfFileMerger
from pathvalidate import validate_filepath, ValidationError
import os


def take_file_input() -> set:
    keep_taking_input = True
    file_list: set = set()
    while keep_taking_input:
        file_path = input(
            "Enter file path, Empty line to stop input, '.' for all pdfs in current dir "
        )
        if not file_path:
            keep_taking_input = False
        else:
            if validate_file_path(file_path):
                if Path(file_path).is_file():
                    file_list.add(file_path)
                elif Path(file_path).is_dir():
                    file_list.update(take_all_files_in_given_path(file_path))

    return file_list


def take_all_files_in_given_path(
    dir_path: str = "", filter_for_extension: str = "pdf"
) -> set:
    return {
        os.path.join(dir_path, file)
        for file in os.listdir(dir_path)
        if file.endswith(filter_for_extension)
    }


def validate_file_path(file_path: str) -> bool:
    """
    Checks for file path formal validity and then existence
    """
    try:
        validate_filepath(file_path, platform="auto")
        if not Path(file_path).exists():
            raise ValidationError(f"The given file does not exist: {file_path}")
        return True
    except ValidationError as e:
        print(f"\nEncountered an error while parsing the given path: {e}")
        return False


def take_output_file_name() -> str:
    keep_taking_input = True
    while keep_taking_input:
        file_name = input("Enter output file path, Empty line for default name ")
        if not file_name:
            return "result.pdf"
        else:
            try:
                validate_filepath(file_name, platform="auto")
                return file_name if file_name.endswith(".pdf") else file_name + ".pdf"
            except ValidationError as e:
                print(f"\nEncountered an error while parsing the given path: {e}")


def order_files(file_list: iter) -> List:
    print("The current print order is as follows: ")
    i = 0
    ordered_list: List = list(file_list)
    ordered_list.sort()
    for file in ordered_list:
        print(f"[{i}]: {file}")
        i += 1
    result = input(
        "If you wish to change the order enter the list"
        " of number separated by ',' ex: 1,2,3,4 otherwise"
        " if the order is okay enter empty line \n"
    )

    number_list = result.split(",")
    if not number_list:
        return ordered_list
    try:
        return [ordered_list[int(number)] for number in number_list]
    except ValueError as e:
        print(e)
        return ordered_list


def start():
    file_list = order_files(take_file_input())

    merger = PdfFileMerger()
    for pdf in file_list:
        merger.append(pdf)
    merger.write(take_output_file_name())
    merger.close()
