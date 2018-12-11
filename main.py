import des

def main():
    mydes = des.Des()
    res = mydes.genSubkeys("0001001100110100010101110111100110011011101111001101111111110001")
    print(res)

main()
