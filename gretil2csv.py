import os
import re
import csv
import argparse
from bs4 import BeautifulSoup, NavigableString

# Defaults
input_files = ["gretil/2_pali/9_phil/gramm/balava_u.htm"]
output_dir = "gretilcsv"

page_num = 1
footer_num = 0
output_footnote = False
br_count = 0
csv_header = [ "document", "section", "page", "markup", "text" ]

def output_row(writer, text):
    global page_num, footer_num, output_footnote
    markup = 'text'
    newpage = re.findall(r'\[\\x ([ 0123456789]+)/\]', text)
    if newpage:
        page_num = int(newpage[0].strip())
        return
    
    if '*' in text[1:]:
        footer_num += 1
        text = text.replace('*', f'[^{footer_num}]')

    footerbreak = re.findall(r'^----------', text)

    if footerbreak:
        output_footnote = True
        return

    if text[0] == '*' and output_footnote:
        output_footnote = False
        text = text.replace('*', f'[^{footer_num}]: ')
        markup = 'footnote'

    writer.writerow([ '', '', page_num, markup, text ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert GRETIL htm files to csv with markup')
    parser.add_argument('-o', '--output_dir', default=output_dir, help='The outdir directory to write the CSV.')
    parser.add_argument('input_files', nargs='*', default=input_files, help='The input files from GRETIL.')
    args = parser.parse_args()
    # print(args.input_files, args.output_dir)

    for file in args.input_files:
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(file))[0] + '.csv')
        print(f'Converting {file} to {output_file}')
        with open(file, 'r') as filehandle, open(output_file, 'w') as output:
            writer = csv.writer(output)
            writer.writerow(csv_header)
            soup = BeautifulSoup(filehandle, 'html.parser')

            start = soup.find_all('hr')[1]

            for tag in start.next_siblings:
                if type(tag) is NavigableString:
                    text = tag.strip()
                    if len(text) > 0:
                        if br_count > 1:
                            br_count = 0
                            writer.writerow([ '', '', page_num, 'break', '' ])
                        output_row(writer, text)
                elif tag.name == 'br':
                    br_count += 1
                else:
                    print(tag.prettify())
