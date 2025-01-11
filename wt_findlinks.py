from posixpath import basename
import xml.etree.ElementTree as ET
import html
import os
import re
from bs4 import BeautifulSoup

def get_data(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Find the <data> tag
    data_tag = root.find('data')
    if data_tag is not None:
        # Extract the text content of the <data> tag
        data_content = data_tag.text
        
        # Convert HTML entities to literal characters
        data = html.unescape(data_content)
        return data
    else:
        print(f"No <data> tag found in the XML file: {xml_path}")
        return None
    
if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "wt-html"
    linkdict = {}
    namedict = {}
    for subdir, _, files in os.walk(xml_dir):
        for file in files:
            if file.endswith('.xml'):
                xml_path = os.path.join(subdir, file)
                data = get_data(xml_path)

                if data is None:
                    continue

                # links = re.findall(r'<a\shref="javascript:void\(0\)"\s+onclick="([^"]+)"\sid="([^"]+)"\sname="([^"]+)"\stitle="([^"]+)">(?:<< )?([^<>]+)(?:>>)?</a>', data)
                links = re.findall(r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">([^<]+)</a>\s*</li>', data)

                for link in links:
                    linkdict.update({link[1]: link[0]})
                    namedict.update({link[1]: link[2]})
                    
    for subdir, _, files in os.walk(os.path.join(xml_dir, "data")):
        for file in files:
            if file.endswith('.xml'):
                link = basename(file).split('.')[0]
                if link not in linkdict:
                    print(f"link {link} not found")
                    if link == "260787":
                        id = "/tipitaka/37P1/12/12.1/12.1.2/12.1.2.2"
                    else:
                        xml_path = os.path.join(subdir, file)
                        data = get_data(xml_path)
                        id = re.findall(r'<div\sclass="q"\sid="([^"]+)">', data)[0].replace("p_", "/tipitaka/")
                    name = re.findall(r'<div\sclass="i">([^<]+)</div>', data)[0]
                    print(f"link {link} not found, inferred id {id} name {name}")
