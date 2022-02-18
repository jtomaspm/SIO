import hashlib
import sys

def read_file(mfile):
    with open(mfile, "r") as f:
        return f.read()

def write_file(hashed):
    with open("hash.txt", "w") as f:
        f.write(hashed)

def hash_msg(hash_type, msgs):
    m = hashlib.new(hash_type)
    for msg in msgs:
        m.update(str.encode(msg))
    return m.hexdigest()


def main():
    hash_type = sys.argv[1]
    files = sys.argv[2:]
    msgs = []
    for file in files:
        msgs.append(read_file(file))
    hashed = hash_msg(hash_type, msgs)
    print(hashed)
    write_file(hashed)

main()

