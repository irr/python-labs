import os
import sys

# python iptv.py TV-2020-01-21.m3u "BR:"

def process(fname, fexp):
    print("#EXTM3U")
    channels = []
    buffer = None
    with open(fname) as fp:
        for line in fp:
            if line.startswith("#EXTINF"):
                if line.lower().find(fexp.lower()) != -1:
                    buffer = line
            elif buffer is not None:
                channels.append([buffer, line])
                buffer = None
    channels = sorted(channels, key=lambda k: k[0])
    for channel in channels:
        print(channel[0].strip())
        print(channel[1].strip())


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python {} <file> <pattern>".format(os.path.basename(sys.argv[0])))
    else:
        process(sys.argv[1], sys.argv[2])
