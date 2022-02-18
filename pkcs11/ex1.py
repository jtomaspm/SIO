#!/usr/bin/bash

import pkcs11
import binascii

lib = '/usr/lib/libpteidpkcs11.so'
pkcs11 = pkcs11.lib(lib)
pkcs11.load(lib)
slots = pkcs11.getSlotList()

for slot in slots:
    print(pkcs11.getTokenInfo(slot))
