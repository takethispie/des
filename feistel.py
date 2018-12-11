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


    


    def DoPermutation(self, PMatrix, sbox):
        bits = ""
        for index in PMatrix:
            bits += sbox[index]
        return bits
