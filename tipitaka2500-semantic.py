import xml.etree.ElementTree as ET
import html
import os
import re
from bs4 import BeautifulSoup, NavigableString

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

    replaced_links = re.sub(r'<li\sname="([^"]+)">\s*<a\shref="javascript:void\(0\)"\sonclick="outD\(([^\)]+)\)">([^<]+)</a>\s*</li>', r'<li name="\1"><a href="\2">\3</a></li>', replaced_links)
    replaced_links = re.sub(r'<a\shref="javascript:void\(0\)"\s+onclick="([^"]+)"\sid="([^"]+)"\sname="([^"]+)"\stitle="([^"]+)">(?:<< )?([^<>]+)(?:>>)?</a>', r'<a href="\3" id="\2">\5</a>', replaced_links)
    
    # Hack to add .html to all links
    replaced_links = re.sub(r'href="/([^"]+)"', r'href="/\1.html"', replaced_links)

    html_output = html_header + replaced_links + html_footer

    # Pretty print the HTML content
    soup = BeautifulSoup(html_output, 'html.parser')

    # Modify breadcrumb to use Bootstrap
    breadcrumbs = soup.find_all(class_="b")
    for breadcrumb in breadcrumbs:
        breadcrumb.name = 'ol'
        breadcrumb['class'] = 'breadcrumb'
        navtag = breadcrumb.wrap(soup.new_tag('nav'))
        navtag['aria-label'] = 'breadcrumb'
        crumbs = breadcrumb('a')
        for crumb in crumbs:
            li = crumb.wrap(soup.new_tag('li'))
            li['class'] = 'breadcrumb-item'
        for item in breadcrumb.children:
            if isinstance(item, NavigableString):
                item.extract()

    # Convert heading
    titles = soup.find_all(class_="i")
    for title in titles:
        title['class'] = 'text-body-emphasis'
        title.name = 'h1'
        container = title.wrap(soup.new_tag('div'))
        container['class'] = 'm-4 p-4 text-center bg-body-tertiary rounded-3'
        div = container.wrap(soup.new_tag('div'))
        div['class'] = 'container'
    
    headings = soup.find_all(class_="h")
    for heading in headings:
        heading.name = 'h2'
        heading['class'] = 'text-center'

    # Convert main content
    divs = soup.find_all(class_="divNumber")
    for div in divs:
        div.name = 'span'
        div['class'] = "badge rounded-pill text-bg-secondary float-start me-2"

    pns = soup.find_all(class_="pN")
    for pn in pns:
        pn.name = 'a'
        pn['href'] = '#' + pn.string.strip()
        pn['class'] = 'badge rounded-pill text-bg-light'

    paras = soup.find_all(class_="p")
    for p in paras:
        p.name = 'p'
        del p['class']

    qs = soup.find_all(class_="q")
    for q in qs:
        del q['class']

    centers = soup.find_all(class_="CENTER")
    for center in centers:
        center.name = 'p'
        center['class'] = 'text-center lead'

    # Convert footer
    tags = soup.find_all(class_='tn')
    for tag in tags:
        tag['class'] = 'fixed_bottom container'

    tags = soup.find_all(class_='plcb')
    for tag in tags:
        tag.name = 'footer'
        tag['class'] = 'row align-items-center py-4 my-4 border-top'

    tags = soup.find_all(id='prevL')
    for tag in tags:
        tag['id'] = 'Previous'
        tag['class'] = 'col order-1 btn btn-outline-primary'

    tags = soup.find_all(id='upL')
    for tag in tags:
        tag['id'] = 'Up'
        tag['class'] = 'col order-2 btn btn-outline-primary'

    tags = soup.find_all(id='nextL')
    for tag in tags:
        tag['id'] = 'Next'
        tag['class'] = 'col order-3 btn btn-outline-primary'

    # Convert menus
    menus = soup.find_all(class_='menu')
    for menu in menus:
        menu['class'] = 'list-group'
        links = menu.find_all('li')
        for link in links:
            link['class'] = 'list-group-item list-group-item-action'

    pretty_html = soup.prettify()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Write the result to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(pretty_html)

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "tipitaka2500.github.io"

    print("Converting subdirs")
    for link, path in linkdict.items():
        if link in exceptions:
            continue

        xml_path = os.path.join(xml_dir, "data", link + ".xml")
        output_path = os.path.join(dst_dir, path[1:] + ".html")
        # print(f"Converting {xml_path} to {output_path}")     
        tohtml(xml_path, output_path)

    print("Converting menus")
    for file in os.listdir(xml_dir):
        if file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, file)
            output_path = os.path.join(dst_dir, "tipitaka", os.path.splitext(file)[0] + ".html")
            # print(f"Converting {xml_path} to {output_path}")
            tohtml(xml_path, output_path)