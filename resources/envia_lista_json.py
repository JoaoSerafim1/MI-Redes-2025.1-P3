from solcx import compile_standard, install_solc
from web3 import Web3
import json

# 1. Instalar versão do compilador Solidity
install_solc("0.8.0")

# 2. Ler contrato
with open("ListaCodificada.sol", "r") as file:
    contrato_source = file.read()

# 3. Compilar contrato
compilado = compile_standard({
    "language": "Solidity",
    "sources": {"ListaCodificada.sol": {"content": contrato_source}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "evm.bytecode"]
            }
        }
    }
}, solc_version="0.8.0")

# 4. Obter ABI e Bytecode
abi = compilado["contracts"]["ListaCodificada.sol"]["ListaCodificada"]["abi"]
bytecode = compilado["contracts"]["ListaCodificada.sol"]["ListaCodificada"]["evm"]["bytecode"]["object"]

# 5. Conectar ao Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
conta = w3.eth.accounts[0]

# 6. Implantar contrato
Contrato = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Contrato.constructor().transact({'from': conta})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
endereco_contrato = tx_receipt.contractAddress
print(f"Contrato implantado em: {endereco_contrato}")

# 7. Instanciar contrato
lista = w3.eth.contract(address=endereco_contrato, abi=abi)

# 8. Lista de listas → JSON
lista_de_listas = [["produto", "preco"], ["banana", "3.50"], ["laranja", "4.00"]]
json_codificado = json.dumps(lista_de_listas)

# 9. Enviar JSON para a blockchain
tx = lista.functions.adicionarLista(json_codificado).transact({'from': conta})
w3.eth.wait_for_transaction_receipt(tx)
print("Lista enviada com sucesso!")

# 10. Recuperar e decodificar
index = 0
json_recebido = lista.functions.obterLista(index).call()
lista_recebida = json.loads(json_recebido)

print("\nLista recuperada da blockchain:")
for linha in lista_recebida:
    print(linha)
