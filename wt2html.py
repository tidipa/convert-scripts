from hmac import new
from posixpath import basename
import xml.etree.ElementTree as ET
import html
import os
import re
from bs4 import BeautifulSoup
from get_data import get_data
from links import exceptions

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "wt-html"
    for subdir, _, files in os.walk(xml_dir):
        for file in files:
            if file.endswith(".xml"):
                link = basename(file).split(".")[0]

                if link in exceptions:
                    continue
            
                xml_path = os.path.join(subdir, file)
                data = get_data(xml_path)
                
                # Pretty print the HTML content
                soup = BeautifulSoup(data, 'html.parser')
                pretty_html = soup.prettify()

                output_path = os.path.splitext(xml_path)[0] + ".md"
                output_path = output_path.replace(xml_dir, dst_dir)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Write the result to the output file
                with open(output_path, 'w') as output_file:
                    output_file.write(pretty_html)