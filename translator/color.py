import re
import sys

def add_font_color_to_subtitles(filename, color="yellow"):
    # Read the contents of the file
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define the pattern for matching subtitle text (excluding timing lines)
    subtitle_pattern = re.compile(r'(\d+\n\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}\n)(.*?)(\n\n|\Z)', re.DOTALL)

    # Function to add font color to the subtitle text
    def add_color(match):
        timing = match.group(1)
        text = match.group(2)
        colored_text = f'<font color="{color}"><b>{text}</b></font>'
        return f'{timing}{colored_text}\n\n'

    # Substitute the original text with the colored text
    new_content = subtitle_pattern.sub(add_color, content)

    # Print the new contents to stdout
    sys.stdout.write(new_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python color.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    add_font_color_to_subtitles(filename)
