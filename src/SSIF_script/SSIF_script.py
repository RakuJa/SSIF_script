import sys
from itertools import chain
import os
from os import listdir
from os.path import isfile, join
from src import interface

tutorial_name = "SSIF_tutorial.md"


def pdf_to_text(file_name) -> str:
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    import io

    fp = open(file_name, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data = retstr.getvalue()

    return data


def parse_pdf(file_name, string_to_search) -> list:
    data = pdf_to_text(file_name)
    tmp_file = file_name + ".txt"
    write_info_to_file("", data, tmp_file, "")
    tmp = parse_txt(tmp_file, string_to_search)
    os.remove(tmp_file)
    return tmp


def parse_txt_data(data, string_to_search) -> list:
    to_return = []
    for line in data:
        if line.find(string_to_search) != -1:
            to_return.append(line)
    return to_return


def parse_txt(file_name, string_to_search) -> list:
    with open(file_name, 'r', encoding='utf-8') as f:
        data = f.readlines()
        tmp = parse_txt_data(data, string_to_search)
        return tmp


def check_extension(file_name, string_to_search) -> list:
    if file_name.lower().endswith('.txt'):
        return parse_txt(file_name, string_to_search)
    if file_name.lower().endswith('.pdf'):
        return parse_pdf(file_name, string_to_search)


def check_file_validity(file_name) -> bool:
    with open(file_name, 'r', encoding='utf-8'):
        return True
    return False


def take_all_files(my_path) -> list:
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
    return only_files


def remove_duplicates(list_to_clean_up) -> bool:
    clean_list = list(set(list_to_clean_up))
    for item in clean_list:
        check_file_validity(item)
    return clean_list


def take_file_input() -> list:
    keep_taking_input = True
    file_list = []
    while keep_taking_input:
        file_name = input("Enter file path, Empty line to stop input ")
        if file_name == "ALL":
            file_list = take_all_files(os.getcwd())
        elif file_name == "":
            keep_taking_input = False
        else:
            file_list.append(file_name)
    file_list = remove_duplicates(file_list)
    return file_list


def write_info_to_file(info_string, flattened_list, file_name="results.txt", separator=' \n') -> bool:
    with open(file_name, 'a') as f:
        print(info_string, file=f)
        print(*flattened_list, sep=separator, file=f)


def print_instructions():
    text = "[1] Tutorial \n" + "[2] Continua esecuzione \n" + "[7] Credits   [9] Exit \n"
    print(interface.bordered(text))


def require_input():
    choice = input("Enter Your Choice in the Keyboard [1,2,7,9] : ")
    return choice.upper()


def start():
    print_instructions()
    keep_asking_input = True
    while keep_asking_input:
        choice = require_input()
        if choice == '1' or choice == 'TUTORIAL':
            interface.print_file(tutorial_name)
        elif choice == '2' or choice == 'CONTINUE':
            keep_asking_input = False
        elif choice == '7' or choice == 'CREDITS':
            print("https://github.com/RakuJa")
        elif choice == '9' or choice == 'EXIT':
            sys.exit()

    options = input("Enter options like this : -v -f or press enter")

    write_to_file = options.find('-f') != -1

    verbose = options.find('-v') != -1

    file_list = take_file_input()
    to_search = input("Enter string to search ")

    print("\n Search started.... \n")
    occurrences_list = []
    for file_name in file_list:
        if verbose:
            print("\n Starting search in " + file_name + "\n")
        tmp = check_extension(file_name, to_search)
        if tmp is not None:
            occurrences_list.append(tmp)
        if verbose:
            print("\n" + file_name + " Searched...." + "\n")
    if verbose:
        print("\n" + "Search over........." + "\n")

    flattened_list = list(chain(*occurrences_list))
    prepare_string = "Found in " + str(len(occurrences_list)) + " files \n" + "Found " + str(
        len(flattened_list)) + " occurrences of the string \n" + "Here's the list \n"
    print(prepare_string)
    print(*flattened_list, sep=' \n')

    if write_to_file:
        write_info_to_file(prepare_string, flattened_list)

    x = input(" Would you like to restart the script? Y/N")
    if x == "Y" or x == "y":
        os.startfile(__file__)
        sys.exit()
