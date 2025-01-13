import os
import re
from bs4 import BeautifulSoup
from html_template import html_header, html_footer
from get_data import get_data

def tohtml(xml_path, output_path):
    converted_content = get_data(xml_path)

    replaced_links = re.sub(r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">([^<]+)</a>\s*</li>', r'<li name="\1"><a href="/tipitaka/data/\2.html" class="btn btn-outline-primary btn-lg">\3</a></li>', converted_content)
    replaced_links = re.sub(r'<a\shref="javascript:void\(0\)"\s+onclick="([^"]+)"\sid="([^"]+)"\sname="([^"]+)"\stitle="([^"]+)">(?:<< )?([^<>]+)(?:>>)?</a>', r'<a href="/tipitaka/data/\3.html" id="\2" class="btn btn-outline-primary mt-2">\5</a>', replaced_links)
    html_output = html_header + replaced_links + html_footer
    # Pretty print the HTML content
    soup = BeautifulSoup(html_output, 'html.parser')
    pretty_html = soup.prettify()
    
    # Write the result to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(pretty_html)
    
    print(f"Output written to {output_path}")

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

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    output_dir = "tipitaka2500.github.io/tipitaka"
    convert_texts(xml_dir, output_dir)
