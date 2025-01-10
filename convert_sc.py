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

def convert_texts(root_dir, html_dir, output_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.json'):
                relative_path = os.path.relpath(os.path.join(subdir, file), root_dir)
                root_path = os.path.join(subdir, file)
                html_path = os.path.join(html_dir, relative_path).replace("_root-pli-ms", "_html")
                output_path = os.path.join(output_dir, relative_path).replace("_root-pli-ms.json", ".html")
                output_dir1 = os.path.dirname(output_path)
                
                if not os.path.exists(output_dir1):
                    os.makedirs(output_dir1)
                text2html(root_path, html_path, output_path)                # text2html(root_dir, html_dir, relative_path)

def to_markdown(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    markdown_content = markdownify.markdownify(html_content, heading_style="ATX")
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print(f"Converted {file_path} to {output_path}")

def sc_markdown(html_dir, markdown_dir):
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
    root_dir = "bilara-data/root/pli/ms"
    html_dir = "bilara-data/html/pli/ms"
    output_dir = "sc-html"
    convert_texts(root_dir, html_dir, output_dir)

    html_dir = "sc-html"
    markdown_dir = "sc-markdown"
    sc_markdown(html_dir, markdown_dir)