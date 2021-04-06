from itertools import chain

def check(file_name, string_to_search) -> list:
    to_return = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find(string_to_search) != -1:
                to_return.append(line)
    return to_return

def check_file_validity(file_name) -> bool:
    if file_name == "":
        return False
    with open(file_name, 'r', encoding='utf-8'):
        return True

def take_file_input() -> list:
    keep_taking_input = True
    file_list =[]
    while keep_taking_input:
        file_name = input("Enter file path, Empty line to stop input ")
        keep_taking_input = check_file_validity(file_name)
        if keep_taking_input:
            file_list.append(file_name)
    return file_list

def write_info_to_file() -> bool:
    pass
    
    
if __name__ == "__main__":
    
    file_list = take_file_input()
    to_search = input("Enter string to search ")
    print ("\n Search started.... \n")
    occurrences_list = []
    for file_name in file_list:
        print("\n Starting search in " + file_name + "\n")
        tmp = check(file_name, to_search)
        occurrences_list.append(tmp)
        print("\n" + file_name + "Searched...." + "\n")
    print("\n" + "Search over........." + "\n")

    print( "Found the string in " + str(len(occurrences_list)) + " files \n")
    flattened_list = list(chain(*occurrences_list))
    print("Found " + str(len(flattened_list)) + " occurrences of the string \n")

    print("Here's the list \n")
    print(*flattened_list, sep=' \n')


