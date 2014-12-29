#!/usr/bin/env python

import argparse
import sys
import socket

import vigenere
import aes
import lsb

PORT = 42424


def client(data, keyVigenere, keyAES, picture, host):
    data_vig = vigenere.vigenere(data, keyVigenere, True)
    data_aes = aes.aesString(data_vig, keyAES, 'c')
    picname = lsb.lsb_in(picture, data_aes)
    if not picname:
        return False
    pic = open(picname, 'rb')
    pic_data = pic.read()

    sock = socket.socket()
    sock.connect((host, PORT))
    sock.send(pic_data)
    sock.close()
    return True


def recieve_data():
    sock = socket.socket()
    sock.bind(('', PORT))

    sock.listen(100)
    conn, addr = sock.accept()
    conn.settimeout(10)
    res = ""
    while True:
        data = conn.recv(1000000)
        if not data:
            break
        res += data
    conn.close()
    
    return res


def server(keyVigenere, keyAES):
    picture = recieve_data()
    imgfile = open("tmp.bmp", 'wb')
    imgfile.write(picture)
    imgfile.close()

    coded_aes = lsb.lsb_out("tmp.bmp")
    coded_vig = aes.aesString(coded_aes, keyAES, 'd')
    data = vigenere.vigenere(coded_vig, keyVigenere, False)
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('key_vigenere')
    parser.add_argument('key_aes')
    parser.add_argument('-p', '--picture', nargs='?', help="Required if CLIENT")
    parser.add_argument('-i', '--input_data', nargs='?', help="Required if CLIENT")
    parser.add_argument('-a', '--address', nargs='?', help="Required if CLIENT")
    parser.add_argument('-o', '--output_data', nargs='?', help="Required if SERVER")
    args = parser.parse_args()

    keyVigenerefile = open(args.key_vigenere, 'rb')
    keyVigenere = keyVigenerefile.read()
    keyVigenerefile.close()

    keyAESfile = open(args.key_aes, 'rb')
    keyAES = keyAESfile.read()
    keyAESfile.close()

    if args.input_data and args.address:
        infile = open(args.input_data, 'rb')
        data = infile.read()
        infile.close()
        if not client(data, keyVigenere, keyAES, args.picture, args.address):
            print "Can't send data"
        
    elif args.output_data:
        recieved_data = server(keyVigenere, keyAES)
        if not recieved_data:
            print "Can't recieve data"
        else:
            outfile = open(args.output_data, 'wb')
            outfile.write(recieved_data)
            outfile.close()

    else:
        print "Specify picture, input_data and address for CLIENT"
        print "Specify output_data for SERVER"
