from PyPDF2 import PdfFileMerger
import os


def check_file_validity(file_name) -> bool:
    with open(file_name, 'r', encoding='utf-8'):
        return True
    return False

def remove_duplicates(list_to_clean_up) -> bool:
    clean_list = list(set(list_to_clean_up))
    for item in clean_list:
        check_file_validity(item)
    return clean_list

def take_file_input() -> list:
    keep_taking_input = True
    file_list =[]
    while keep_taking_input:
        file_name = input("Enter file path, Empty line to stop input ")
        if file_name == "ALL":
            file_list = [a for a in os.listdir() if a.endswith(".pdf")]
        elif file_name == "":
            keep_taking_input = False
        else:
            file_list.append(file_name)
    file_list = remove_duplicates(file_list)
    return file_list

if __name__ == "__main__":
    file_list = take_file_input()
    merger = PdfFileMerger()
    for pdf in file_list:
        merger.append(pdf)
    merger.write("result.pdf")
    merger.close()

