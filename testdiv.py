import re
import sys

def divide_file_sections(filename):
    header = ""
    text = ""
    footer = ""

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    section = "header"

    for line in lines:
        if section == "header" and line.strip().startswith('#'):
            section = "text"
        
        if section == "text" and line.strip().startswith('['):
            section = "footer"

        if section == "header":
            header += line
        elif section == "text":
            text += line
        elif section == "footer":
            footer += line

    return header, text, footer


# Example usage
if __name__ == "__main__":
    filename = sys.argv[1]  # Replace with the actual file path
    header, text, footer = divide_file_sections(filename)

    print ("Header section:")
    print(header)
    print ("Text section:")
    print(text)
    print ("Footer section:")
    print(footer)
