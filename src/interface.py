from pathlib import Path


def bordered(text: str) -> str:
    """
    Gets a string as input and as output gives the same
     string contained in "borders". Used to pretty print
    """
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = (
        ["┌" + "─" * width + "┐"]
        + ["│" + (s + " " * width)[:width] + "│" for s in lines]
        + ["└" + "─" * width + "┘"]
    )
    return "\n".join(res)


def print_file(file_name: str) -> None:
    with (Path.cwd() / file_name).open() as f:
        print(bordered(f.read()))
