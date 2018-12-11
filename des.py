import Extract_ConstantesDES

class Des:
    def __init__(self):
        self.constDes = Extract_ConstantesDES.recupConstantesDES()

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

    def DoCompression(self, key56):
        key48 = ""
        for i in self.constDes["CP_2"]:
            for j in i:
                key48 += key56[j]
        return key48



