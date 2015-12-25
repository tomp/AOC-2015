#!/usr/bin/env python

import hashlib

key = 'bgvyzdsv'
# key = 'abcdef'
# key = 'pqrstuv'
print "key:", key

coin = 0
while not hashlib.md5(key+str(coin)).hexdigest().startswith('000000'):
    coin += 1

print "coin:", coin


