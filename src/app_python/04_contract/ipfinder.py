#Importa bibliotecas basicas do python 3
import socket


#IP do servidor
localServerIP = socket.gethostbyname(socket.gethostname())


print("-------------------------------------------------------------------------")
print("IP da maquina local: " + str(localServerIP))
print("-------------------------------------------------------------------------")