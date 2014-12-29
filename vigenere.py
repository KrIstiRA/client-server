#!/usr/bin/env python

import argparse

def vigenere(data, key, encode):
    encoded = str()
    for i in range(len(data)):
        a = ord(data[i])
        b = ord(key[i % len(key)])
        if encode:
            c = (a + b) % 256
        else:
            c = (a - b + 256) % 256
        encoded += chr(c)
    return encoded

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('key')
    parser.add_argument('mode', choices=['c', 'd'])
    args = parser.parse_args()

    infile = open(args.input, 'rb')
    data = infile.read()
    infile.close()

    keyfile = open(args.key, 'rb')
    key = keyfile.read()
    keyfile.close()

    outfile = open(args.output, 'wb')
    mode = (args.mode == 'c')
    encoded = vigenere(data, key, mode)
    outfile.write(encoded)
    outfile.close()
