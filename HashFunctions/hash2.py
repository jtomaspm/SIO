import hashlib
import sys
import bitarray

def read_file(mfile):
    with open(mfile, "r") as f:
        return f.read()

def write_file(hashed):
    with open("hash.txt", "w") as f:
        f.write(hashed)

def hash_msg(hash_type, msgs):
    m = hashlib.new(hash_type)
    for msg in msgs:
        m.update(msg)
    return m.hexdigest()


def main():
    ba = bitarray.bitarray()
    attempts = int(sys.argv[1])
    inputs = sys.argv[2]
    file = read_file(inputs)
    ba.frombytes(file.encode("utf-8"))
    by = ba
    hash_arr = []
    hash_m = hash_msg("sha256",  [by]) 
    hash_arr.append(hash_m)


    for i in range(len(by)):
        
        if i >= attempts:
            break
        temp = by
        
        if temp[i] == 1:
            temp[i] = 0
        else:
            temp[i] = 1
        hash_m = hash_msg("sha256",  [temp]) 
        hash_arr.append(hash_m)

    original = hash_arr[0]
    compare = hash_arr[1:]

    results = []

    print("original: " + original)
    print()
    print()
    print()
    print()

    for h in compare:
        count = 0
        for i in range(len(original)):
            if not (original[i] == h[i]):
                count  += 1

        results.append(len(original)-count)
        
        print(h, len(original)-count)


    #igualdades
    print("IGUALDADES")
    ig = {}
    for r in results:
        if r not in ig.keys():
            ig[r] = 1
        else:
            ig[r] += 1
    keys = sorted(ig.keys())
    for key in keys:
        print(str(key)+ ": " + "#"*ig[key])

    #diferenças
    print("DIFERENÇAS")
    dif = {}
    for r in results:
        r = len(original)-r
        if r not in dif.keys():
            dif[r] = 1
        else:
            dif[r] += 1
    keys = sorted(dif.keys())
    for key in keys:
        print(str(key)+ ": " + "#"*dif[key])





main()
