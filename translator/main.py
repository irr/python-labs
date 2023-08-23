import sys
import boto3
import os

TEST_FILE = "./test.srt"

WINDOW = 50

def translate(text, src="en", dst="pt"):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=src,
        TargetLanguageCode=dst
    )
    return response


def process(file_path, src='en'):
    with open(file_path, encoding='utf-8-sig') as file:
        content = file.readlines()
    try:
        while len(content) > 0:
            chunk = []
            while len(content) > 0:
                line = content.pop(0)
                chunk.append(line)
                if line.strip().isnumeric():
                    if len(chunk) > WINDOW:
                        content.insert(0, line)
                        chunk.pop()
                        break
            text = ''.join(chunk)
            response = translate(text, src)
            translated_text = f"{response.get('TranslatedText')}"
            print(translated_text.strip())
            print(flush=True)
    except Exception as ex:
        print(ex)


def show_help():
    print(f"usage: {sys.argv[0]} <file>\n")


if __name__ == '__main__':
    if len(sys.argv) < 2: 
        if os.path.exists(TEST_FILE): 
            process(TEST_FILE, "es")
        else:
            show_help()
            sys.exit(1)
    else:
        if len(sys.argv) == 3:
            process(sys.argv[1], sys.argv[2])
        else:
            process(sys.argv[1])
