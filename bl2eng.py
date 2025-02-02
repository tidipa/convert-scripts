# kc2eng.py
#
# Pali to English translator and summariser for Kaccayana grammar

import csv
import os
from pydoc import text
import re
from tqdm import tqdm
from mlx_lm import load, generate
from mlx_lm.models.cache import make_prompt_cache

INPUT_FILE = "gretilcsv/balavataro.csv"
OUTPUT_DIR="balavataro-eng"
MD_DIR="balavataro"

repo = "mlx-community/Llama-3.3-70B-Instruct-4bit"
model, tokenizer = load(repo)

# Make the initial prompt cache for the model
prompt_cache = make_prompt_cache(model)

MAX_TOKENS = 65536
MAX_KV_SIZE = 4096

system_prompt = """
You are an efficient and accurate Pali to English translator.

## Instructions

Step 1. Read the entire text. This is a Pali grammar rule from the Kaccayana grammar.
Step 2. Translate word by word in each line.
Step 3. Using each word, translate each line of text as accurately as possible in natural Engish considering the overall context of the text.
Step 4. Do not insert any additional text or explanations.
Step 5. When you have finished translating, output the translation.
Step 6. Don't include preambles, postambles or explanations.
"""

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)

    
def translate(output, rule):
    messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': "## text\n" + rule}
    ]
    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True
    )

    translation = generate(model, tokenizer, prompt=prompt, max_tokens=MAX_TOKENS, max_kv_size=MAX_KV_SIZE, verbose=False)

    for line in translation.split("\n"):
        if line.find("## Translation") == -1:
            output.write(line + "\n")

    output.write("\n")
        
    # output.write(translation + "\n")
    
def process_md(filename):
    rule = ""
    print(f'Translating {filename}\n')
    with open(os.path.join(MD_DIR, filename), 'r') as input, open(os.path.join(OUTPUT_DIR, filename), 'w') as output:
        for line in input:
            rule += line
            if line.strip() == "":
                output.write(line)
            elif line.startswith("#"):
                output.write(line)
            else:
                output.write("> " + line)
        translate(output, rule)

def process_file(input_path):
    with open(input_path, 'r', newline='') as file:
        rows = csv.reader(file)
        section = ""
        output = None
        for i, row in enumerate(rows):
            if i <= 1:
                continue
            if (section != row[1]):
                section = row[1]
                output_path = os.path.join(MD_DIR, section + ".md")
                print(f"Writing {output_path}")
                if output:
                    output.close()
                output = open(output_path, 'w')
                output.write(f'# {section}\n')
            
            markup = row[3]
            text = row[4]

            if markup == "text":
                output.write(f'{text}\n')
            elif markup == "break":
                output.write('\n')
            elif markup == "endsection":
                output.write(f'---\n\n({text})\n')
        return

if __name__ == "__main__":
    os.makedirs(MD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # write out Chapters to MD_DIR
    process_file(INPUT_FILE)

    # process each file in MD_DIR
    for filename in os.listdir(MD_DIR):
        process_md(filename)
