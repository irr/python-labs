#!/home/irocha/dev/bin/python

import codecs, subprocess, sys, re, os

def main():
    try:
        output = subprocess.check_output(["file", "-bi", sys.argv[1]])
        charset = output.decode('ascii').split('charset=')[1].strip()
        with codecs.open(sys.argv[1], 'r', encoding=charset) as source:
            with codecs.open("%s.bak" % (sys.argv[1],), 'w+', encoding='utf8') as target:
                target.write(source.read())
        with codecs.open("%s.bak" % (sys.argv[1],), 'r', encoding='utf8') as source:
            data = source.read()
            data = re.compile(r'<[^>]+>').sub('', data)
            with codecs.open(sys.argv[1], 'w+', encoding='utf8') as target:
                target.write(data)
        os.unlink("%s.bak" % (sys.argv[1],))
        os.system("zenity --info --text='Filename: %s\nEncoding: [%s]\nSize: %d'" % 
            (sys.argv[1], charset, os.stat(sys.argv[1]).st_size))
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Usage: srt <file>")
        sys.exit(1)
    main()
