import des

def main():
    mydes = des.Des()
    message = "lolopooptest"
    key = "1110111111000100110111111010000110011110010100100000111001000011"
    res = mydes.Encrypt(message, key)
    res2 = mydes.Decrypt(res, key)
    print(res2)

main()
