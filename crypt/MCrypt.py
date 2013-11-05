# -*- coding: utf-8 -*-

from Crypto.Cipher import AES

BLOCK_SIZE = 16
PADDING    = " "
pad        = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

obj        = AES.new('ba0113f5b71eb5ce', AES.MODE_CBC, IV = "ba14f4a4d7ecddbf")
plain      = "mysql"
padded     = pad("mysql")
ciph       = obj.encrypt(padded)
encrypted  = ''.join('%02x' % ord(byte) for byte in ciph)

obj        = AES.new('ba0113f5b71eb5ce', AES.MODE_CBC, IV = "ba14f4a4d7ecddbf")
decrypted  = obj.decrypt(encrypted.decode("hex")).strip()

print "Plaintext=[%s]" % plain
print "Encrypted=[%s]" % encrypted
print "Decrypted=[%s]" % decrypted
