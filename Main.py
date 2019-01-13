import DES
import User_Dialog
import ConvAlphaBin


def main():
    my_des = DES.Des()
    user_dialog = User_Dialog.UserDialog()

    # encrypt_decrypt = user_dialog.encrypt_or_decrypt()
    message = user_dialog.get_input_message(1)
    key = user_dialog.get_input_key()
    # where_print_result = user_dialog.where_result()

    encrypt_decrypt = user_dialog.DECRYPT
    # message = "D:\Project\Python\des\Messages\Chiffrement_DES_de_Orelsan.txt"
    # key = "D:\Project\Python\des\Messages\Clef_de_Orelsan.txt"
    # message = "je sais pas trop mais je test des trucs plutot interessant ahah"
    # key = "0100110010101110110111001010110111000100011010001100100000101010"
    where_print_result = user_dialog.CONSOLE

    if encrypt_decrypt == user_dialog.ENCRYPT:
        message = my_des.encrypt(message, key)
    elif encrypt_decrypt == user_dialog.DECRYPT:
        message = my_des.decrypt(message, key)

    if where_print_result == user_dialog.CONSOLE:
        print(message)
    elif encrypt_decrypt == user_dialog.FILE:
        open("result.txt", "w").write(message)
        print("Le fichier résultat 'result.txt' a été enregistré à la racine du projet.")


# Run this app
main()
