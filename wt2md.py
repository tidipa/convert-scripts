import os
import re
from bs4 import BeautifulSoup, NavigableString

from links import exceptions, linkdict, namedict
from get_data import get_data

def tomd(link, xml_path, output_path):
    data = get_data(xml_path)

    # Parse data into HTML
    soup = BeautifulSoup(data, 'html.parser')

    # Create frontmatter
    frontmatter = "---\n"
    frontmatter += f"title: {namedict[link]}\n"
    frontmatter += f"path: {linkdict[link]}\n"
    frontmatter += f"ref: {link}\n"
    frontmatter += "breadcrumbs:\n"
    breadcrumbs = soup.find_all(class_="b")
    for breadcrumb in breadcrumbs:
        crumbs = breadcrumb('a')
        for crumb in crumbs:
            frontmatter += f"  - name: {crumb.string.strip()}\n"
            frontmatter += f"    link: {crumb['href']}\n"
    navfooter = soup.find_all(class_='plcb')
    for n in navfooter:
        links = n('a')
        for l in links:
            href = l['name']
            if href.isdigit():
                href = linkdict[href]
            frontmatter += f"{l['id']}: {href}\n"
    frontmatter += "---\n"

    # Create markdown
    markdown = '\n'
    for child in soup.children:
        if type(child) is NavigableString:
            if len(child.string.strip()) > 0:
                markdown += child.string + '\n\n'
        elif 'b' in child['class']:
            continue
        elif 'i' in child['class']:
            markdown += f"# {child.string.strip()}\n\n"
        elif 'h' in child['class']:
            markdown += f"### {child.string.strip()}\n\n"
        elif 'q' in child['class']:
            for c in child.children:
                if type(c) is NavigableString:
                    if len(c.string.strip()) > 0:
                        markdown += c.string + '\n\n'
                elif 'divNumber' in c['class']:
                    markdown += f"({c.string.strip()})\n\n"
                elif 'p' in c['class']:
                    for pc in c.children:
                        if type(pc) is NavigableString:
                            if len(pc.string.strip()) > 0:
                                markdown += pc.string + '\n\n'
                        elif 'pN' in pc['class']:
                            markdown += f"{pc.string.strip()}. "
                        elif pc.name == 'table':
                            tds = pc.find_all('td')
                            for td in tds:
                                for tde in td.children:
                                    if type(tde) is NavigableString:
                                        if len(tde.string.strip()) > 0:
                                            markdown += tde.string + '  \n'
                                    elif 'pN' in tde['class']:
                                        markdown += f"{tde.string.strip()}. "
                                    elif 'G' in tde['class']:
                                        markdown += '*' + tde.string + '*  \n'
                            markdown += '\n'
                        else:
                            print(f"Unhandled content in p {pc.name}")
                else:
                    print(f"Unhandled content in q {c['class']}")
        elif 'CENTER' in child['class'] or 'ENDH3' in child['class'] or 'ENDBOOK' in child['class']:
            markdown += '---\n\n'
            for c in child.children:
                if type(c) is NavigableString:
                    if len(c.string.strip()) > 0:
                        markdown += c.string
                elif c.name == 'br':
                    markdown += '  \n'
                elif 'pN' in c['class']:
                    markdown += f"({c.string.strip()}) "
                else:
                    print(f"Unhandled content in CENTER: {c.name}")
            markdown += '\n\n'
        elif 'tn' in child['class']:
            for c in child.children:
                if 'plcb' in c['class']:
                    continue
                elif 'menu' in c['class']:
                    menu = child.find(class_='menu')
                    links = menu.find_all('a')
                    for a in links:
                        markdown += f"* [{a.string.strip()}]({linkdict[re.sub(r'outD\(([0-9]+)\)', r'\1', a['onclick'])]})\n"
                    markdown += '\n'
                else:
                    print(f"Unhandled content in tn: {c.name}")
            markdown += '\n'
        elif 'plcb' in child['class']:
            continue
        else:
            print(f"Unhandled content {child['class']}")
        

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Write the result to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(frontmatter + markdown)

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "wt-md"

    print("Converting subdirs")
    for link, path in linkdict.items():
        if link in exceptions:
            continue

        xml_path = os.path.join(xml_dir, "data", link + ".xml")
        output_path = os.path.join(dst_dir, path[1:] + ".md")
        print(f"Converting {xml_path} to {output_path}")     
        tomd(link, xml_path, output_path)

    print("Converting menus")
    for file in os.listdir(xml_dir):
        if file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, file)
            output_path = os.path.join(dst_dir, "tipitaka", os.path.splitext(file)[0] + ".md")
            # print(f"Converting {xml_path} to {output_path}")
            # tomd2(file, xml_path, output_path)