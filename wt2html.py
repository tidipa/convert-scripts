import xml.etree.ElementTree as ET
import html
import sys
import os
from bs4 import BeautifulSoup

def extract_and_convert(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Find the <data> tag
    data_tag = root.find('data')
    if data_tag is not None:
        # Extract the text content of the <data> tag
        data_content = data_tag.text
        
        # Convert HTML entities to literal characters
        converted_content = html.unescape(data_content)
        
        # Pretty print the HTML content
        soup = BeautifulSoup(converted_content, 'html.parser')
        pretty_html = soup.prettify()
        
        # Determine the output file path
        base_name = os.path.basename(file_path)
        output_file_path = os.path.splitext(base_name)[0] + '.html'
        
        # Write the result to the output file
        with open(output_file_path, 'w') as output_file:
            output_file.write(pretty_html)
        
        print(f"Output written to {output_file_path}")
    else:
        print(f"No <data> tag found in the XML file: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wt2html.py <path_to_xml_file1> <path_to_xml_file2> ...")
    else:
        for file_path in sys.argv[1:]:
            extract_and_convert(file_path)