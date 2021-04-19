import os
import sys

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)

def print_readme():
    import markdown
    from bs4 import BeautifulSoup
    
    html = markdown.markdown(open("readme.md").read())
    x = BeautifulSoup(html, features="html.parser").findAll(text=True)
    print("\n")
    for line in x:
        print(line)
    print("\n")

def print_instructions():
    text = "[1] Read Me \n"+"[2] File merger \n"+"[3] Search string in file \n"+"[7] Credits  [8] Instructions  [9] Exit \n"
    print(bordered(text))
    
def require_input():
    choice = input("Enter Your Choice in the Keyboard [1,2,3,7,9] : ")
    return choice.upper()

if __name__ == "__main__":
    
    current_path = os.getcwd()
    
    file_merger_path = os.path.join("file_merger", "file_merger.py")
    file_merger_path = os.path.join(current_path, file_merger_path)
    
    ssif_path = os.path.join("SSIF_script", "SSIF_script.py")
    ssif_path = os.path.join(current_path, ssif_path)
    print_instructions()

    while(True):
        choice = require_input()
        if choice=='1' or choice=='READ':
            print_readme()
        elif choice=='2' or choice=='MERGER':
            os.startfile(file_merger_path)
            sys.exit()
        elif choice=='3' or choice=='SSIF' or choice=='SEARCH':
            os.startfile(ssif_path)
            sys.exit()
        elif choice=='7' or choice=='CREDITS':
            print("https://github.com/RakuJa")
        elif choice=='8' or choice=='INSTRUCTIONS':
            print_instructions()
        elif choice=='9' or choice=='EXIT':
            sys.exit()
    

    


