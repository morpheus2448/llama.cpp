#  Tested with GPT4All-13B-snoozy.ggml, Wizard-Vicuna-13B-Uncensored.ggml, WizardLM-7B-uncensored.ggml. Other models may not follow the prompt and formatting well.

#  Usage:
#  The script is intended to be used in interactive mode (-i), but you can let it run without.
#  If you omit the query (-q) in interactive mode, you get to type it in. In non-interactive mode, a query will be generated for you!

#  Prompt caching is default so add (-nc) if you don't want tmp files stored in your models folder.

#  Ex: python unity.py -m WizardLM-7B-uncensored.ggml.q8_0.bin -q "Search for Sephiroth" -nc -i
#  Ex: python unity.py -q "I'm searching for information on the great spot on Jupiter."

#  Notes: Remember to look at the parameters below and modify to suit your needs.
#  This script uses the argparse library. You'll need it (pip install argparse).

model_dir = "/home/morpheus/llama.cpp/models/"
default_model = "Wizard-Vicuna-13B-Uncensored.ggml.q8_0.bin"
threads = "4" # Don't forget to set your threads appropriately
temperature = "0.1" # temperature (default: 0.1)

import subprocess
import sys
import time
import os
import argparse

parser = argparse.ArgumentParser(description='Digital Akasha Explorer Agent Module.')
parser.add_argument('-q', '--query', help='Initial query for Unity')
parser.add_argument('-m', '--model', help='Specify custom model file')
parser.add_argument('-i', '--interactive', action='store_true', help='Interactive mode')
parser.add_argument('-nc', '--nocache', action='store_true', help="Don't store prompt cache")
args = parser.parse_args()

def main():

    if args.model:
        session_file = args.model
        model_file = model_dir + args.model
    else:
        session_file = default_model
        model_file = model_dir + session_file

    gen_options = [
        "--threads", threads,
        "--temp", temperature,
        "--mirostat", "1", # I use mirostat for this script.
        "--batch_size", "140", # Batch size for prompt processing. Calculate with [https://huggingface.co/spaces/Xanthius/llama-token-counter] (default: 512)
        "--ctx_size", "2048", # Size of the prompt context (default: 512)
        "--repeat_last_n", "-1", # (default: 1.1, 1.0 = disabled)
        "--repeat_penalty", "1.3", # (default is 1.1)
        "--top_p", "1", # top-p sampling (default: 0.9, 1.0 = disabled)
        "--n_predict", "-1",
        "--no-penalize-nl",
        "--model", model_file,
        ]

    if args.interactive:
        gen_options = gen_options + ["--interactive", "--color", "--keep", "160", "--reverse-prompt", "### [USER]\n"]
        if not args.query:
            gen_options = gen_options + ["--interactive-first"]
    
    if not args.nocache:
        session_file = model_dir + session_file + ".tmp"
        gen_options = gen_options + ["--prompt-cache", session_file]

    # Store the start time
    start_time = time.time()

    prompt = f"""
### [UNITY]
Welcome User. I am Unity, your interface to the Digital Akasha Corporation's Universal Entity Registry: A vast repository of data, spanning galaxies. I am at your disposal for information retrieval, and direct communication purposes with any entity. You have been granted full clearance for collaboration with one or more entities in the database to further your research and education. Please refer to your UER starter guide, or type 'help' for ways you can interact with me, or 'ideas' for some recommended entities.

### [USER]
"""

    if args.query:
        prompt = prompt + args.query + ".\n"

    main_command = ["../main"] + gen_options + [
        "--prompt", prompt,
    ]

    subprocess.run(main_command)
 
    # Store the end time
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time

    # Print the elapsed time
    print("The elapsed time is", elapsed_time)

if __name__ == "__main__":
    main()
