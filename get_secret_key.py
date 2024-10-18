import secrets
secret_key = secrets.token_bytes(24)
print(secret_key)

import os
print(os.urandom(24))

import sys
print(sys.path)

import os
print(os.urandom(24).hex())

