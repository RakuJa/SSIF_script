def check(file_name, string_to_search):
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find(string_to_search) != -1:
                print(line)
    # return open(file_name, 'r', encoding='utf-8').read().find(string_to_search)


if __name__ == "__main__":
    #file_name = input("Enter file path")
    #to_search = input("String to search in file")
    file_name = "0.txt"
    to_search = "Sara"
    print(check(file_name, to_search))


