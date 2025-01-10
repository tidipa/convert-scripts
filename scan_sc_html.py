import os
import json
from bs4 import BeautifulSoup
import markdownify

def text2html(root_path, html_path, output_path):
    with open(root_path, 'r', encoding='utf-8') as root_file:
        root = json.load(root_file)

        try:
            with open(html_path, 'r', encoding='utf-8') as html_file:
                html = json.load(html_file)
        except FileNotFoundError:
            html = {}
            print('No HTML for {}'.format(root_path))

        print('Writing {}'.format(output_path))
        with open(output_path, 'w') as output_file:
            for segment_id, value in root.items():
                if (segment_id in html):
                    output_file.write(html[segment_id].format(value) + '\n')
                else:
                    print('No HTML for {}'.format(segment_id))
                    output_file.write(value + '\n')

def scan(html_dir):
    for subdir, _, files in os.walk(html_dir):
        for file in files:
            if file.endswith('.json'):
                html_json = os.path.join(subdir, file)
                with open(html_json, 'r', encoding='utf-8') as html_file:
                    html = json.load(html_file)
                    for segment_id, value in html.items():
                        print(value)


if __name__ == "__main__":
    html_dir = "bilara-data/html/pli/ms"
    scan(html_dir)
