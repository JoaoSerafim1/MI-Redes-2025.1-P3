#PROPRIEDADES DO SERVIDOR
####################################################################################

#Maximo de threads simultaneos para requisicoes de clientes (estacoes, veiculos)
maxClientThreads = 8

#Maximo de threads simultaneos para requisicoes de outros servidores
maxServerThreads = 8

#Porta do broker MQTT, porta para requisicoes HTTP e porta para interacao com blockchain
mqttPort = 1883
httpPort = 8025
blockchainNodePort = 7545

#IP do broker MQTT de teste
testBroker = 'broker.emqx.io'

#Tempo em segundos antes e depois do horario exato marcado durante o qual um posto de recarga sera considerado como "ocupado"
timeWindow = 7200

#Tempo em segundos entre cada acao de sincronizacao
syncWindow = 600

#ABI do contrato solidity
blockchainContractABI = [{'anonymous': False, 'inputs': [{'indexed': False, 'internalType': 'string', 'name': 'jsonData', 'type': 'string'}], 'name': 'ListaAdicionada', 'type': 'event'}, {'inputs': [{'internalType': 'string', 'name': 'jsonData', 'type': 'string'}], 'name': 'adicionarLista', 'outputs': [], 'stateMutability': 'nonpayable', 'type': 'function'}, {'inputs': [{'internalType': 'uint256', 'name': 'index', 'type': 'uint256'}], 'name': 'obterLista', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'name': 'totalListas', 'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}], 'stateMutability': 'view', 'type': 'function'}]

####################################################################################