# wt2eng-gemini.py
#
# Pali to English translator and summariser for markdown files
# Uses Google GenAI library with Gemini Pro
# Takes filenames or directories as command line arguments
# (by default all files in "tipitaka2500/tipitaka" directory)
# Then summarise each file into "tipitaka2500-eng/gemini/" directory
# as Markdown with headings retained where appropriate and bullet points in content.
# Accepted file extensions: .md

import re
import sys
import os
import argparse
from tqdm import tqdm
# import frontmatter

## Google GenAI API
from google import genai
from google.genai import types

# from bilara-data..scripts import num
from google.api_core import retry
from google.api_core import exceptions

INPUT_DIR="tipitaka2500/tipitaka"
OUTPUT_DIR="tipitaka2500-eng/staging"
MODEL="models/gemini-2.5-pro-preview-05-06"
MAX_TOKENS = 8192
TEMPERATURE=0.3

SYSTEM = """
You are an efficient and accurate Pali to English translator.

## Instructions

Step 1. Read the entire text.
Step 2. Translate the text as accurately as possible. Do not insert any additional text or explanations.
Step 3. Don't include preambles, postambles or explanations.
Step 4. Leave honorifics and vocatives like Buddha, bhikkhave etc. untranslated.
Step 5. For Buddhist technical terms eg. nibbāna, quote the Pāli word with English equivalent in parentheses eg. "nibbāna (extinguishment)"
Step 6. Output the translation only, preserving formatting of the input text, including Markdown headings and other formatting.
"""

client = genai.Client()

# Retry when rate limit reached
is_retriable = lambda e: isinstance(e, (exceptions.ResourceExhausted, exceptions.ServiceUnavailable))
retry_decorator = retry.Retry(predicate=is_retriable)
generate_content = retry_decorator(client.models.generate_content)

def output_file(s, prefix):
    input_prefix = INPUT_DIR + "/"

    # Strip _input/ prefix if it exists
    if s.startswith(input_prefix):
        s = s[len(input_prefix):]

    # Add _output/ prefix
    s = os.path.join(prefix, s)

    return s

def output_summary(filename: str, summary: str):
    base = os.path.splitext(filename)[0]

    summary_file = output_file(f"{base}.md", OUTPUT_DIR + '/')
    # original = output_file(filename, "")
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    with open(summary_file, 'w') as file:
        file.write(summary)
    # print(f'Translated [{summary_file}]\n')

def divide_file_sections(filename):
    header = ""
    title = ""
    text = ""
    footer = ""

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    section = "header"

    text_begin = re.compile(r'^\(?\d+')\
    
    for line in lines:
        if section == "header" and line.strip().startswith('#'):
            section = "title"
        
        if section == "title" and text_begin.match(line.strip()):
            section = "text"
        
        if section == "text" and line.strip().startswith('['):
            section = "footer"

        if section == "header":
            header += line
        elif section == "title":
            title += line
        elif section == "text":
            text += line
        elif section == "footer":
            footer += line

    return header, title, text, footer

def output_md(filename):
    header, title, pali, footer = divide_file_sections(filename)
    # fm = frontmatter.loads(markdown)

    with tqdm(total=4, desc="Translating") as pbar:
        pbar.set_description("Translating")
        text = ""
        while text is None or text == "":
            translation = generate_content(
                model=MODEL,
                contents=[pali],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM,
                    max_output_tokens=MAX_TOKENS,
                    temperature=TEMPERATURE,
                ),
            )
            text = translation.text

        pbar.update(1)
        pbar.set_description("Summary")
        summary_prompt = "Given the following text, provide a summary of the key points in a single paragraph."
        summary = generate_content(
            model=MODEL,
            contents=[summary_prompt, translation.text],
            config=types.GenerateContentConfig(
                max_output_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            ),
        )

        pbar.update(1)
        pbar.set_description("Diagram")
        diagram_prompt = "Given the following text, generate a mermaid diagram summaring the key points in the text. Choose an appropriate type of mermaid diagram. Output only the mermaid diagram without any preamble, postamble or explanations."
        diagram = generate_content(
            model=MODEL,
            contents=[diagram_prompt, translation.text],
            config=types.GenerateContentConfig(
                max_output_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            ),
        )

        pbar.update(1)
        pbar.set_description("Commentary")
        commentary_prompt = "Provide a short commentary on the text, explaining the major points. Adopt the position of a rationalist and explain the concept in non-spiritual terms using phenomenology as a basis. Don't add any preamble or explanation."
        commentary = generate_content(
            model=MODEL,
            contents=[commentary_prompt, translation.text],
            config=types.GenerateContentConfig(
                max_output_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            ),
        )
        pbar.update(1)
        pbar.set_description(filename)

    output = header + title
    output += f"<details>\n<summary>Pali text</summary>\n{pali}</details>\n\n"
    output += f"## Summary\n\n{summary.text}\n\n"
    output += f"## Diagram\n\n{diagram.text}\n\n"
    output += f"## Text\n\n{translation.text}\n\n"
    output += f"## Commentary\n\n{commentary.text}\n\n"
    output += footer

    # fm.content = output
    # output = frontmatter.dumps(fm)

    output_summary(filename, output)

def process_path(path):
    _, file_extension = os.path.splitext(path)
    if (file_extension != ".md"):
        print(f"Skipping unknown file [{path}]")
        return

    base = os.path.splitext(path)[0]
    output = output_file(f"{base}.md", OUTPUT_DIR + '/')
    if os.path.isfile(output):
        print(f"Skipping existing translation and summary file [{output}]")
        return

    with open(path, 'r') as file:
        output_md(path)

def process_dir(folder):
    for foldername, _, filenames in os.walk(folder):
        for filename in filenames:
            path = os.path.join(foldername, filename)
            process_path(path)

def main():
    if len(sys.argv) < 2:
        print(f"Processing `{INPUT_DIR}` directory by default")
        path = INPUT_DIR
        process_dir(path)
    else:
        parser = argparse.ArgumentParser(description="Pali to English translator")
        parser.add_argument("files", nargs="+", help="file or directory ...")
        args = parser.parse_args()

        for path in args.files:
            if os.path.isfile(path):
                process_path(path)
            elif os.path.isdir(path):
                process_dir(path)
            else:
                print(f'The file {path} does not exist')

if __name__ == "__main__":
    main()
