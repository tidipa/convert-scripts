import xml.etree.ElementTree as ET
import html
import os
import re
# import shutil
from bs4 import BeautifulSoup

def tohtml(xml_path, output_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Find the <data> tag
    data_tag = root.find('data')
    if data_tag is not None:
        # Extract the text content of the <data> tag
        data_content = data_tag.text
        
        # Convert HTML entities to literal characters
        converted_content = html.unescape(data_content)
        replaced_links = re.sub(r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">([^<]+)</a>\s*</li>', r'<li name="\1"><a href="\1.html">\3</a></li>', converted_content)
        
        # Pretty print the HTML content
        soup = BeautifulSoup(replaced_links, 'html.parser')
        pretty_html = soup.prettify()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Write the result to the output file
        with open(output_path, 'w') as output_file:
            output_file.write(pretty_html)
        
        print(f"Output written to {output_path}")
    else:
        print(f"No <data> tag found in the XML file: {xml_path}")

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "wt-html"
    for subdir, _, files in os.walk(xml_dir):
        for file in files:
            if file.endswith('.xml'):
                xml_path = os.path.join(subdir, file)
                tree = ET.parse(xml_path)
                root = tree.getroot()
                
                # Find the <data> tag
                data_tag = root.find('data')
                if data_tag is not None:
                    # Extract the text content of the <data> tag
                    data_content = data_tag.text
                    
                    # Convert HTML entities to literal characters
                    data = html.unescape(data_content)
                    links = re.findall(r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">[^<]+</a>\s*</li>', data)
                    for link in links:
                        xml_path = os.path.join(xml_dir, "data", link[1] + ".xml")
                        output_path= dst_dir + link[0] + ".html"
                        tohtml(xml_path, output_path)
                        # print(f"Copying {src} to {dst}")
                        # os.makedirs(os.path.dirname(dst), exist_ok=True)
                        # shutil.copy2(src, dst)