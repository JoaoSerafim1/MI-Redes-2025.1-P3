#Importa bibliotecas basicas do python 3
import string
import random
import hashlib

lettersanddigits = string.ascii_uppercase + string.digits
hashHandler = hashlib.sha256()

#Loop para gerar IDs ate satisfazer certas condicoes
for idIndex in range(0, 20):

    newRandomID = ""

    #Concatena os os digitos ou letras aleatorios para um novo ID
    for count in range(0,24):
        newRandomID += random.choice(lettersanddigits)

    hashHandler.update(newRandomID.encode())
    newRandomHashedID = ("ID-" + str(hashHandler.hexdigest()))
    newRandomHashedFileName = (newRandomHashedID + ".json")

    print(newRandomID)
    print(newRandomHashedFileName)
    print(len(newRandomHashedID))
    print(len(newRandomHashedFileName))