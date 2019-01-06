import textwrap


class Feistel:
    @staticmethod
    def FirstAndLastBit(bits6):
        return bits6[0] + bits6[-1]

    @staticmethod
    def MiddleFourBits(bits6):
        return bits6[1:5]

    @staticmethod
    def conv_bin_to_decimal(binarybits):
        return int(binarybits, 2)

    @staticmethod
    def conv_decimal_to_bin(decimal):
        return bin(decimal)[2:].zfill(4)

    @staticmethod
    def xor(bits1, bits2):
        result = ""
        for i in range(0, len(bits1)):
            if bits1[i] == bits2[i]:
                result += '0'
            else:
                result += '1'
        return result

    @staticmethod
    def do_permutation_key(matrix, key):
        mix_key = ""
        for j in matrix[0]:
            mix_key += key[j]
        return mix_key

    @staticmethod
    def split_half_56bits(key56):
        left, right = key56[:28], key56[:28]
        return left, right

    @staticmethod
    def split_half_64bits(key64):
        left, right = key64[:32], key64[:32]
        return left, right

    @staticmethod
    def split_many_blocks_64bits(key):  # En remplissant les derniers bits par des "0"
        blocks = textwrap.wrap(key, 64)
        str_temp = blocks[len(blocks) - 1]
        while len(str_temp) < 64:
            str_temp += "0"
        blocks[len(blocks) - 1] = str_temp
        return blocks

    @staticmethod
    def split_many_blocks_6bits(bits):
        return textwrap.wrap(bits, 6)

    @staticmethod
    def left_shift(bits, num_bits):
        return bits[num_bits:] + bits[:num_bits]

    def do_feistel(self, key32_left, key48_round, expansion_matrix, permutation_round_matrix):
        result = ""
        key48_left = self.do_permutation_key(expansion_matrix, key32_left)  # 1
        xored = self.xor(key48_left, key48_round)  # 2
        bits6list = self.split_many_blocks_6bits(xored)  # 3 et comme xored fait 48 bits ça fera automatiquement la séparation en 8 blocs de 6 bits
        for sboxcount, bits6 in enumerate(bits6list):
            first_last = self.FirstAndLastBit(bits6)
            middle4 = self.MiddleFourBits(bits6)
            sboxvalue = self.lookup(sboxcount, first_last, middle4)
            result += sboxvalue
        final32bits = self.do_permutation_key(permutation_round_matrix, result)
        return final32bits

    def lookup(self, sboxMatrix, firstlast, middle4):
        first_last = self.conv_bin_to_decimal(firstlast)
        middle = self.conv_bin_to_decimal(middle4)
        result = sboxMatrix[first_last][middle]
        return self.conv_decimal_to_bin(result)
