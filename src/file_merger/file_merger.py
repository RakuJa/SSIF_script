import logging
import os
from pathlib import Path

from pathvalidate import ValidationError, validate_filepath
from PyPDF2 import PdfFileMerger

logger = logging.getLogger(__name__)


def take_file_input() -> set:
    keep_taking_input = True
    file_list: set = set()
    while keep_taking_input:
        file_raw_path = input(
            "Enter file path."
            " Empty line to stop input, '.' for all pdfs in current dir ",
        )
        if not file_raw_path:
            keep_taking_input = False
        elif validate_file_path(file_raw_path):
            file_path: Path = Path(file_raw_path)
            if file_path.is_file():
                file_list.add(str(file_path))
            elif file_path.is_dir():
                file_list.update(take_all_files_in_given_path(file_path))

    return file_list


def take_all_files_in_given_path(
    dir_path: Path,
    filter_for_extension: str = "pdf",
) -> set:
    return {
        str(dir_path / file)
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
            error: str = f"Error while parsing the given path: {file_path}"
            logger.warning(error)
            return False
    except ValidationError:
        return False
    else:
        return True


def take_output_file_name() -> str:
    keep_taking_input = True
    while keep_taking_input:
        file_name = input("Enter output file path, Empty line for default name ")
        if file_name:
            try:
                validate_filepath(file_name, platform="auto")
                return file_name if file_name.endswith(".pdf") else file_name + ".pdf"
            except ValidationError as e:
                error: str = f"\nEncountered an error while parsing the given path: {e}"
                logger.warning(error)
    return "result.pdf"


def order_files(file_list: iter) -> list:
    print("The current print order is as follows: ")
    i = 0
    ordered_list: list = list(file_list)
    ordered_list.sort()
    for file in enumerate(ordered_list):
        print(f"[{i}]: {file}")
    result = input(
        "If you wish to change the order enter the list"
        " of number separated by ',' ex: 1,2,3,4 otherwise"
        " if the order is okay enter empty line \n",
    )

    number_list = result.split(",")
    if not number_list:
        return ordered_list
    try:
        return [ordered_list[int(number)] for number in number_list]
    except ValueError as e:
        print(e)
        return ordered_list


def start() -> None:
    file_list = order_files(take_file_input())

    merger = PdfFileMerger()
    for pdf in file_list:
        merger.append(pdf)
    merger.write(take_output_file_name())
    merger.close()
