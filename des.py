import Extract_ConstantesDES
import ConvAlphaBin
import feistel


class Des:
    def __init__(self):
        self.constDes = Extract_ConstantesDES.recup_constantes_des()
        self.roundSH = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        self.f = feistel.feistel()

    def do_pc1(self, key56):
        mix_key = ""
        i = 1
        for j in self.constDes["CP_1"][0]:
            pos = j - i
            if (pos < 0):
                len(key56) + j
            mix_key += key56[pos]
            i += 1
        return mix_key

    def do_pc2(self, key56):
        mix_key = ""
        i = 1
        for j in self.constDes["CP_2"][0]:
            pos = j - i
            if (pos < 0):
                len(key56) + j
            mix_key += key56[pos]
            i += 1
        return mix_key

    @staticmethod
    def do_inverse_perm(InvPMatrix, roundFunRes):
        cipher = ""
        for x in InvPMatrix[0]:
            cipher += roundFunRes[x]
        return cipher

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
        pc1_out = self.do_pc1(key56)
        key_left, key_right = self.split_half_56bits(pc1_out)
        subkeys = list()
        for roundNum in range(16):
            new_key_left = self.left_shift(key_left, 1)  # self.roundSH[roundNum]
            new_key_right = self.left_shift(key_right, 1)  # self.roundSH[roundNum]
            subkey = self.do_pc2(new_key_left + new_key_right)
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
        blocks = self.split_many_blocks_64bits(bin_message)  # Split du message binaire an plusieurs bloc de 64bits

        # TODO faire une boucle sur chaque blocs afin d'effectuer la permutation de chacun des blocs
        #   (la boucle remplacera le bloc actuel par le bloc permuté)
        permuted_message = self.do_initial_perm(self.constDes["PI"], bin_message)



        left, right = self.split_half_64bits(permuted_message)
        for round in range(16):
            newR = self.f.XOR(left, self.f.DoF(right, round_keys[round], self.constDes["E"], self.constDes["PERM"]))
            newL = right
            right = newR
            left = newL
        cipher = self.do_inverse_perm(self.constDes["PI_I"], right + left)
        return cipher

    def encrypt(self, message, key):
        return self.encrypt_decrypt(message, key)

    def decrypt(self, message, key):
        return self.encrypt_decrypt(message, key)
