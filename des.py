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
        key48 = ""
        for j in self.constDes["CP_2"][0]:
            key48 += key56[j]
        return key48

    @staticmethod
    def split_in_two(key56):
        left, right = key56[:28], key56[:28]
        return left, right

    @staticmethod
    def BarrelLShift(bits, numBits):
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
        key_left, key_right = self.split_in_two(pc1_out)
        subkeys = list()
        for roundNum in range(16):
            newLeft = self.BarrelLShift(key_left, self.roundSH[roundNum])
            newRight = self.BarrelLShift(key_right, self.roundSH[roundNum])
            subkey = self.do_pc2(newLeft + newRight)
            subkeys.append(subkey)
            key_left = newLeft
            key_right = newRight
        return subkeys

    @staticmethod
    def DoInitialPerm(IPMatrix, text):
        permutated = ""
        for x in IPMatrix[0]:
            permutated += text[x]
        return permutated

    @staticmethod
    def splitHalf(binarybits):
        return binarybits[:32], binarybits[32:]

    @staticmethod
    def DoInversePerm(InvPMatrix, roundFunRes):
        cipher = ""
        for x in InvPMatrix[0]:
            cipher += roundFunRes[x]
        return cipher

    def encrypt_decrypt(self, message, key):
        binTxt = ConvAlphaBin.conv_bin(message)
        clearKey = ConvAlphaBin.nib_vnoc(key)
        print("encrypt_decrypt =>", key)
        print("encrypt_decrypt =>", clearKey)
        roundkeys = self.gen_sub_keys(key)
        permutedTxt = self.DoInitialPerm(self.constDes["PI"], binTxt)
        left, right = self.splitHalf(permutedTxt)
        for round in range(16):
            newR = self.f.XOR(left, self.f.DoF(right, roundkeys[round], self.constDes["E"], self.constDes["PERM"]))
            newL = right
            right = newR
            left = newL
        cipher = self.DoInversePerm(self.constDes["PI_I"], right + left)
        return cipher

    def encrypt(self, message, key):
        return self.encrypt_decrypt(message, key)

    def decrypt(self, message, key):
        return self.encrypt_decrypt(message, key)
