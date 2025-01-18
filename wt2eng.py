# wt2eng.py
#
# Pali to English translator and summariser for markdown files
# Takes filenames or directories as command line arguments
# (by default all files in "_markdown" directory)
# Then summarise each file into "eng/file-summ.md"
# as Markdown with headings retained where appropriate and bullet points in content.
# Accepted file extensions: .md, .txt

import sys
import os
import argparse
from tqdm import tqdm
from mlx_lm import load, generate
import frontmatter

repo = "mlx-community/Llama-3.3-70B-Instruct-8bit"
model, tokenizer = load(repo)

OUTPUT_DIR="eng"
MAX_TOKENS = 65536
MAX_KV_SIZE = 4096
NUM_CTX=8192
TEMPERATURE=0.3


system_prompt = """
You are an efficient and accurate Pali to English translator.

## Instructions

Step 1. Read the entire text.
Step 2. Extract headings which begin with #.
Step 3. Include each heading in the output.
Step 4. Translate each line of text word by word as accurately as possible. Do not insert any additional text or explanations.
Step 5. Don't include preambles, postambles or explanations.
Step 6. When you have finished translating, output the translation following the format of the input text as closely as possible with '# Translation' as the heading.
Step 7. After translating, provide a one paragraph summary of the translation with '# Summary' as the heading.
"""

def output_file(s, prefix):
    input_prefix = "_markdown/"

    # Strip _input/ prefix if it exists
    if s.startswith(input_prefix):
        s = s[len(input_prefix):]

    # Add _output/ prefix
    s = prefix + s

    return s

def output_summary(filename: str, summary: str):
    base = os.path.splitext(filename)[0]
    
    summary_file = output_file(f"{base}.md", OUTPUT_DIR + '/')
    original = output_file(filename, "")
    os.makedirs(os.path.dirname(summary_file), exist_ok=True)
    with open(summary_file, 'w') as file:
        file.write(summary)
    print(f'Converted to English plus summary [{summary_file}]\n')
    
def output_md(filename, markdown):
    fm = frontmatter.loads(markdown)

    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': "## text\n" + fm.content}
    ]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True
    )

    translation = generate(model, tokenizer, prompt=prompt, max_tokens=MAX_TOKENS, max_kv_size=MAX_KV_SIZE, verbose=False)

    fm.content = translation
    output = frontmatter.dumps(fm)

    output_summary(filename, output)
    
def process_path(path):
    _, file_extension = os.path.splitext(path)
    if (file_extension == ".md" or file_extension == ".txt"):
        print(f"Processing file: [{path}]")
    else:
        print(f"Skipping unknown file [{path}]")
        return
    
    base = os.path.splitext(path)[0]
    output = output_file(f"{base}.md", OUTPUT_DIR + '/')
    if os.path.isfile(output):
        print(f"Skipping existing translation and summary file [{output}]")
        return       

    with open(path, 'r') as file:
        output_md(path, file.read())

def process_dir(folder):
    for foldername, _, filenames in os.walk(folder):
        for filename in filenames:
            path = os.path.join(foldername, filename)
            process_path(path)            
            
def main():
    if len(sys.argv) < 2:
        print("Processing _markdown directory by default")
        path = "_markdown"
        process_dir(path)
    else:
        parser = argparse.ArgumentParser(description="summarise.py [file|dir] ...")
        parser.add_argument("path", nargs="+", help="Path to a file or directory")
        args = parser.parse_args()

        for path in args.path:
            if os.path.isfile(path):
                process_path(path)
            elif os.path.isdir(path):
                process_dir(path)
            else:
                print(f'The file {path} does not exist')

if __name__ == "__main__":
    main()
