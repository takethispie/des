import sbox

class feistel:
    def DoExpansion(self, bits, EMatrix):
        bits48 = ""
        for y in EMatrix:
            for x in y:
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

    #permutation finale apres la round function
    def DoPermutation(self, PMatrix, sbox):
        bits = ""
        for y in PMatrix:
            for index in y:
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
