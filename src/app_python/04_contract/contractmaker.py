#Importa bibliotecas basicas do python 3
import socket

#Importa bibliotecas adicionais
from solcx import compile_standard, install_solc
from web3 import Web3
from eth_account import Account

#IP do servidor, porta do broker MQTT e porta para requisicoes HTTP
localServerIP = socket.gethostbyname(socket.gethostname())

#Porta do cliente blockchain
blockchainNodePort = 7545

#Pergunta endereco do node da blockchain
blockchainNodeIP = input("Insira o endereço IP do Cliente da Blockchain (OU PRESSIONE ENTER para utilizar o endereço da maquina local): ")

#Pergunta chave privada da conta
blockchainAccountPrivateKey = input("Insira a chave privada da conta a ser utilizada para acessar a Blockchain : ")

if (blockchainNodeIP == ""):
    blockchainNodeIP = localServerIP

# 1. Instalar versão do compilador Solidity
install_solc("0.8.0")

# 2. Ler contrato
with open("sl.sol", "r") as file:
    contrato_source = file.read()

# 3. Compilar contrato
compilado = compile_standard({
    "language": "Solidity",
    "sources": {"sl.sol": {"content": contrato_source}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
})

# 4. Obter ABI e Bytecode
abi = compilado["contracts"]["sl.sol"]["ListaCodificada"]["abi"]
bytecode = compilado["contracts"]["sl.sol"]["ListaCodificada"]["evm"]["bytecode"]["object"]

# 5. Conectar ao blockchain
w3 = Web3(Web3.HTTPProvider("http://" + str(blockchainNodeIP) + ":" + str(blockchainNodePort)))
conta = Account.from_key(blockchainAccountPrivateKey)

# 6. Implantar contrato
Contrato = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Contrato.constructor().transact({'from': conta.address})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
endereco_contrato = tx_receipt.contractAddress

# 7. Instanciar contrato
lista = w3.eth.contract(address=endereco_contrato, abi=abi)

print("*************************************************************************")
print("CONTRATO ESTABELECIDO!")
print("ABI: " + str(abi))
print("ENDERECO: " + str(endereco_contrato))
print("IP da maquina local: " + str(localServerIP))
print("*************************************************************************")