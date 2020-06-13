
# https://stackoverflow.com/questions/39928401/recover-db-password-stored-in-my-dbeaver-connection

# requires pycrypto lib (pip install pycrypto)

import sys
import base64
import os
import json
from Crypto.Cipher import AES

if len(sys.argv) < 2:
  filepath = os.path.expanduser("~/.local/share/DBeaverData/workspace6/General/.dbeaver/credentials-config.json")
else:
  filepath = sys.argv[1]

print(filepath)

PASSWORD_DECRYPTION_KEY = bytes([186, 187, 74, 159, 119, 74, 184, 83, 201, 108, 45, 101, 61, 254, 84, 74])

data = open(filepath, 'rb').read()

decryptor = AES.new(PASSWORD_DECRYPTION_KEY, AES.MODE_CBC, data[:16])

# The '-8' was observed in my case, I'm not sure it will be the same in every case
# Basically this was the string '\x08\x08\x08\x08\x08\x08\x08\x08' in the decrypted output
output = decryptor.decrypt(data[16:])[:-8]

try:
  print(json.dumps(json.loads(output), indent=4, sort_keys=True))
except:
  print(output)
