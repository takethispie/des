import des

def main():
    mydes = des.Des()
    message = "0123456789ABCDEF"
    key = "1110111111000100110111111010000110011110010100100000111001000011"
    res = mydes.Encrypt(message, key)
    print(res)

main()
