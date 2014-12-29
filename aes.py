#!/usr/bin/env python
# coding: UTF-8

import argparse

Nk = 4
Nb = 4
Nr = 10

def KeyExpansion(key):
    Rcon = [
        [0x00, 0x00, 0x00, 0x00],
        [0x01, 0x00, 0x00, 0x00],
        [0x02, 0x00, 0x00, 0x00],
        [0x04, 0x00, 0x00, 0x00],
        [0x08, 0x00, 0x00, 0x00],
        [0x10, 0x00, 0x00, 0x00],
        [0x20, 0x00, 0x00, 0x00],
        [0x40, 0x00, 0x00, 0x00],
        [0x80, 0x00, 0x00, 0x00],
        [0x1b, 0x00, 0x00, 0x00],
        [0x36, 0x00, 0x00, 0x00]]

    w = [[0] * 4] * (Nb * (Nr + 1))

    i = 0
    while i < Nk:
        for j in range(4):
            w[i][j] = key[4 * i + j]
        i += 1

    while i < Nb * (Nr + 1):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = SubWord(RotWord(temp))
            for j in range(4):
                temp[j] ^= Rcon[i / Nk][j]
                
        for j in range(4):
            w[i][j] = temp[j] ^ w[i - Nk][j]
        i += 1
    return w


def SubByte(byte):
    Sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
            0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
            0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
            0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
            0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
            0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
            0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
            0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
            0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
            0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
            0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
            0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
            0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
            0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
            0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    return Sbox[byte]


def InvSubByte(byte):
    Sbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
           0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
           0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
           0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
           0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
           0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
           0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
           0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
           0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
           0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
           0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
           0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
           0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
           0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
           0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
           0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
    return Sbox[byte]


def SubBytes(state):
    for i in range(4):
        for j in range(Nb):
            state[i][j] = SubByte(state[i][j])
    return state


def InvSubBytes(state):
    for i in range(4):
        for j in range(Nb):
            state[i][j] = InvSubByte(state[i][j])
    return state


def RotWord(word):
    return word[1:] + word[:1]


def SubWord(word):
    result = [0] * 4
    for i in range(4):
        result[i] = SubByte(word[i])
    return result


def AddRoundKey(state, roundKey):
    for i in range(4):
        for j in range(Nb):
            state[i][j] ^= roundKey[i][j]
    return state

def ShiftRows(state):
    for i in range(4):
        state[i] = state[i][i:] + state[i][:i]
    return state


def InvShiftRows(state):
    for i in range(4):
        state[i] = state[i][-i:] + state[i][:-i]
    return state


def gmul(a, b):
    p = 0
    for counter in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        a &= 0xff
        if hi_bit_set:
            a ^= 0x1b
        b >>= 1
    return p


def MixColumnsStep(line, x1, x2, x3, x4):
    return gmul(line[0], x1) ^ gmul(line[1], x2) ^ gmul(line[2], x3) ^ gmul(line[3], x4)


def MixColumns(state):
    for i in range(Nb):
        b = [0] * 4
        b[0] = MixColumnsStep(state[i], 2, 3, 1, 1)
        b[1] = MixColumnsStep(state[i], 1, 2, 3, 1)
        b[2] = MixColumnsStep(state[i], 1, 1, 2, 3)
        b[3] = MixColumnsStep(state[i], 3, 1, 1, 2)
        state[i] = list(b)
    return state


def InvMixColumns(state):
    for i in range(Nb):
        b = [0] * 4
        b[0] = MixColumnsStep(state[i], 14, 11, 13, 9)
        b[1] = MixColumnsStep(state[i], 9, 14, 11, 13)
        b[2] = MixColumnsStep(state[i], 13, 9, 14, 11)
        b[3] = MixColumnsStep(state[i], 11, 13, 9, 14)
        state[i] = list(b)
        
    return state


def Cipher(in_, w):
    state = [0] * 4
    for i in range(4):
        state[i] = in_[i::Nb]
    state = AddRoundKey(state, w[0:Nb])
    for round in range(1, Nr):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, w[round*Nb:Nb * (round + 1)])

    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, w[Nr*Nb:(Nr + 1) * Nb])

    out = [0] * (Nb * 4)
    for i in range(Nb):
        for j in range(4):
            out[i * Nb + j] = state[j][i]
    return out


def InvCipher(in_, w):
    state = [0] * 4
    for i in range(4):
        state[i] = in_[i::Nb]
        
    state = AddRoundKey(state, w[Nr * Nb:(Nr + 1) * Nb])
    for round in range(Nr - 1, 0, -1):
        state = InvShiftRows(state)
        state = InvSubBytes(state)
        state = AddRoundKey(state, w[Nb * round:Nb * (round + 1)])
        state = InvMixColumns(state)

    state = InvShiftRows(state)
    state = InvSubBytes(state)
    state = AddRoundKey(state, w[0: Nb])

    out = [0] * (Nb * 4)
    for i in range(Nb):
        for j in range(4):
            out[i * Nb + j] = state[j][i]
    return out


# шифрует или дешифрует блок данных (байт, чисел), кратный 16
def aes(data, key, encryption):
    if len(key) != 16 or len(data) % 16 != 0:
        return None
        
    w = KeyExpansion(key)

    result = []
    for i in range(0, len(data), 16):
        if encryption:
            coded = Cipher(data[i:i + 16], w)
        else:
            coded = InvCipher(data[i:i + 16], w)
        result += coded

    return result


# шифрует или дешифрует строки
def aesString(data, key, mode):
    if len(key) != 16:
        raise Exception("Bad key size")
        
    # переведём символы в числа
    data = [ord(x) for x in data]
    key = [ord(x) for x in key]

    encryption = (mode == 'c')
    if encryption:
        # перед шифрованием - выравнивание длины
        lastLen = len(data) % 16
        nZeroes = 16 - lastLen - 1
        data = [nZeroes] + data + [0] * nZeroes

    result = aes(data, key, encryption)

    if not encryption:
        # при дешифровании необходимо избавиться от фиктивных нулей в конце
        nZeroes = result[0]
        if nZeroes != 0:
            result = result[1:-nZeroes]
        else:
            result = result[1:]

    # переводим числа обратно в символы
    result = [chr(x) for x in result]
    return ''.join(result) # возвращаем в виде строки


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

    encoded = aesString(data, key, args.mode)

    outfile = open(args.output, 'wb')
    outfile.write(encoded)
    outfile.close()