import DES


def main():
    my_des = DES.Des()

    key = "0100110010101110110111001010110111000100011010001100100000101010"

    # message_encrypted = "zENEDyWtIzB!m QfTKodCpf,MhybIX,'ye,ànèM'féCcrB-uRu!m"
    message_decrypted = "je sais pas trop"

    message_encrypted = my_des.encrypt(message_decrypted, key)
    print("Encrypted message =>", message_encrypted)

    # message_decrypted = my_des.decrypt(message_encrypted, key)
    # print("Decrypted message =>", message_decrypted)


# Run this app
main()
