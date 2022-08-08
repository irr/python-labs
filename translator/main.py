import sys
import boto3
import os

TEST_FILE = "./test.srt"

def translate(text, src="en", dst="pt"):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=src,
        TargetLanguageCode=dst
    )
    return response


def process(file):
    f = open(file, "rt")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            translated_text = ""
        else:
            if len(line) > 0 and not line.isnumeric() and line.find(" --> ") == -1:
                response = translate(line)
                translated_text = response.get("TranslatedText")
            else:
                translated_text = line
        print(translated_text, flush=True)


def show_help():
    print(f"usage: {sys.argv[0]} <file>\n")


if __name__ == '__main__':
    if len(sys.argv) != 2: 
        if os.path.exists(TEST_FILE): 
            process(TEST_FILE)
        else:
            show_help()
            sys.exit(1)
    else:
        process(sys.argv[1])
