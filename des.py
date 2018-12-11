import Extract_ConstantesDES

class Des:
    def __init__(self):
        self.constDes = Extract_ConstantesDES.recupConstantesDES()

    def DoPC1(self, key64):
        key56 = ""
        for i in self.constDes["CP_1"]:
            key56 += key64[i-1]
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
            key48 += key56[i-1]
        return key48



