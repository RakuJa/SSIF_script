import os


def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ["┌" + "─" * width + "┐"]
    for s in lines:
        res.append("│" + (s + " " * width)[:width] + "│")
    res.append("└" + "─" * width + "┘")
    return "\n".join(res)


def print_file(file_name):
    current_path = os.getcwd()
    path_to_tutorial = os.path.join(current_path, file_name)
    text = open(path_to_tutorial).read()
    print(bordered(text))
