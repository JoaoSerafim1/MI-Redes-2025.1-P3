###########################################################
#
# => MODULO DE USO DA BLOCKCHAIN <=
#
###########################################################


#Importa bibliotecas basicas do python 3
import threading
import json
import time

#Importa bibliotecas adicionais
from solcx import compile_standard, install_solc
from web3 import Web3

#Importa os modulos da aplicacao
from application.util import *

def addToBlockchain(blockchainNodeIP, blockchainNodePort, abi, endereco_contrato, dataType, dataLabel, infoTable):
    
    try:
        objectToStore = [dataType, dataLabel, infoTable]

        # 5. Conectar ao blockchain
        w3 = Web3(Web3.HTTPProvider("http://" + blockchainNodeIP + ":" + str(blockchainNodePort)))
        conta = w3.eth.accounts[0]

        # 7. Instanciar contrato
        lista = w3.eth.contract(address=endereco_contrato, abi=abi)

        # 8. objeto a ser gravado → JSON
        
        #lista_de_listas = [["produto", "preco"], ["banana", "3.50"], ["laranja", "4.00"]]
        
        json_codificado = json.dumps(objectToStore)

        # 9. Enviar JSON para a blockchain
        tx = lista.functions.adicionarLista(json_codificado).transact({'from': conta})
        w3.eth.wait_for_transaction_receipt(tx)

        #print("Lista enviada com sucesso!")
    
    except:
        pass

#Funcao para realizar sincronizacao com a blockchain
def syncWithBlockchain (fileLock: threading.Lock, blockchainNodeIP, blockchainNodePort, abi, endereco_contrato):
    
    try:
        
        # 5. Conectar ao blockchain
        w3 = Web3(Web3.HTTPProvider("http://" + blockchainNodeIP + ":" + str(blockchainNodePort)))
        conta = w3.eth.accounts[0]

        # 7. Instanciar contrato
        lista = w3.eth.contract(address=endereco_contrato, abi=abi)

        #Tamanho da lista de elementos do contrato
        chainSize = int(lista.functions.totalListas().call())
        
        #Percorrer os elementos do contrato
        for chainIndex in range(0, chainSize):
            
            # 10. Recuperar e decodificar
            json_recebido = lista.functions.obterLista(chainIndex).call()
            recoveredPurchase = json.loads(json_recebido)

            purchaseID = recoveredPurchase[1]
            purchaseInfoTable = recoveredPurchase[2]

            #Nome do arquivo da compra
            purchaseFileName = purchaseID + ".json"

            #ID do veiculo que fez a compra
            vehicleID = purchaseInfoTable["vehicle_ID"]

            #Nome do arquivo do veiculo
            vehicleFileName = vehicleID + ".json"
            
            #Dicionario de informacoes do veiculo, inicialmente vazio
            vehicleInfo = {}

            #Carrega o dicionario de informacoes do veiculo, se possivel
            if (verifyFile(["clientdata", "clients", "vehicles"], vehicleFileName) == True):
                
                vehicleInfo = readFile(["clientdata", "clients", "vehicles", vehicleFileName])
            
            else:

                vehicleInfo["purchases"] = []

            #Adiciona a compra a lista de compras do veiculo (cliente) e grava o resultado
            vehicleInfo["purchases"].append(purchaseID)

            fileLock.acquire()

            #Grava as informacoes remotas
            writeFile(["clientdata", "purchases", purchaseFileName], purchaseInfoTable)
            writeFile(["clientdata", "clients", "vehicles", vehicleFileName], vehicleInfo)

            fileLock.release()
    
    except:
        pass