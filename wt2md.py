import os
from posixpath import basename
import re
from bs4 import BeautifulSoup, NavigableString

from links import exceptions, linkdict, namedict
from get_data import get_data

def unhandled(item, name):
    print(f"Unhandled content in {name}:")
    print(item.prettify())
    exit(1)

def convert_section(s, name):
    markdown = ''
    for c in s.children:
        if type(c) is NavigableString:
            if len(c.string.strip()) > 0:
                markdown += c.string.strip() + '\n\n'
        elif c.name == 'br':
            markdown += '  \n'
        elif 'pN' in c['class']:
            markdown += f"{c.string.strip()}. "
        elif c.name == 'table':
            tds = c.find_all('td')
            for td in tds:
                for tde in td.children:
                    if type(tde) is NavigableString:
                        if len(tde.string.strip()) > 0:
                            markdown += tde.string + '  \n'
                    elif 'pN' in tde['class']:
                        markdown += f"{tde.string.strip()}. "
                    elif 'G' in tde['class']:
                        # print(tde.prettify())
                        markdown += '_' + tde.string.strip() + '_  \n'
            markdown += '\n\n'
        else:
            unhandled(c, name)

    return markdown

def do_menu(menu):
    markdown = ''
    links = menu.find_all('a')
    for a in links:
        markdown += f"* [{a.string.strip()}]({linkdict[re.sub(r'outD\(([0-9]+)\)', r'\1', a['onclick'])]})\n"
    markdown += '\n'

    return markdown

def tomd(link, xml_path, output_path):
    data = get_data(xml_path)

    # Parse data into HTML
    soup = BeautifulSoup(data, 'html.parser')

    # Create frontmatter
    frontmatter = "---\n"
    if link is None:
        title = os.path.splitext(basename(xml_path))[0]
        path = '/tipitaka/' + title + '.html'
    else:
        title = namedict[link]
        path = linkdict[link]
    frontmatter += f"title: {title}\n"
    frontmatter += f"path: {path}\n"
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

    # Convert bespoke markup to markdown
    gqs = soup.find_all(class_='gathaQuote')
    for gq in gqs:
        p = gq.parent
        gq.string = '__' + gq.string.strip() + '__'
        gq.unwrap()
        p.smooth()

    bolds = soup.find_all(class_='bold')
    for bold in bolds:
        if bold.string is None:
            unhandled(bold, 'bold')
        bold.string = '**' + bold.string.strip() + '**'
        bold.unwrap()

    italics = soup.find_all(class_='italic')
    for italic in italics:
        italic.string = '*' + italic.string.strip() + '*'
        italic.unwrap()

    rlaps = soup.find_all(class_='RLAP')
    for rlap in rlaps:
        rlap.string = '(' + rlap.string.strip() + ')'
        rlap.unwrap()

    firsts = soup.find_all(class_='firstLetter')
    for first in firsts:
        first.unwrap()

    firsts = soup.find_all(class_='smallFont')
    for first in firsts:
        first.unwrap()

    soup.smooth()

    # Create markdown
    markdown = '\n'
    for child in soup.children:
        if type(child) is NavigableString:
            if len(child.string.strip()) > 0:
                print(f"Discarded extra text: {child.string}")
                # markdown += child.string + '\n\n'
        elif 'b' in child['class']:
            continue
        elif 'i' in child['class']:
            markdown += f"# {child.string.strip()}\n\n"
        elif 'h' in child['class']:
            if child.string is not None:
                markdown += f"### {child.string.strip()}\n\n"
        elif 'q' in child['class']:
            for c in child.children:
                if type(c) is NavigableString:
                    if len(c.string.strip()) > 0:
                        markdown += c.string + '\n\n'
                elif 'divNumber' in c['class']:
                    markdown += f"({c.string.strip()})\n\n"
                elif 'p' in c['class']:
                    # print(c.prettify())
                    markdown += convert_section(c, 'p')
                elif 'paliSectionName' in c['class']:
                    markdown += "## "
                    markdown += convert_section(c, 'paliSectionName')
                else:
                    unhandled(c, 'q')
        elif 'CENTER' in child['class'] or 'ENDH3' in child['class'] or 'ENDBOOK' in child['class'] or 'SUMMARY' in child['class']:
            markdown += '===\n\n'
            markdown += convert_section(child, child['class'])
            markdown += '\n\n'
        elif 'tn' in child['class']:
            for c in child.children:
                if 'plcb' in c['class']:
                    continue
                elif 'menu' in c['class']:
                    markdown += do_menu(child.find(class_='menu'))
                else:
                    unhandled(c,'tn')
            markdown += '\n'
        elif 'plcb' in child['class']:
            continue
        elif 'content' in child['class']:
            markdown += do_menu(child.find(class_='menu'))
        else:
            unhandled(child, 'top')
        

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Write the result to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(frontmatter + markdown)

if __name__ == "__main__":
    xml_dir = "World-Tipitaka/tipitaka"
    dst_dir = "tipitaka2500"

    print("Converting subdirs")
    for link, path in linkdict.items():
        if link in exceptions:
            continue

        xml_path = os.path.join(xml_dir, "data", link + ".xml")
        output_path = os.path.join(dst_dir, path[1:] + ".md")
        # print(f"Converting {xml_path} to {output_path}")     
        tomd(link, xml_path, output_path)

    print("Converting menus")
    for file in os.listdir(xml_dir):
        if file.endswith(".xml"):
            xml_path = os.path.join(xml_dir, file)
            output_path = os.path.join(dst_dir, "tipitaka", os.path.splitext(file)[0] + ".md")
            # print(f"Converting {xml_path} to {output_path}")
            tomd(None, xml_path, output_path)