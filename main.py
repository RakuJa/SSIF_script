def check(file_name, string_to_search) -> list:
    to_return = []
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find(string_to_search) != -1:
                to_return.append(line)
    return to_return


if __name__ == "__main__":
    #file_name = input("Enter file path")
    #to_search = input("String to search in file")
    file_name = "0.txt"
    to_search = "Nome:Cognome"
    print(check(file_name, to_search))


