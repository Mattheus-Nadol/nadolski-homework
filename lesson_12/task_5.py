"""Simple file-read demo.

Attempts to open and print a file called 'nonexistent.txt' and demonstrates
basic FileNotFoundError handling.
"""

def read_file():
    """Try to open and print the contents of 'nonexistent.txt'.

    Prints the file content if found, otherwise prints an error message.
    """
    try:
        with open("nonexistent.txt", "r", encoding="utf-8") as file:
            file_content = file.read()
            print("File content: \n ", file_content)
    except FileNotFoundError:
        print("Unfortunately, your file was not found.")

read_file()
