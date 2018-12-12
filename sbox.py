import textwrap


def SplitTo6Bits(bits):
    return textwrap.wrap(bits, 6)

def FirstAndLastBit(bits6):
    return bits6[0] + bits6[-1]


def MiddleFourBits(bits6):
    return bits6[1:5]


def BinToDec(binarybits):
    return int(binarybits, 2)


def DecToBin(decimal):
    return bin(decimal)[2:].zfill(4)


def lookup(sboxMatrix, firstlast, middle4):
    firstlast = BinToDec(firstlast)
    middle = BinToDec(middle4)
    res = sboxMatrix[firstlast][middle]
    return DecToBin(res)