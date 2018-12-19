import Extract_ConstantesDES
import ConvAlphaBin
import feistel

class Des:
    def __init__(self):
        self.constDes = Extract_ConstantesDES.recupConstantesDES()
        self.roundSH = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        self.f = feistel.feistel()

    def DoPC1(self, key64):
        key56 = ""
        for j in self.constDes["CP_1"][0]:
            key56 += key64[j]
        return key56

    def SplitInTwo(self, key56):
        left, right = key56[:28], key56[:28]
        return left, right

    def BarrelLShift(self, bits, numBits):
        SHBits = bits[numBits:] + bits[:numBits]
        return SHBits

    def DoPC2(self, key56):
        key48 = ""
        for j in self.constDes["CP_2"][0]:
            key48 += key56[j]
        return key48

    def genSubkeys(self, key64):
        subkeys = list()
        pc1out = self.DoPC1(key64)
        left, right = self.SplitInTwo(pc1out)
        for roundNum in range(16):
            newLeft = self.BarrelLShift(left, self.roundSH[roundNum])
            newRight = self.BarrelLShift(right, self.roundSH[roundNum])
            subkey = self.DoPC2(newLeft+newRight)
            subkeys.append(subkey)
            left = newLeft
            right = newRight
        return subkeys


    def DoInitialPerm(self, IPMatrix, text):
        permutated = ""
        for x in IPMatrix[0]:
            permutated += text[x]
        return permutated


    def splitHalf(self, binarybits):
        return binarybits[:32], binarybits[32:]


    def DoInversePerm(self, InvPMatrix, roundFunRes):
        cipher = ""
        for x in InvPMatrix[0]:
            cipher += roundFunRes[x]
        return cipher


    def Encrypt(self, message, key):
        binTxt = ConvAlphaBin.conv_bin(message)
        clearKey = ConvAlphaBin.nib_vnoc(key)
        roundkeys = self.genSubkeys(key)
        permutedTxt = self.DoInitialPerm(self.constDes["PI"], binTxt)
        left,right = self.splitHalf(permutedTxt)
        for round in range(16):
            newR = self.f.XOR(left, self.f.DoF(right, roundkeys[round], self.constDes["E"], self.constDes["PERM"]))
            newL = right
            right = newR
            left = newL
        cipher = self.DoInversePerm(self.constDes["PI_I"], right+left)
        return cipher

    def Decrypt(self, message, key):
        binTxt = ConvAlphaBin.conv_bin(message)
        clearKey = ConvAlphaBin.nib_vnoc(key)
        roundkeys = self.genSubkeys(key)
        permutedTxt = self.DoInitialPerm(self.constDes["PI"], binTxt)
        right,left = self.splitHalf(permutedTxt)
        for round in range(16):
            newR = self.f.XOR(left, self.f.DoF(right, roundkeys[16-round], self.constDes["E"], self.constDes["PERM"]))
            newL = right
            right = newR
            left = newL
        cipher = self.DoInversePerm(self.constDes["PI_I"], right+left)
        return cipher


