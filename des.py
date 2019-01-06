import Extract_ConstantesDES
import ConvAlphaBin
import feistel


class Des:
    def __init__(self):
        self.const_des = Extract_ConstantesDES.recup_constantes_des()
        self.roundSH = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        self.feistel = feistel.feistel()

    @staticmethod
    def do_perm_key_matrix(inv_matrix, key):
        mix_key = ""
        i = 1
        for j in inv_matrix[0]:
            pos = j - i
            if (pos < 0):
                len(key) + j
            mix_key += key[pos]
            i += 1
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
    def split_many_blocks_64bits(key):
        blocks = list()
        str_temp = ""
        i = 0
        for j in key:
            str_temp += j
            if (i % 64 == 63):
                while (len(str_temp) < 64):
                    str_temp += "0"
                blocks.append(str_temp)
                str_temp = ""
            i += 1
        return blocks

    @staticmethod
    def left_shift(bits, numBits):
        SHBits = bits[numBits:] + bits[:numBits]
        return SHBits

    @staticmethod
    def delete_control_bits(key64):  # Delete 8 bits of control
        key56 = ""
        i = 0
        for j in key64:
            if (i % 8 < 7):
                key56 += j
            i += 1
        return key56

    def gen_sub_keys(self, key64):
        key56 = self.delete_control_bits(key64)
        pc1_out = self.do_perm_key_matrix(self.const_des["CP_1"], key56)  # Permutation CP1
        key_left, key_right = self.split_half_56bits(pc1_out)
        subkeys = list()
        for roundNum in range(16):
            new_key_left = self.left_shift(key_left, 1)
            new_key_right = self.left_shift(key_right, 1)
            subkey = self.do_perm_key_matrix(self.const_des["CP_2"], new_key_left + new_key_right)  # Permutation CP2
            subkeys.append(subkey)
            key_left = new_key_left
            key_right = new_key_right
        return subkeys

    @staticmethod
    def do_initial_perm(IPMatrix, text):
        permutated = ""
        for x in IPMatrix[0]:
            permutated += text[x]
        return permutated

    @staticmethod
    def split_half(binarybits):
        return binarybits[:32], binarybits[32:]

    def encrypt_decrypt(self, message, key):
        # clear_key = ConvAlphaBin.nib_vnoc(key)
        round_keys = self.gen_sub_keys(key)  # Génération des sous clefs

        bin_message = ConvAlphaBin.conv_bin(message)  # Conversion du message en binaire
        blocks = self.split_many_blocks_64bits(bin_message)  # Split du message binaire en plusieurs blocs de 64bits

        pi_left = list()
        pi_right = list()

        for i in range(0, len(blocks) - 1):
            blocks[i] = self.do_perm_key_matrix(self.const_des["PI"], blocks[i])  # Permutation PI
            left, right = self.split_half_64bits(blocks[i])
            pi_left.append(left)
            pi_right.append(right)

        result = list()
        for i in range(0, len(pi_left) - 1):  # Ou pi_left, ça revient au même
            left = pi_left[i]
            right = pi_right[i]
            cipher = ""
            for j in range(16):
                temp_right = self.feistel.XOR(left, self.feistel.DoF(right, round_keys[j], self.const_des["E"], self.const_des["PERM"]))  # Fix un bug qui est dans cette ligne
                temp_left = right
                right = temp_right
                left = temp_left
                cipher = self.do_perm_key_matrix(self.const_des["PI_I"], temp_right + temp_left)
            result.append(cipher)

        return result

    def encrypt(self, message, key):
        return self.encrypt_decrypt(message, key)

    def decrypt(self, message, key):
        return self.encrypt_decrypt(message, key)
