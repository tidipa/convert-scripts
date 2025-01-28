# kc2eng.py
#
# Pali to English translator and summariser for Kaccayana grammar

import sys
import os
import re
from tqdm import tqdm
from mlx_lm import load, generate
from mlx_lm.models.cache import make_prompt_cache

INPUT_FILE = "kaccayana/docs/source/padarupasiddhi.md"
OUTPUT_DIR="rpeng"
MD_DIR="rp"

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
Step 2. Translate each line of text as accurately as possible. Do not insert any additional text or explanations.
Step 3. Don't include preambles, postambles or explanations.
Step 4. When you have finished translating, output the translation.
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
       
    print (f"Translating {rule.split('\n')[0][4:]}")
    # print (f"Translating {rule}")

    translation = generate(model, tokenizer, prompt=prompt, max_tokens=MAX_TOKENS, max_kv_size=MAX_KV_SIZE, verbose=False)

    for line in translation.split("\n"):
        if line.find("## Translation") == -1:
            output.write(line + "\n")

    output.write("\n")
        
    # output.write(translation + "\n")
    
def process_md(filename):
    inrule = False
    rule = ""
    with open(os.path.join(MD_DIR, filename), 'r') as input, open(os.path.join(OUTPUT_DIR, filename), 'w') as output:
        for line in input:
            if line.strip() == "":
                if inrule:
                    rule += line
                output.write(line)
            elif line.startswith("---") and inrule:
                translate(output, rule)
                output.write(line)
            elif line.startswith("<a ") and inrule:
                output.write(line)
            elif line.startswith("### "):
                if not inrule:
                    inrule = True
                rule = line
                output.write(line)
            elif inrule:
                rule += line
                output.write("> " + line)
            else:
                output.write(line)
    print(f'Translated {filename}\n')

def process_file(input_path):
    with open(input_path, 'r') as file:
        output_path = os.path.join(MD_DIR, os.path.basename(input_path))
        output = open(output_path, 'w')
        # read file line by line
        for line in file:
            # open new output file
            if line.startswith("## "):
                if output:
                    output.close()
                output_path = os.path.join(MD_DIR, slugify(line[3:]) + ".md")
                output = open(output_path, 'w')
                print(f"Writing to {output_path}")

            # detect rule number and title
            rule = re.match(r'^(\d+)\. \[\{ref\}`(\d+)\*?<(m\d+)>`\] ([^.]+)\.$', line)
            anchor = re.match(r'^\(([^)]+)\)=$', line)
            subsection = re.match(r'^__([^_]+)__$', line)
            if anchor:
                name = anchor.group(1)
                # print(f"Anchor: {name}")
                output.write(f'<a name="{name}"></a>\n')
            elif subsection:
                output.write(f'### {subsection.group(1)}\n')
            elif rule:
                rule_number = rule.group(1)
                ref = rule.group(2)
                # subref = rule.group(3)
                rule_title = rule.group(4)
                output.write(f'### {rule_number} ({ref}): {rule_title}\n')
            else:
                output.write(line)

if __name__ == "__main__":
    os.makedirs(MD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # write out Chapters to MD_DIR
    process_file(INPUT_FILE)

    # process each file in MD_DIR
    for filename in os.listdir(MD_DIR):
        process_md(filename)
