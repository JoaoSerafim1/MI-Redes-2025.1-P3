###########################################################
#
# => MODULO DE USO DA BLOCKCHAIN <=
#
###########################################################


#Importa bibliotecas basicas do python 3
import threading
import json

#Importa bibliotecas adicionais
from web3 import Web3
from eth_account import Account

#Importa os modulos da aplicacao
from application.util import *

def addToBlockchain(blockchainNodeIP, blockchainNodePort, blockchainAccountPrivateKey, abi, endereco_contrato, dataType, dataLabel, infoTable):
    
    try:

        # 5. Conectar ao blockchain
        w3 = Web3(Web3.HTTPProvider("http://" + blockchainNodeIP + ":" + str(blockchainNodePort)))
        conta = Account.from_key(blockchainAccountPrivateKey)

        # 7. Instanciar contrato
        lista = w3.eth.contract(address=endereco_contrato, abi=abi)

        # 8. objeto a ser gravado → JSON
        objectToStore = [dataType, dataLabel, infoTable]
        json_codificado = json.dumps(objectToStore)

        # 9. Enviar JSON para a blockchain
        tx = lista.functions.adicionarLista(json_codificado).transact({'from': conta.address})
        w3.eth.wait_for_transaction_receipt(tx)
    
    except:
        pass

#Funcao para realizar sincronizacao com a blockchain
def syncWithBlockchain (fileLock: threading.Lock, blockchainNodeIP, blockchainNodePort, blockchainContractABI, blockchainContractAddress, blockchainSyncIndex):
    
    try:
        
        # 5. Conectar ao blockchain
        w3 = Web3(Web3.HTTPProvider("http://" + blockchainNodeIP + ":" + str(blockchainNodePort)))

        # 7. Instanciar contrato
        lista = w3.eth.contract(address=blockchainContractAddress, abi=blockchainContractABI)

        #Tamanho da lista de elementos do contrato
        chainSize = int(lista.functions.totalListas().call())
        
        #Percorrer os elementos do contrato
        for chainIndex in range(blockchainSyncIndex, chainSize):
            
            fileLock.acquire()

            try:

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

                if (purchaseID not in vehicleInfo["purchases"]):
                        
                    #Adiciona a compra a lista de compras do veiculo (cliente) e grava o resultado
                    vehicleInfo["purchases"].append(purchaseID)

                #Grava as informacoes remotas
                writeFile(["clientdata", "purchases", purchaseFileName], purchaseInfoTable)
                writeFile(["clientdata", "clients", "vehicles", vehicleFileName], vehicleInfo)
                #print(purchaseID)
            except:
                pass

            fileLock.release()

        #Atualiza o indice de elemento da blockchain
        blockchainSyncIndex = chainSize

        #Guarda a informacao no arquivo
        fileLock.acquire()
        writeFile(["serverdata", "sync_index.json"], blockchainSyncIndex)
        fileLock.release()

        #Retorna o indice do elemento da blockchain
        return blockchainSyncIndex
    
    except:
        pass