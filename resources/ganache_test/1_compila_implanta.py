from web3 import Web3
from solcx import compile_standard, install_solc, set_solc_version
import json

# Instala o compilador Solidity
install_solc("0.8.0")
set_solc_version("0.8.0")

# Conexão com Ganache (GUI ou outro)
w3 = Web3(Web3.HTTPProvider("http://host.docker.internal:7545"))
assert w3.is_connected(), "❌ Falha na conexão com Ganache"

# Conta padrão (Ganache)
conta = w3.eth.accounts[0]

# Lê o contrato Solidity
with open("ListaCodificada.sol", "r") as f:
    contrato_fonte = f.read()

# Compila
compilado = compile_standard({
    "language": "Solidity",
    "sources": {"ListaCodificada.sol": {"content": contrato_fonte}},
    "settings": {
        "outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}
    }
})

# Extrai ABI e Bytecode
abi = compilado["contracts"]["ListaCodificada.sol"]["ListaCodificada"]["abi"]
bytecode = compilado["contracts"]["ListaCodificada.sol"]["ListaCodificada"]["evm"]["bytecode"]["object"]

# Implanta contrato
Contrato = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Contrato.constructor().transact({'from': conta})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Salva dados localmente
with open("abi.json", "w") as f:
    json.dump(abi, f)

with open("endereco.txt", "w") as f:
    f.write(tx_receipt.contractAddress)

# Feedback
print("✅ Contrato implantado com sucesso!")
print("📍 Endereço do contrato:", tx_receipt.contractAddress)

#PARA EXECUTAR:
#docker-compose build
#docker-compose run web3client bash
#python3 1_compila_implanta.py
#python3 2_interage_contrato.py
