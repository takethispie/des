import Extract_ConstantesDES
import ConvAlphaBin

class Des:
    def __init__(self):
        self.constDes = Extract_ConstantesDES.recupConstantesDES()
        self.roundSH = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    def DoPC1(self, key64):
        key56 = ""
        for i in self.constDes["CP_1"]:
            for j in i:
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
        for i in self.constDes["CP_2"]:
            for j in i:
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
        for y in IPMatrix:
            for x in y:
                permutated += text[int(x)]
        return permutated


    def splitHalf(binarybits):
        return binarybits[:32], binarybits[32:]


    def DoInversePerm(self, InvPMatrix, roundFunRes):
        cipher = ""
        for y in InvPMatrix:
            for x in y:
                cipher += roundFunRes[int(x)]
        return cipher
