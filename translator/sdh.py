import re
import sys
import argparse

def remove_sdh_from_subtitle(input_filename):
    with open(input_filename, "r", encoding="utf-8") as infile:
        for line in infile:
            for exp in [r'\[.*?\]', r'\(.*?\)', r'--(?!>)']:
                line = re.sub(exp, '', line)
            sys.stdout.write(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Remove SDH tags from an SRT subtitle file.')
    parser.add_argument('input_filename', type=str, help='Path to the input .srt file')
    
    args = parser.parse_args()

    remove_sdh_from_subtitle(args.input_filename)
