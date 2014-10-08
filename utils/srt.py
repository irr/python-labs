#!/usr/bin/env python

import codecs, commands, sys, re, os

def main():
    try:
        (_, output) = commands.getstatusoutput("file -bi \"%s\"" % (sys.argv[1],))
        _, charset = output.split('charset=')
        with codecs.open(sys.argv[1], 'r', encoding=charset) as source:
            with codecs.open("%s.bak" % (sys.argv[1],), 'w+', encoding='utf8') as target:
                target.write(source.read())
        with codecs.open("%s.bak" % (sys.argv[1],), 'r', encoding='utf8') as source:
            data = source.read()
            data = re.compile(r'<[^>]+>').sub('', data)
            with codecs.open("%s" % (sys.argv[1],), 'w+', encoding='utf8') as target:
                target.write(data)
        os.unlink("%s.bak" % (sys.argv[1],))
        os.system("zenity --info --text='Filename: %s [%s]\nSize: %d'" % 
            (sys.argv[1], charset, os.stat(sys.argv[1]).st_size))
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Usage: srt <file>"
        sys.exit(1)
    main()