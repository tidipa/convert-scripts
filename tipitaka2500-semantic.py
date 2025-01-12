from posixpath import basename
import xml.etree.ElementTree as ET
import html
import os
import re
# import shutil
from bs4 import BeautifulSoup

from links import exceptions, linkdict, namedict
from html_template import html_header, html_footer

def get_data(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Find the <data> tag
    data_tag = root.find("data")

    # Extract the text content of the <data> tag
    data_content = data_tag.text

    # Convert HTML entities to literal characters
    data = html.unescape(data_content)
    return data

def tohtml(xml_path, output_path):
    data = get_data(xml_path)
    replaced_links = data

    links = re.findall(r'onclick="outD\(([^\),]+)(?:,[^\)]+)?\)"', data)
    for link in links:
        replaced_links = re.sub(link, linkdict[link], replaced_links)

    links = re.findall(r'<a\shref="javascript:void\(0\)"\s+onclick="([^"]+)"\sid="([^"]+)"\sname="([^"]+)"\stitle="([^"]+)">(?:<< )?([^<>]+)(?:>>)?</a>', replaced_links)
    for link in links:
        if link[2].isdigit():
            replaced_links = re.sub(link[2], linkdict[link[2]], replaced_links)

    replaced_links = re.sub(r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">([^<]+)</a>\s*</li>', r'<li name="\1"><a href="\2" class="btn btn-outline-primary btn-lg">\3</a></li>', replaced_links)
    replaced_links = re.sub(r'<a\shref="javascript:void\(0\)"\s+onclick="([^"]+)"\sid="([^"]+)"\sname="([^"]+)"\stitle="([^"]+)">(?:<< )?([^<>]+)(?:>>)?</a>', r'<a href="\3" id="\2" class="btn btn-outline-primary mt-2">\5</a>', replaced_links)
    
    # Hack to add .html to all links
    replaced_links = re.sub(r'href="/([^"]+)"', r'href="/\1.html"', replaced_links)

    html_output = html_header + replaced_links + html_footer

    # Pretty print the HTML content
    soup = BeautifulSoup(html_output, 'html.parser')
    pretty_html = soup.prettify()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Write the result to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(pretty_html)

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "tipitaka2500.github.io"

    for link, path in linkdict.items():
        if link in exceptions:
            continue

        xml_path = os.path.join(xml_dir, "data", link + ".xml")
        output_path = os.path.join(dst_dir, path[1:] + ".html")
        print(f"Converting {xml_path} to {output_path}")     
        tohtml(xml_path, output_path)

    for file in os.listdir(xml_dir):
        if file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, file)
            output_path = os.path.join(dst_dir, "tipitaka", os.path.splitext(file)[0] + ".html")
            print(f"Converting {xml_path} to {output_path}")
            tohtml(xml_path, output_path)