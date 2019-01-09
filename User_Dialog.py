class UserDialog:
    ENCRYPT = 0
    DECRYPT = 1
    CONSOLE = 0
    FILE = 1

    # Propose de chiffrer ou décriffrer
    def encrypt_or_decrypt(self):
        while True:
            result = input("Souaitez-vous [0]chiffrer ou [1]déchiffrer ? : ")
            if int(result) == self.ENCRYPT or int(result) == self.DECRYPT:
                break
            else:
                print("Réponse incorrect... veuillez choisir entre [0] et [1].")
        return int(result)

    # Demande de renseigner le message
    def get_input_message(self, encrypt_or_decrypt):
        dialog = "Entrer le texte (ou le chemin vers votre fichier)"
        if encrypt_or_decrypt == self.ENCRYPT:
            dialog += " à chiffrer : "
        elif encrypt_or_decrypt == self.DECRYPT:
            dialog += " à déchiffrer : "

        while True:
            input_message = input(dialog)
            if input_message != "":
                try:
                    result = open(input_message, 'r').read()
                except IOError:
                    result = input_message
                if result != "":
                    break
                else:
                    print("Message null")
            else:
                print("Aucun message (ou chemin) n'a été entré !")
        return result

    # Demande de renseigner la clé
    @staticmethod
    def get_input_key():
        while True:
            input_key = input("Entrer la clé (ou le chemin vers le fichier contenant la clé) à utiliser : ")
            if input_key != "":
                try:
                    result = open(input_key, 'r').read()
                except IOError:
                    result = input_key
                if result != "":
                    break
                else:
                    print("Clé null")
            else:
                print("Aucune clé (ou chemin) n'a été entré !")
        return result

    # Demande où affciher le resultat
    def where_result(self):
        while True:
            result = input("Affichage du résultat : [0]console [1]fichier texte ? : ")
            if int(result) == self.CONSOLE or int(result) == self.FILE:
                break
            else:
                print("Réponse incorrect... veuillez choisir entre [0] et [1].")
        return int(result)
