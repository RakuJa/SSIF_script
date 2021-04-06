#!/usr/bin/python
import sys,getopt
from itertools import chain
import os
from os import listdir
from os.path import isfile, join
from contextlib import redirect_stdout

def check(file_name, string_to_search) -> list:
    to_return = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find(string_to_search) != -1:
                to_return.append(line)
    return to_return

def check_file_validity(file_name) -> bool:
    with open(file_name, 'r', encoding='utf-8'):
        return True
    return False

def take_all_files(mypath) -> list:
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

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
            file_list = take_all_files(os.getcwd())
        elif file_name == "":
            keep_taking_input = False
        else:
            file_list.append(file_name)
    file_list = remove_duplicates(file_list)
    return file_list

def write_info_to_file(info_string, flattened_list) -> bool:
    with open("results.txt", 'a') as f:
        print(info_string, file=f)
        print(*flattened_list, sep=' \n', file=f)

def print_tutorial():
    print("This script will search for a string inside a list of files (1..n) \n")
    print("You will be asked to input firstly the option (this field can be empty) \n")
    print("Options list: \n")
    print("-v will set verbose option on, this will make the script print a lot more, it will make " +\
          "you understand more how much you have scanned and what \n")
    print("-f will print the output of the script to a file named results.txt \n")
    print("-h will display the help option, this wall of text \n")

    print("Do you wish to continue the execution with the option you have already inputted? \n")
    while (True):
        answer = input("Y/N")
        if answer == "N":
            os.startfile(__file__)
            sys.exit()
        if answer == "Y":
            return;
          
    
        
    
if __name__ == "__main__":

    options = input("Enter options like this : -h -v -f or press enter")

    if options.find('-h') != -1:
        print_tutorial()

    write_to_file = options.find('-f') != -1
    
    verbose =  options.find('-v') != -1
    
    file_list = take_file_input()
    to_search = input("Enter string to search ")
    
    
        
    print ("\n Search started.... \n")
    occurrences_list = []
    for file_name in file_list:
        if verbose :
            print("\n Starting search in " + file_name + "\n")
        tmp = check(file_name, to_search)
        occurrences_list.append(tmp)
        if verbose :
            print("\n" + file_name + " Searched...." + "\n")
    if verbose :
        print("\n" + "Search over........." + "\n")

    flattened_list = list(chain(*occurrences_list))
    prepare_string = "Scanned " + str(len(occurrences_list)) + " files \n" + "Found " + str(len(flattened_list)) + " occurrences of the string \n" + "Here's the list \n"
    print(prepare_string)
    print(*flattened_list, sep=' \n')
    
    if write_to_file:
        write_info_to_file(prepare_string, flattened_list)

    x = input(" Would you like to restart the script? Y/N")
    if x=="Y" or x=="y":
        os.startfile(__file__)
        sys.exit()
        
        


