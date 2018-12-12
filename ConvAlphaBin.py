		
#####################################################
#		   	 	DICTIONNAIRE BINAIRE				#
#####################################################

ALPHABET = ""
ALPHABET +="ABCDEFGHIJKLMNOPQRSTUVWXYZ"#Les 26 lettres de l'alphabet en majuscule
ALPHABET +="abcdefghijklmnopqrstuvwxyz"#Les 26 lettres de l'alphabet en minuscule
ALPHABET+=" " #caractère 53
ALPHABET+="." #caractère 54
ALPHABET+="," #caractère 55
ALPHABET+="!" #caractère 56
ALPHABET+="?" #caractère 57
ALPHABET+="'" #caractère 58
ALPHABET+='"' #caractère 59
ALPHABET+="é" #caractère 60
ALPHABET+="è" #caractère 61
ALPHABET+="à" #caractère 62
ALPHABET+="-" #caractère 63
ALPHABET+="\n" #caractère 64

ALPHABETBINAIRE=dict()
for i in range(0, 64) :
	x=bin(i)
	y='0000'+x[2:]
	ALPHABETBINAIRE[i]=y[-5]+y[-4]+y[-3]+y[-2]+y[-1]


#Renvoie a chaine de caractère txt avec uniquement les caractères de l'alphabet.
def FiltreTXT(txt) :
	res=""
	for c in txt :
		if(ALPHABET.find(c)!=-1) : res+=c
		elif(c=='ê' or c=='ë') : res+='e'
		elif(c=='â') : res+='a'
		elif(c=='ç') : res+='c'
		elif(c=='î') : res+='i'
		elif(c=='Ç') : res+='C'
		elif(c=='ù' or c=="û") : res+='u'
		elif(c=='ô') : res+='o'
		elif(c=='Ô') : res+='O'
		elif(c=='œ') : res+='oe'
		elif(c=="À") : res+='A'
		elif(c=="È" or c=="É") : res+='E'
	return res

	
#prend en paramètre un texte et renvoie la chaine binaire associée (en suivant le dictionnaire)
def conv_bin(txt) :
	X=""
	for c in FiltreTXT(txt) : X+=ALPHABETBINAIRE[ALPHABET.find(c)]
	return X


HexToBin = {'0':'0000',
		 '1':'0001',
		 '2':'0010',
		 '3':'0011',
		 '4':'0100',
		 '5':'0101',
		 '6':'0110',
		 '7':'0111',
		 '8':'1000',
		 '9':'1001',
		 'A':'1010',
		 'B':'1011',
		 'C':'1100',
		 'D':'1101',
		 'E':'1110',
		 'F':'1111',
		}

def hexDigitToBinaryBits(hex_digit):
	binary_4bits = HexToBin[hex_digit]
	return binary_4bits


def hexString_to_binary_bits1(hex_string):
	binary_bits = ""
	for hex_digit in hex_string:
		binary_bits += hexDigitToBinaryBits(hex_digit)
	return binary_bits


def HexToBinary(hexdigits):
	res = ""
	for hexdigit in hexdigits:
		res += bin(int(hexdigit, 16))[2:].zfill(4)
	return res
