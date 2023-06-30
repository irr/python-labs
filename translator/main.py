import sys
import boto3
import os
import re

TEST_FILE = "./test.srt"

def translate(text, src="en", dst="pt"):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=src,
        TargetLanguageCode=dst
    )
    return response


def process(file_path, src='en'):

    with open(file_path, 'r') as file:
        content = file.read()
        blocks = content.split('\n\n')

    for block in blocks:
        translated_text = ""
        if block.strip() != "":
            lines = block.split('\n')

            text = '\n'.join([re.sub(r'\[.*?\]|\(.*?\)', '', line) for line in lines[2:]]).strip()

            response = translate(text, src)
            translated_text = response.get("TranslatedText")

            print(lines[0])
            print(lines[1])
            print(translated_text)
            print(flush=True)


def show_help():
    print(f"usage: {sys.argv[0]} <file>\n")


if __name__ == '__main__':
    if len(sys.argv) < 2: 
        if os.path.exists(TEST_FILE): 
            process(TEST_FILE)
        else:
            show_help()
            sys.exit(1)
    else:
        if len(sys.argv) == 3:
            process(sys.argv[1], sys.argv[2])
        else:
            process(sys.argv[1])
