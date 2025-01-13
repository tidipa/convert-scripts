import xml.etree.ElementTree as ET
import html

def get_data(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Find the <data> tag
    data_tag = root.find("data")
    if data_tag is not None:
        # Extract the text content of the <data> tag
        data_content = data_tag.text

        # Convert HTML entities to literal characters
        data = html.unescape(data_content)
        return data
    else:
        print(f"No <data> tag found in the XML file: {xml_path}")
        return None
