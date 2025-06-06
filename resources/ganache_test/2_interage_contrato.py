from web3 import Web3
import json

# Conexão com Ganache
w3 = Web3(Web3.HTTPProvider("http://host.docker.internal:7545"))
assert w3.is_connected(), "❌ Falha na conexão com Ganache"

# Conta padrão
conta = w3.eth.accounts[0]

# Carrega ABI e endereço
with open("abi.json", "r") as f:
    abi = json.load(f)

with open("endereco.txt", "r") as f:
    endereco = f.read().strip()

# Conecta ao contrato
contrato = w3.eth.contract(address=endereco, abi=abi)

# Exemplo: envia lista de listas
import json as pyjson
lista = [["banana", "3.50"], ["laranja", "2.00"]]
json_str = pyjson.dumps(lista)

# Transação
tx = contrato.functions.adicionarLista(json_str).transact({'from': conta})
w3.eth.wait_for_transaction_receipt(tx)

# Consulta
total = contrato.functions.totalListas().call()
print("📦 Total de listas:", total)

for i in range(total):
    print(f"📄 Lista #{i}:", contrato.functions.obterLista(i).call())
