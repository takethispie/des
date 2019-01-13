import Extract_ConstantesDES
import ConvAlphaBin
import Feistel


class Des:
    def __init__(self):
        self.const_des = Extract_ConstantesDES.recup_constantes_des()
        self.roundSH = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
        self.feistel = Feistel.Feistel()

    def gen_sub_keys(self, key64):
        # Les bits de control se supprime direct avec la permutation CP1
        key56 = self.feistel.do_permutation_key(self.const_des["CP_1"], key64)  # Permutation CP1
        key_left, key_right = self.feistel.split_half_56bits(key56)
        sub_keys = list()
        for roundNum in range(16):
            new_key_left = self.feistel.left_shift(key_left, 1)
            new_key_right = self.feistel.left_shift(key_right, 1)
            new_key = new_key_left + new_key_right
            sub_key = self.feistel.do_permutation_key(self.const_des["CP_2"], new_key)  # Expansion CP2
            sub_keys.append(sub_key)
            key_left = new_key_left
            key_right = new_key_right
        return sub_keys

    def encrypt(self, message, key):
        if message[0] != '0' or message[0] != '1':
            bin_message = ConvAlphaBin.conv_alpha_to_bin(message)  # Conversion du message en binaire
        else:
            bin_message = message

        # 1- Création de 16 sous-clefs
        round_keys = self.gen_sub_keys(key)

        # 2 - Paquetage
        blocks = self.feistel.split_many_blocks_64bits(bin_message)  # Split du message binaire en plusieurs blocs de 64bits

        # 3 - Permutation initiale
        pi_left = list()
        pi_right = list()
        for i in range(0, len(blocks) - 1):
            blocks[i] = self.feistel.do_permutation_key(self.const_des["PI"], blocks[i])  # Permutation PI
            left, right = self.feistel.split_half_64bits(blocks[i])
            pi_left.append(left)
            pi_right.append(right)

        # 4 - Rondes (Pour chacun des blocs)
        result = list()
        for i in range(0, len(pi_left[0]) - 1):  # Ou pi_left, ça revient au même
            left = pi_left[i]
            right = pi_right[i]
            cipher = ""
            for j in range(16):
                dof_result = self.feistel.do_feistel(right, round_keys[j], self.const_des["E"], self.const_des["PERM"])
                temp_right = self.feistel.xor(left, dof_result)
                temp_left = right
                right = temp_right
                left = temp_left
                # 5 - Permutation initiale inverse
                cipher = self.feistel.do_permutation_key(self.const_des["PI_I"], temp_right + temp_left)
            result.append(cipher)

        alpha_message = ConvAlphaBin.conv_bin_to_alpha(result)  # Conversion du message en alphab
        return alpha_message

    def decrypt(self, message, key):
        return message
