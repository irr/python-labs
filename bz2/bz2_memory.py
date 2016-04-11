import bz2
import binascii

text = '''
The titular threat of The Blob has always struck me as the ultimate movie
monster: an insatiably hungry, amoeba-like mass able to penetrate
virtually any safeguard, capable of--as a doomed doctor chillingly
describes it--"assimilating flesh on contact.
Snide comparisons to gelatin be damned, it's a concept with the most
devastating of potential consequences, not unlike the grey goo scenario
proposed by technological theorists fearful of
artificial intelligence run rampant.
'''

original_data = bytes(text, "utf-8")

print("Original     : {} bytes".format(len(original_data)))
print(text)

print()
compressed = bz2.compress(original_data)
print("Compressed   : {} bytes".format(len(compressed)))
hex_version = binascii.hexlify(compressed)
for i in range(len(hex_version) // 40 + 1):
    print(hex_version[i * 40:(i + 1) * 40])

print()
decompressed = bz2.decompress(compressed)
print("Decompressed : {} bytes".format(len(decompressed)))
print(decompressed.decode("utf-8"))
