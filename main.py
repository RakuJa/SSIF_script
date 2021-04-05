def check(file_name, string_to_search) -> list:
    to_return = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find(string_to_search) != -1:
                to_return.append(line)
    return to_return

def check_file_validity(file_name):
    if file_name == "":
        return False
    with open(file_name, 'r', encoding='utf-8'):
        return True
    


if __name__ == "__main__":
    keep_taking_input = True
    file_list =[]
    while keep_taking_input:
        file_name = input("Enter file path, Empty line to stop input")
        keep_taking_input = check_file_validity(file_name)
        if keep_taking_input:
            file_list.append(file_name)
            
    to_search = "Nome:Cognome"
    print ("\n Search started.... \n")
    for file_name in file_list:
        print("\n Starting search in " + file_name + "\n")
        print(check(file_name, to_search))
        print("\n" + file_name + "Searched...." + "\n")
    print("\n" + "Search over........." + "\n")


