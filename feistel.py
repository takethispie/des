import sbox


class feistel:
    def DoExpansion(self, EMatrix, bits):
        bits48 = ""
        for x in EMatrix[0]:
            bits48 += bits[x]
        return bits48

    def XOR(self, bits1, bits2):
        result = ""
        for i in range(len(bits1)):
            if bits1[i] == bits2[i]:
                result += '0'
            else:
                result += '1'
        return result

    # permutation finale apres la round function
    # example : M = 1010  become  M' = 0110
    def DoPermutation(self, PMatrix, sbox):
        bits = ""
        for index in PMatrix[0]:
            bits += sbox[index]
        return bits

    def DoF(self, bits32, key48, EMatrix, PMatrix):
        result = ""
        ELeftHalf = self.DoExpansion(EMatrix, bits32)
        xored = self.XOR(ELeftHalf, key48)
        bits6list = sbox.SplitTo6Bits(xored)
        for sboxcount, bits6 in enumerate(bits6list):
            firstLast = sbox.FirstAndLastBit(bits6)
            middle4 = sbox.MiddleFourBits(bits6)
            sboxvalue = sbox.lookup(sboxcount, firstLast, middle4)
            result += sboxvalue
        final32bits = self.DoPermutation(PMatrix, result)
        return final32bits
