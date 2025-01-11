import xml.etree.ElementTree as ET
import html
import os
import re
from bs4 import BeautifulSoup
import markdownify

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
        replaced_links = re.sub(r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">([^<]+)</a>\s*</li>', r'<li name="\1"><a href="/tipitaka/data/\2.html">\3</a></li>', converted_content)
        replaced_links = re.sub(r'<a\shref="javascript:void\(0\)"\s+onclick="([^"]+)"\sid="([^"]+)"\sname="([^"]+)"\stitle="([^"]+)">(?:<< )?([^<>]+)(?:>>)?</a>', r'<a href="/tipitaka/data/\3.html" id="\2">\5</a>', replaced_links)
        html_output = replaced_links
        # Pretty print the HTML content
        soup = BeautifulSoup(html_output, 'html.parser')
        pretty_html = soup.prettify()
        
        # Write the result to the output file
        with open(output_path, 'w') as output_file:
            output_file.write(pretty_html)
        
        print(f"Output written to {output_path}")
    else:
        print(f"No <data> tag found in the XML file: {xml_path}")

def convert_texts(xml_dir, output_dir):
    for subdir, _, files in os.walk(xml_dir):
        for file in files:
            if file.endswith('.xml'):
                relative_path = os.path.relpath(os.path.join(subdir, file), xml_dir)
                xml_path = os.path.join(subdir, file)
                output_path = os.path.join(output_dir, relative_path).replace(".xml", ".html")
                output_dir1 = os.path.dirname(output_path)
                
                if not os.path.exists(output_dir1):
                    os.makedirs(output_dir1)
                tohtml(xml_path, output_path)   

def to_markdown(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_content = markdownify.markdownify(html_content, heading_style="ATX")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print(f"Converted {file_path} to {output_path}")

def wt_markdown(html_dir, markdown_dir):
    for root, _, files in os.walk(html_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                output_path = os.path.splitext(file_path)[0] + ".md"
                output_path = output_path.replace(html_dir, markdown_dir)
                output_dir = os.path.dirname(output_path)
                
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                to_markdown(file_path, output_path)

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    output_dir = "wt-html/tipitaka"
    convert_texts(xml_dir, output_dir)

    markdown_dir = "wt-markdown"
    # wt_markdown(output_dir, markdown_dir)