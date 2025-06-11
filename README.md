# Sistemas distribuídos - recarga de veículos elétricos com protocolos de comunicação MQTT / HTTP-REST e uso de blockchain tipo Ethereum.

Chamamos sistemas distribuídos aqueles compostos por várias instâncias individuais de aplicação, costumeiramente de dois ou mais tipos distintos, que trabalham em conjunto para prover um serviço em massa.

No contexto do MI de Concorrência e Conectividade da UEFS, semestre 2025.1, foi requisitado aos alunos a confecção de um sistema distribuído capaz de coordenar a recarga de veículos elétricos, além de monitorar o nível de carga dos veículos no qual a versão de usuário final está instanciada, e fornecer informações acerca do histórico de compras (recargas) de um usuário final.

O sistema aqui desenvolvido conta com 4 versões, cada uma destinada a ser executada por um agente distinto:
- Estabelecimento de contrato: É encontrado aqui o arquivo solidity que descreve o contrato para interação com a blockchain tipo Ethereum, além de uma aplicação Python que é capaz de instanciar e firmar tal contrato. A ação de firmar um contrato só deve ser executada uma vez por instância de todo o sistema.
- Servidor: Aplicação pertencente aos provedores do serviço. Recebe requisicões das aplicações-cliente (veículo/usuário final e estação de recarga) e de outros servidores, validando, executando e registrando tão requisições. Também faz sincronização por meio de uso de blockchain tipo Ethereum.
- Estação de recarga: Software instalado em computadores de cada ponto de recarga. Rotineiramente "pergunta" ao servidor se existe veículo a ser recarregado, caso disponível.
- Veículo (usuário final): Programa responsável por prover a um motorista de automóvel a opção de requisitar serviços de recarga por meio de pagamento, reservar pontos em horários desejado e visualizar compras bem-sucedidas registradas em um determinado servidor. Como dito anteriormente, também monitora o nível de carga do veículo no qual é instalado.

# Sumário (clique para ir até a seção desejada)

[1. Instalação e uso da aplicação](#Instalação-e-uso-da-aplicação)

[2. Comunicação por protocolo HTTP-REST e MQTT](#Comunicação-por-protocolo-HTTP-REST-e-MQTT)

[3. Sincronização com uso de blockchain tipo Ethereum](#Sincronização-com-uso-de-blockchain-tipo-Ethereum)

[4. Desenvolvimento com uso de containers por meio de Docker Engine](#Desenvolvimento-com-uso-de-containers-por-meio-de-Docker-Engine)

[5. Ferramentas de Densenvolvimento Adicionais](#Ferramentas-de-Densenvolvimento-Adicionais)

[6. Bibliografia](#Bibliografia)
  
# Instalação e uso da aplicação

## Requisitos básicos
- Sistema operacional compatível com protocolo TCP-IP e Python (ex: [Ubuntu](https://ubuntu.com/download), [Windows](https://www.microsoft.com/pt-br/windows/)).
- [Python](https://www.python.org/downloads/) 3.9 (recomendado: gerenciador de ambientes virtuais [Anaconda](https://www.anaconda.com/download)).
- [Pip para Python](https://pypi.org/project/pip/)
- Contrato: [wget](https://www.gnu.org/software/wget/) (apenas para Linux), [build-essential](https://packages.ubuntu.com/jammy/build-essential) (apenas para Linux)
- Veículo: [tkinter](https://docs.python.org/3/library/tkinter.html), [fontconfig](https://www.freedesktop.org/wiki/Software/fontconfig/) (apenas para Linux)
## Recursos Adicionais
- Servidor: Broker MQTT (ex: [Eclipse Mosquitto](https://mosquitto.org/download/))
  
## 📦 Instalando e utilizando as diferentes versões do sistema distribuído

As versões do sistema destinadas a usuários distintos estão disponíveis individualmente neste repositório online, em formato .zip, na sessão "Releases" (encontrada no canto direito da tela inicial do repositório na maioria dos navegadores).

Cada versão do sistema distribuído possui  requerimentos em termos de bibliotecas Python contidos em arquivos `requirements.txt`, estando esses nos diretórios principais das aplicações.
```
  pip install -r requirements.txt
```
OU
```
  pip3 install -r requirements.txt
```
##### (Instala as bibliotecas em sistemas tipo Linux e segundo o arquivo `requirements.txt`.

Note que a instalação de bibliotecas Python é por padrão impedida fora de ambientes virtuais, visto o risco de conflitos com a versão mais nova do Python (possivelmente utilizada pelo sistema operacional e/ou outras aplicações) que tal ação pode gerar. Caso deseje, de fato, forçar a instalação das bibliotecas fora de um ambiente virtual, adicione o argumento `--break-system-packages` ao comando de instalação.
```
  pip install -r requirements.txt --break-system-packages
```
OU
```
  pip3 install -r requirements.txt --break-system-packages
```
##### (Instala, DE FORMA FORÇADA, as bibliotecas em sistemas tipo Linux e segundo o arquivo `requirements.txt`.

### 📄 Estabelecimento de contrato

O arquivo .zip da versão da aplicação responsável por estabelecer um contrato (ferramenta da blockchain Ethereum) possui ```contract``` antes de seu número de versão. Para iniciar o programa, execute o arquivo ```contract_maker.py```

![tela_inicial_contrato](/imgs/contract_waiting.png?raw=true "Instruções do início do programa e prompt de entrada do endereço do cliente da blockchain e da chave privada")

Após o fornecimento do endereço do cliente da blockchain e da chave privada da conta escolhida para a ação de estabelecimento do contrato, o contrato será firmado no blockchain, e suas informações de ABI ("esqueleto" do contrato) e endereço serão exibidas.

![Tela apos estabelecimento do contrato](/imgs/contract_after_deployment.png?raw=true "Resultado de um contrato bem-sucedido")

Note que o valor ABI de um contrato baseado em um determinado compilado solidity deve permanecer o mesmo para qualquer instância criada, ou seja, a menos que sejam feitas alterações na estrutura do contrato, o valor exibido após a ação de estabelecimento do contrato será o mesmo daquele encontrado no arquivo de propriedades de cada servidor (`/application/properties.py` a partir do diretório principal da aplicação do servidor), dispensando qualquer mudança.

No entanto, o endereço do contrato é único para cada instância do mesmo, e considerando que todos os servidores conectados a um sistema devem utilizar um único contrato para sincronização, tal endereço possui importância em ser gravado.

Por fim, é importante lembrar que o contrato não limita de forma alguma quem pode realizar as ações de sincronização. Assim sendo, a implementação do sistema distribuído em situações reais deve ser fazer uso de uma distribuição privada do Ethereum, distribuição essa que só permita a inclusão de clientes e contas criados em clientes existente e utilizando contas existentes.

### ☁️ Servidor

O arquivo .zip do servidor possui ```server``` antes de seu número de versão. Para iniciar o programa do servidor, execute o arquivo ```server.py```, encontrado no diretório principal da aplicação. Após a inicialização, será pedido ao usuário do sistema que insira o endereço do cliente da blockchain e da chave privada de uma conta qualquer existente na blockchain, e do endereço do contrato utilizado para a ação de sincronização. Também será requisitada a entrada de um endereço para o broker MQTT, sempre na porta TCP 1883. Caso deseje usar um broker MQTT que está rodando com o mesmo endereço do servidor, também na porta TCP 1883, pressione ENTER sem prover entrada alguma.

Nota: Utilizar a entrada "test" resulta na escolha de um broker MQTT de teste pre-definido, por padrão aquele da [EMQX](https://www.emqx.com/en/mqtt/public-mqtt5-broker) (endereço: broker.emqx.io, porta TCP 1883).

![tela_inicial_servidor](/imgs/server_waiting.png?raw=true "Instruções do início do programa e prompt de entrada do broker MQTT, endereço do cliente da blockchain e da chave privada")

Não existe verificação para a entrada de informações corretas / válidas, mas a impossibilidade de sincronização não resulta em mal-funcionamento das operações do sistema. Ademais, a impossibilidade de sincronização pode (e deve) ser eventualmente resolvida, o que deve incluir a reinicialização da aplicação do servidor em caso de entrada incorreta.

Após o cadastro de uma estação de carga, o servidor automaticamente gerará um novo ID que deverá ser utilizado na próxima operação do tipo, e em seguida exibirá na tela tal informação.

![Tela inicial apos cadastrar primeira estação de carga](/imgs/server_after_station.png?raw=true "Resultado no terminal de uma operação de cadastro de estação de carga")

O recebimento de mensagens, bem como a execução de ações em cima do banco de dados do servidor, são todas operações registrados em arquivos de texto (logs), os quais podem ser encontrados nas pastas ```/logs/received/``` (recados/requisições lidos/recebidas) e ```logs/performed/``` (ações executadas pelo servidor).

Logs possuem o seguinte formato:
- Título: YYYY-MM-DDD = Data local
- Conteúdo:
  - [YYYY-MM-DDD hh:mm:ss.ssssss] => Data e horário locais (24 horas)
  - NAME:
  - NOME-DA-ENTRADA => Informação do nome da entrada no log
    - RVMQTT:        Recado MQTT lido
    - HTTPREQUEST:   Requisição HTTP recebida
    - RGTSTATION:    Registrar nova estação
    - RGTVEHICLE:    Registrar novo veículo
    - GETBOOKED:     Obter informações acerca de possível veículo agendado (estação)
    - FREESPOT:      Liberar estação para agendamento
    - GETDISTANCE:   Obter e retornar informações da estação dispónível mais próxima de um veículo
    - RTDETAILS:     Obter informações de uma rota em específico
    - RESROUTE:      Reservar uma rota
    - PHCCHARGE:     Confirmar pagamento e agendar recarga
    - PCHDETAILS:    Obter e retornar informações de uma determinada compra (de acordo com o ID do veículo vinculado à compra e ao índice da compra)
  - TIPO-DA-ENTIDADE => Tipo do identificador da entidade que gerou a entrada
    - ADDRESS:       Endereço IP (tipo de usuário não-definido)
    - S_ID:          ID de estação de carga
    - V_ID:          ID de veículo
    - V_ADD:         Endereço IP de um usuário que supõe-se ser um veículo
  - IDENTIFICADOR-DA-ENTIDADE => Identificador da entidade que gerou a entrada

![Tela do arquivo de texto de um log](/imgs/server_log.png?raw=true "Log referentes às ações executadas pelo servidor no dia 04 de Abril de 2025, data local")

A reserva de rotas é feita com base em listas de nós contendo endereços de servidores e as siglas de suas respectivas cidades, cabendo ao adminsitrador do sistema editar o arquivo `routes.json` encontrado na pasta `/serverdata/` de forma a disponibilizar tais rotas. Note que uma rota jamais deve incluir o próprio servidor, devido a limitações em requisições HTTP enviadas e recebidas por uma mesma aplicação.

![Tela do arquivo de json de rotas](/imgs/server_routes.png?raw=true "Exemplo de arquivo routes.json, contendo uma lista de rotas disponíveis em um servidor")

Pressionar a tecla ENTER durante a execução do servidor inicia o processo de encerramento da aplicação, como já explicitado anteriormente na saída do terminal.

Nota: Por questões de limitações do código, é necessário enviar uma requisição HTTP qualquer ao endereço do servidor, porta 2025, para que ocorra o encerramento correto do programa. No entanto, reiniciar o sistema da máquina do servidor também soluciona o impasse (caso seja impossível o envio de uma requisição HTTP). Tendo em vista que todas as operações de dados ocorrem em cima do sistema de arquivos, é seguro reiniciar o sistema a qualquer momento após iniciar o processo de encerramento do programa, mesmo que este não seja concluído.

![Tela de encerramento](/imgs/server_termination.png?raw=true "Resultado da sequência de encerramento do servidor")

### 🔋 Estação de Carga

O arquivo .zip da estação possui ```station``` antes de seu número de versão. Para iniciar o programa referente à estação de carga, execute o arquivo ```client.py```, encontrado no diretório principal da aplicação. Ao usuário será pedida a entrada do endereço IP do servidor, seguido do endereço do broker MQTT (porta 1883, entrada vazia para utilizar o broker do servidor conectado), de informações da estação e do ID para cadastro de estação fornecido por um administrador do sistema com acesso ao terminal do servidor. É importante notar que o programa não detecta e não corrige um endereço IP incorreto, sendo necessária a reinicialização para que esse valor seja mudado, em caso de entrada incorreta.

Caso um ID correto falhe em cadastrar, basta repetir a entrada.

Caso seja a primeira vez que a estação foi utilizada, será pedido ao usuário também informações referentes às coordenadas da estação e o preço de seu KWh, os quais deverão ser inseridos como números, possivemente incluindo decimais.

Nota: Utilizar a entrada "test" para o campo de broker MQTT resulta na escolha de um broker de teste pre-definido, por padrão aquele da [EMQX](https://www.emqx.com/en/mqtt/public-mqtt5-broker) (endereço: broker.emqx.io, porta TCP 1883). Ademais, note que não é necessário que um broker MQTT esteja em execução na máquina da estação sob hipótese alguma, visto que a entrada vazia, como dito anteriormente, resulta na utilização de um broker em execução na máquina do servidor conectado.

![Tela inicial](/imgs/station_waiting.png?raw=true "Resultado caso a estação já tenha sido inicializada anteriormente.")

Após tais informações serem fornecidas e em cada inicialização subsequente do programa, o terminal exibirá o ID da estação e o preço unitário de seu KWh.

Quando um veículo agenda com sucesso uma recarga, a estação agendada receberá suas informações em até 1 minuto, inicando o processo de recarga.

![Tela de recarga](/imgs/station_recharge.png?raw=true "Realizando recarga")

Na atual versão de teste do programa, a recarga é feita apenas pressionando a tecla ENTER no terminal da estação.

### 🚘 Veículo (Usuário Final)
Terceiro e último módulo do sistema, a parte referente ao veículo possui ```vehicle``` antes de seu número de versão do arquivo .zip. Para iniciar a aplicação (incluindo janela gráfica), execute o arquivo ```client.py```, encontrado no diretório principal da aplicação. O processo de cadastro de um veículo só requer ao usuário inserir o endereço IP do servidor (e tal entrada só é requisitada no cadastro, sendo "pulada" em execuções seguintes da aplicação). Assim como para a estação de recarga, o programa não detecta e não corrige um endereço IP incorreto, e portanto pode ser necessária a reinicialização do programa caso seja feita uma entrada incorreta.

Em seguida, é perguntado ao usuário o endereço do broker MQTT (porta 1883, entrada vazia para utilizar o broker do servidor conectado).

Nota: Utilizar a entrada "test" para o campo de broker MQTT resulta na escolha de um broker de teste pre-definido, por padrão aquele da [EMQX](https://www.emqx.com/en/mqtt/public-mqtt5-broker) (endereço: broker.emqx.io, porta TCP 1883). Ademais, note que não é necessário que um broker MQTT esteja em execução na máquina do veículo sob hipótese alguma, visto que a entrada vazia, como dito anteriormente, resulta na utilização de um broker em execução na máquina do servidor conectado.

![Terminal Inicial](/imgs/vehicle_waiting.png?raw=true "A aplicação requer o endereço IP do servidor (em caso de cadastro) e uma entrada do broker MQTT (sempre) logo no seu início")

#### TELA PRINCIPAL

Após sua entrada, a aplicação será exibida em janela gráfica (caso trata-se da primeira execução, ou seja, cadastro, será necessário estabelecer conexão com um servidor antes que a aplicação seja exibida. o que resulta na espera de alguns segundos).

A interface gráfica do programa contém informações referentes ao nível de carga do veículo (incluindo aviso caso fique abaixo de 30%) e botões para navegar aos submenus referentes à recarga, realizar reserva em uma rota e visualizar o histórico de compras. Nesta tela também encontra-se um espaço para a entrada do servidor local conectado, o qual responderá todas as requisições do veículo, inclusive aquelas que dependem de respostas de outros servidores. Toda e qualquer mudança nessa caixa de texto será refletida no endereço do servidor que processará as requisições do veículo feitas a partir daquele momento, não importando em qual janela sejam feitas as requisições.

![GUI principal](/imgs/vehicle_gui_main.png?raw=true "Janela principal da aplicação.")

#### MENU DE RECARGA

Pressionar o botão ```ABRIR MENU DE RECARGA``` abre a janela de gerenciamento de recarga. Nesta janela, o usuário pode obter as informações referentes à estação mais próxima e gerar uma guia de pagamento de serviço referente à recarga total do veículo no preço da estação cujas informações estão sendo atualmente exibidas.

![GUI de recarga 1](/imgs/vehicle_gui_recharge_1.png?raw=true "Resultado de uma ação de busca de estação mais-próxima bem-sucedida, seguida de uma ação de geração de guia de pagamento (identificada por UUID) para recarga total em tal estação mais próxima.")

Após realizar o pagamento de acordo com o método desejado, o usuário deve confirmar que efetuou o pagamento pressionando o botão ```RECARREGAR NA ESTAÇÃO SELECIONADA```.

Se entre a busca da estação e a confirmação do pagamento nenhum outro veículo agendar com sucesso o local de recarga, o usuário conseguirá agendar a recarga de seu próprio veículo, cabendo ao software de controle do equipamento da estação de carga verificar o ID do veículo quando este chegar até o ponto e então realizar a recarga.

![GUI de recarga 2](/imgs/vehicle_gui_recharge_2.png?raw=true "Resultado de um agendamento de recarga bem-sucedido")

No entanto, caso outro veículo consiga agendar o local de recarga durante a compra, o usuário em questão será notificado de que não conseguiu agendamento e que sua compra foi automaticamente cancelada (estornada), o que de fato acontece no servidor (é chamada uma função PLACEHOLDER para API de serviço de pagamentos).

![GUI de recarga 3](/imgs/vehicle_gui_recharge_3.png?raw=true "Resultado de um agendamento de recarga mal-sucedido")

#### MENU DE RESERVA

De volta à tela principal da aplicação, o usuário pode abrir o menu de reserva de rotas pressionando o botão ```ABRIR MENU DE RESERVAS```. Utilizando os botões ```<``` e ```>```, encontrados no topo da tela, o usuário pode navegar pela lista de rotas que possuem como destino final o servidor de endereço especificado na caixa de entrada de texto no topo da tela. A rota atual selecionada será exibida como uma lista de siglas para cada cidade que faz parte da rota (menos a cidade de origem, pertencente ao servidor local).

![GUI de rotas 1](/imgs/vehicle_gui_route_1.png?raw=true "Menu de reserva de rotas após uma ação de busca de rota com destino final no servidor de endereço 172.18.0.4")

Logo abaixo dos botões de navegação da lista de rotas, o usuário encontrará uma caixa de entrada de texto destinada à entrada de uma data/horário para cada reserva individual, no formato DD/MM/AAAA-hh:mm.

Ao pressionar os dois botões encontrados abaixo da caixa de texto do horário, o cliente poderá adicionar cada horário a lista de reserva, ou remover o horário adicionado anteriormente à lista. Uma lista com o nome dos locais com horário atualmente selecionados é exibida abaixo dos botões de adicionar ou remover horário, sendo que uma lista de reserva estará completa quando for igual ao retorno da consulta de rotas.

![GUI de rotas 2](/imgs/vehicle_gui_route_2.png?raw=true "Menu de reserva de rotas após serem adicionados dois horários para a rota atual")

Após adicionar todos os horários desejados, o cliente deve pressionar o botão ```REQUISITAR RESERVA NA ROTA```. Caso a requisição seja bem-sucedida, o cliente poderá contar com exclusividade (não-obrigatória) de agendamento de recarga em um dos postos associados a cada servidor do trajeto (respeitando também a autonomia de seu veículo durante todo o trajeto). Caso contrário, nenhum agendamento será feito.

O texto logo abaixo do botão de confirmação de reserva reflete o resultado da requisição. Por questões de conveniência, uma reserva bem-sucedida limpa a lista de horários atuais para uma nova reserva, enquanto que uma mal-sucedida não o faz.

![GUI de rotas 3](/imgs/vehicle_gui_route_3.png?raw=true "Resultado de uma reserva de rota bem-sucedida")

#### HISTÓRICO DE COMPRAS

Novamente a partir da tela principal da aplicação, o usuário poderá abrir o histórico de compras pressionando o botão ```ABRIR HISTÓRICO DE COMPRAS```. Qualquer usuário com ao menos uma compra bem-sucedida realizada pode navegar seu histórico de compras por meio dos botões ```<``` e ```>```. Note que os espaços referentes às informações da compra permanecem vazios até que um dos botões seja pressionado, mesmo após ao menos uma compra ser feita.

Note que as compras estão disponíves para consulta apenas no servidor que processou a operação de compra.

![GUI de compras](/imgs/vehicle_gui_purchases.png?raw=true "Detalhes de uma compra registrada no histórico")

#### IMPORTANTE: Não cabe ao usuário final, por meio da interface gráfica ou do terminal, alterar as informações referentes ao nível da bateria, da autonomia do veículo, de sua posição ou mesmo da capacidade de carga (após o cadastro). Tais informações estão salvas no arquivo ```vehicle_data.json```, presente na pasta ```/vehicledata/``` a partir do diretório principal da aplicação. A aplicação está configurada para monitorar constantemente tal arquivo de configuração e refletir quaisquer mudanças diretamente nas suas variáveis. Assim sendo, é esperado que o arquivo de propriedades seja alterado por softwares terceiros (e não pelo usuário da aplicação, mesmo que isso seja perfeitamente possível e útil em situações de teste), os quais devem fazer uso de sensores que não estão presentes no atual ambiente de desenvolvimento.

# Comunicação por protocolo HTTP-REST e MQTT

## Protocolo MQTT

O protocolo MQTT utiliza da relação de publicação/assinatura para intermediar a comunicação entre clientes através de um broker, este que por sua vez envia a mensagem publicada para todos os assinantes interessados no tópico. No contexto do sistema distribuído o protocolo MQTT é responsável por definir a forma como a comunicação entre cliente e servidor deve ser estabelecida.

As mensagens postadas utilizando o protocolo MQTT são sempre strings sendo necessária a conversão da lista contendo as informações de cada requisição/resposta para strings antes do envio da mensagem. O objeto lista que gera a string da mensagem possui os seguintes elementos:
- Endereço do cliente (string)
- Porta TCP utilizada para conectar-se ao broker MQTT (integer)
- Parâmetros da mensagem de requisição ou resposta (list para requisições, objetos variadas para respostas)

Por sua vez, as listas referentes aos parâmetros das mensagens de requisição possuem o formato:

- ID da requisicao (string) => Identificador passado pelo cliente para determinar se o servidor deve executar uma requisição ou apenas retornar o resultado de uma requisição já concluída.
- nome da requisicao (string): => Sigla que identifica a ação a ser realizada pelo servidor caso a requisição seja válida.
- parâmetros da requisição (lista) => Informação necessária para que o servidor execute uma ação de acordo com uma requisição. Cada requisição possui seus próprios parâmetros.
  - nome da requisição = 'rcs' => parâmetros = [id-da-estação (string), coordenada-x(string), coordenada-y(string), preço-unitário(string)]; Requisição para cadastrar uma nova estação de recarga. Retorna resultado positivo ("OK") ou negativo ("ERR") para a estação.
  - nome da requisição = 'gbv' => parâmetros = [id-da-estação (string)]; Requisição para retornar a uma estação de recarga o veículo atualmente recarregando nela.
  - nome da requisição = 'fcs' => parâmetros = [id-da-estação(string)]; Requisição para liberar uma estação de carga(fim do processo de recarga). Sempre deve retornar "OK" para a estação de recarga.
  - nome da requisição = 'rve' => parâmetros = []; Requisição para registrar um novo veículo. Retorna resultado positivo ("OK") ou negativo ("ERR") para o veículo.
  - nome da requisição = 'nsr' => parâmetros = [coordenada-x-do-veículo(string), coordenada-y-do-veículo(string), autonomia-do-veículo(string)]; Requisição para retornar informações do posto de recarga mais próximo disponível para uso. Retorna uma lista contendo ID da estação, distância e preço unitário do KWh, os quais estarão como "0" caso não encontre estação disponível.
  - nome da requisição = 'bcs' => parâmetros = [id-da-compra(string), id-do-veículo(string), id-da-estação(string), quantidade-paga(string)]; Requisição para tentar realizar (reserva de) abastecimento. Retorna resultado positivo ("OK") ou negativo ("ERR"/"NF") para o veículo.
  - nome da requisição = 'gpr' => parâmetros = [id-do-veículo(string), índice-da-compra(string)]; Requisição para retornar as informações de uma compra em específico). Retorna uma lista contendo ID da compra, valor total em BRL, preço unitário do KWh e quantidade carregada em KWh, em ordem.
  - nome da requisição = 'rwr' => parâmetros = [indíce-da-rota(string), destino-da-rota(string)]; Requisição para retornar informações de uma rota em específico. Retorna uma lista contendo o índice real da rota no banco de dados do servidor e uma lista dos nomes das localidades nas quais os servidores contemplados pela rota estão. O índice e a lista de rota serão vazios caso não encontre
  - nome da requisição = 'rrt' => parâmetros = [id-do-veículo(string), indíce-da-rota(string),tempo-de-reserva(list), autonomia-do-veículo(string), coordenada-x(string), coordenada-y(string)]; Requisição para reservar uma rota.


![mqtt_pub](/imgs/mqtt_pub.png?raw=true "Enviando contendo requisição do veículo com endereço 172.18.0.1 para o broker no endereço 172.18.0.2 utilizando o software de terceiro Mosquitto Client")

![mqtt_sub](/imgs/mqtt_sub.png?raw=true "Recebendo resposta referente a uma requisição do veículo com endereço 172.18.0.1 a partir do broker no endereço 172.18.0.2 utilizando o software de terceiro Mosquitto Client")

## Protocolo HTTP
O protocolo HTTP permite o envio e recebimento de informações através de transferência de hypertexto na WEB.É característico de sua constituição tipagens específicas de requisição como POST ou GET . O mesmo é bastante utilizado na construção de APIs REST (apesar de não ser um requisito para tal). Sua utilização no projeto é conveniente na medida que prevê por padrão um retorno para requisições.

Para realizar uma requisição HTTP o servidor-remetente deve enviar uma requisição do tipo POST com um corpo JSON para a URL http://endereço-do-destinatário:porta/submit. Existem dois tipos de requisições disponíveis para serem feitas aos servidores atuais: realizar reserva e desfazer reserva.

A requisição enviada por meio de protocolo HTTP tem a opção de ser automaticamente convertida para formato JSON, o que acontece automaticamente quando um objeto compatível é designado para o campo JSON da requisição. O objeto lista que representa a string da requisição possui os seguintes elementos:
- Nome da requisição (string)
- Parâmetros da requisição (list)

Por sua vez, as listas referentes aos parâmetros das requisições possuem o formato:

- nome da requisição = 'drr' => parâmetros = [id-do-veículo (string),tempo-de-reserva (float), autonomia-do-veículo (float), coordenada-x (float), coordenada-y (float)]; Requisição para retornar uma lista contendo as coordenadas x e y, caso bem sucedida a ação, após tentar realizar a reserva de qualquer ponto de recarga disponível em um servidor específico.
- nome da requisição = 'urr' => parâmetros = [id-do-veículo (string)]; Requisição para remover um veículo específico que possivelmente está reservado em algum ponto de recarga associado ao servidor que recebeu a requisição.

![http_req](/imgs/http_req_1.png?raw=true "Enviando requisição http para criação de reserva a um servidor utilizando o software de terceiro Insomnia")

# Sincronização com uso de blockchain tipo Ethereum

Para realizar a sincronização entre os diversos servidores conectados dos registros das transações (compras) realizadas, a aplicação do servidor faz uso de blockchain tipo [Ethereum](https://ethereum.org/en/).

É possível operar diretamente sob a lógica básica da blockchain de modo a obter o resultado necessário (sincronização segura de dados) para a aplicação de recarga de veículos. No entanto, tendo em vista seu grande potencial como ferramenta a ser usada em aplicações descentralizadas, o Ethereum implementa o que é conhecido como "contrato inteligente". Um contrato inteligente nada mais é que uma aplicação cujo código, armazenado em uma transação de uma blockchain, é esperado poder ser executado por qualquer computador que faça parte da blockchain e de acordo com instruções enviadas após sua implementação, podendo após sua "chamada" fazer consulta à base de dados da blockchain ou mesmo realizar uma nova transação.

Ainda com o intuito de facilitar o desenvolvimento de aplicações descentralizadas, criou-se a linguagem de [Solidity](https://soliditylang.org/), a qual permite reduzir funções de manipulação de dados normalmente compostas de várias operações sobre a blockchain em simples chamadas de funções CRUD comuns em diversas linguagens de programação, além de associar diversas funções em sequência a uma única chamada de função na interface da aplicação.

![pure_sol](/imgs/sol_bit.png?raw=true "Código solidity para estabelecer o contrato utilizado pela aplicação do servidor.")

Utilizando Solidity, a aplicação atual estabelece um contrato inteligente com as seguintes chamadas:

## adicionarLista(string memory jsonData)

Adiciona um novo elemento à lista utilizada para sincronização. Qualquer objeto capaz de ser transformado em string por meio de serialização json pode ser adicionado.

## obterLista(uint index)

Lê e retorna o elemento da lista (string memory) no índice especificado.

## totalListas()

Avalia o tamanho da lista de sincronização e retorna seu valor em número inteiro (uint)

![python_sol](/imgs/python_bit.png?raw=true "Exemplo, em Python (utilizando web3.py), de chamada remota das funções \"totalListas\" e \"obterLista\"")

# Desenvolvimento com uso de containers por meio de Docker Engine
```console
bash dockerscript.sh ACAO SUBPARAMETRO
```

### Utilize os comandos no terminal Linux executado no diretório `src/` da aplicação e como descrito acima, sendo `ACAO` um paramêtro obrigatório para todas as ações, enquanto que `SUBPARAMETRO` so é utilizado em uma destas.

### > LOADIMAGE carrega uma imagem a partir do arquivo de nome `python-redes-image.tar`, o qual foi baixado e colocado no diretório de desenvolvimento `/src/` (ou seja, juntamente com o arquivo de script), ou ainda, anterioromente salvo pelo comando ```saveimage``` (não recomendado). Também cria a rede necessária para testes.

- Formato fixo:
```console
bash dockerscript.sh loadimage
```

### > RUN instancia os containers para as diferentes versões da aplicação (4 de servidor, 10 de estações e 4 de veículos). Vale lembrar que este comando também resulta na configuração de brokers MQTT Mosquitto Eclipse para funcionar perfeitamente dentro de cada container de servidor.

- Formato fixo:
```console
bash dockerscript.sh run
```

### > STOP apaga os containers instanciados.

- Formato fixo:
```console
bash dockerscript.sh stop
```

### > UPDATE copia os varios arquivos da aplicação para os containers em execução. Pode e deve ser utilizado toda vez que houver alguma mudança nos arquivos da própria aplicacão (para atualizar os arquivos gerados durante a execução da aplicação, utilize o comando `export` como descrito mais abaixo).

- Formato fixo:
```console
bash dockerscript.sh update
```

### > CONTROL Assume o controle do terminal do container especificado no parâmetro `SUBPARAMETRO`, sendo bcm referente ao container da aplicação de estabelecimento de contrato, sv01-sv04 referente a cada um dos quatro containers do servidores, cs01-cs10 referente a cada um dos dez containers das estações, e ev01-ev04 referente a cada um dos dos quatro containers dos veículos.

- Exemplo:
```console
bash dockerscript.sh control cs07
```
#### AVISO: Antes de realizar um acesso remoto a interfaces gráficas (de veículos), certifique-se de a biblioteca "x11 Server Utils" para Linux está na máquina que exibirá tais interfaces, e em seguida habilite a execução remota de programas.
```console
sudo apt-get install x11-xserver-utils -y
```
##### (Instala a biblioteca em sistemas do tipo Linux. O acesso remoto a elementos gráficos de containers por outros tipos de sistemas operacionais NÃO é previsto pelo kit de desenvolvimento deste programa.)
```console
xhost +
```
##### (Habilita a visualização remota de elementos gráficos, deve ser executado sempre que o sistema operacional sofrer reinicialização.)

### > TESTDUMP Copia os varios arquivos de testes encontrados em `src/test_files` para os containers em execução.

- Formato fixo:
```console
bash dockerscript.sh testdump
```
#### AVISO: As rotas de teste possuem endereço IP que muito provavelmente não corresponderão a endereços observados por todos os desenvolvedores. Cabe a cada desenvolvedor mudar os IPs para corresponder àqueles utilizados pelos containers dos servidores, os quais podem ser vistos ao executar a aplicação de cada servidor, e lembrando que nenhum servidor deverá ter seu próprio IP como parte de um nó de qualquer rota.

### > IMPORT Copia os arquivos e/ou diretórios gerados pelas aplicações em execução nos containers para a pasta `/src/files/imported`.

- Formato fixo:
```console
bash dockerscript.sh import
```

### > EXPORT Copia os arquivos da pasta `/src/files/export` para suas respectivas pastas em seus respectivos containers, de acordo com a organização dentro da própria pasta `/src/files/export`.
Para re-inserir arquivos modificados nos containers, certifique-se de que a hierarquia em `/files/export` é a mesma encontrada em `/files/imported`, ou seja, tal como encontrado após o processo de importação.

- Formato fixo:
```console
bash dockerscript.sh export
```

### > CLEARIMPORTED Apaga todos os arquivos atualmente presentes nas várias pastas contidas em `/src/files/imported`.

- Formato fixo:
```console
bash dockerscript.sh clearimported
```

### > CLEAREXPORT Apaga todos os arquivos atualmente presentes nas várias pastas contidas em `/src/files/export`.

- Formato fixo:
```console
bash dockerscript.sh clearexport
```

### > SCRAP Apaga todos os containers, redes e imagens criadas pelas ações `build` e `run`.

- Formato fixo:
```console
bash dockerscript.sh scrap
```

### > BUILD  compila a imagem e cria a rede necessária para testes. Note que a imagem docker segundo o arquivo Dockerfile contém todos os recursos possivelmente utlizados em um ambiente de produção, incluindo um broker MQTT (Mosquitto Eclipse)

- Formato fixo:
```console
bash dockerscript.sh build
```
#### AVISO: Devido à natureza de mudança na versão mais recente e de possível indisponibilidade de versões específicas de aplicações, plugins e APIs, é recomendado ao usuário carregar uma versão da imagem já compilada e testada, como já descrito anteriormente, ao invés de compilar sua própria imagem com o comando `build`. Um link do Google Drive contendo uma imagem pré-compilada e testada está incluso no fim deste documento README.md, sessão "Ferramentas de Desenvolvimento Adicionais".

### > SAVEIMAGE  salva a versão mais recente da imagem local no arquivo python-redes-image.tar.

- Formato fixo:
```console
bash dockerscript.sh saveimage
```

### NOTA: O kit de desenvolvimento inclui um arquivo DOS-batch (dockerscript.bat) com comandos idênticos, exceto aqueles relacionados a interfaces gráficas, os quais estão totalmente ausentes.

# Ferramentas de Densenvolvimento Adicionais

## Imagem Docker
[python-redes-image.tar - Google Drive](https://drive.google.com/file/d/1yu0YU4HwyEMYXltb9l4f3w7dYQ2QfauG/view?usp=sharing)

## Anaconda - gerenciador de ambientes virtuais para Python
[_Installing Anaconda Distribution_]()

## Comandos e Argumentos Especiais

### Broker MQTT de Teste
Como citado anteriormente, utilizar `test` como entrada para o endereço do broker MQTT, quando solicitado, resulta na uso do [broker MQTT pertencente à EMQX](https://www.emqx.com/en/mqtt/public-mqtt5-broker)

### Passagem de parâmetros durante inicialização da aplicação de um veículo
É possível passar parâmetros do veículo durante a execução do comando que inicia a aplicação, sendo que os argumentos passadas diferem caso seja a primeira execução ou não. Caso seja a primeira execução, os parâmetros são, em ordem: capacidade(KWh), Autonomia(Km), nível de bateria (0-1), coordenada x, coordenada y. Caso contrário, os argumentos são apenas: nível de bateria (0-1), coordenada x, coordenada y.

### Formato do Horário para Reserva
O horário para reserva sempre é passado como número para o servidor, sendo este número correspondente à quantidade de segundos passados desde o [EPOCH POSIX](https://www.epoch101.com/), e a aplicação do cliente passará a entrada como número automaticamente caso o texto digitado tenha valor númerico (o que não acontece caso o cliente digite o horário em formato DD/MM/AAAA-hh:mm, o que por sua vez resulta em uma conversão antes do envio).

## Aplicações de Desenvolvimento
O arquivo `data_randomizer.py` encontrado no diretório de desenvolvimento `/src/` pode ser executado para realizar a randomização dos dados de teste (preço do KWh de estação de carga, autonomia de veículo, capacidade de veículo, nível atual de carga de veículo, coordenadas de veículo). Seu funcionamento se dá por distribuição binomial (mais detalhes em comentários em seu código), e os parâmetros de cada distribuição são estabelecidos de tal forma que os valores resultantes acabam por serem parecidos com aqueles observados em situações reais.

# Bibliografia

## 🔧 📚 Paginas web consultadas para instalacao, solucao de problemas e aprendizado:
- **Instalacao do Docker Engine:**
  - [_Install Docker Engine on Ubuntu_](https://docs.docker.com/engine/install/ubuntu)
- **Como resolver problemas ao executar o Docker**:
  - [_Cannot connect to the Docker daemon at unix:/var/run/docker.sock. Is the docker daemon running?_](https://stackoverflow.com/questions/44678725/cannot-connect-to-the-docker-daemon-at-unix-var-run-docker-sock-is-the-docker)
  - [_Is it possible to use docker without sudo?_](https://askubuntu.com/questions/1165877/is-it-possible-to-use-docker-without-sudo)
  - [_can i install customtkinter on linux_](https://www.reddit.com/r/Tkinter/comments/15sqnvx/can_i_install_customtkinter_on_linux/)
  - [_docker \_tkinter.TclError: couldn't connect to display_](https://stackoverflow.com/questions/49169055/docker-tkinter-tclerror-couldnt-connect-to-display/49229627#49229627)
- **Ajuda geral da biblioteca web3 para Python**:
  - [_Troubleshooting_](https://web3py.readthedocs.io/en/stable/troubleshooting.html)
- **Tutoriais e documentação de programação**:
  - [_Docker Containers: IPC using Sockets — Part 2_](https://medium.com/techanic/docker-containers-ipc-using-sockets-part-2-834e8ea00768)
  - [_How to get bash or ssh into a running container in background mode?_](https://askubuntu.com/questions/505506/how-to-get-bash-or-ssh-into-a-running-container-in-background-mode/543057#543057)
  - [MQTT com Python: MQTT e Troca de informações](https://www.youtube.com/watch?v=6zwRG7FQX1k)
  - [O que é uma API REST?](https://www.redhat.com/pt-br/topics/api/what-is-a-rest-api)
  - [_Eclipse Paho™ MQTT Python Client_](https://eclipse.dev/paho/files/paho.mqtt.python/html/index.html)
  - [_MQTT Allow anonymous login_](https://community.home-assistant.io/t/mqtt-allow-anonymous-login/338345)
  - [_http.server — HTTP servers_](https://docs.python.org/dev/library/http.server.html#module-http.server)
  - [_Requests: HTTP for Humans™_](https://requests.readthedocs.io/en/latest/)
  - [_Entry Widgets in CustomTkinter - Tkinter CustomTkinter 3_](https://www.youtube.com/watch?v=mwalgzuEfvw)
  - [_New Top Level Windows - Tkinter CustomTkinter 15_](https://www.youtube.com/watch?v=FyPOqu3akDw)
  - [_Ganache: Installation and Usage with Python_](https://blog.agilephd.com/posts/ganache/)
  - [_Solidity Example: Yacht Rental Smart Contract_](https://blog.agilephd.com/posts/smart_contract_solidity/)
  - [_Decentralized Application (dApp): An Example using Python_](https://blog.agilephd.com/posts/dapp_python_example/)
  - [_Hashing in Python: Using Hashlib Library for Secure Hashing_](https://www.youtube.com/watch?v=i-h0CtKde6w)
## Aplicativos de teste
- **Clientes de protocolo de rede**:
  - [Mosquitto Eclipse](https://mosquitto.org/)
  - [Insomnia](https://insomnia.rest/)
- **Simulador de blockchain tipo Ethereum**:
  - [Ganache](https://archive.trufflesuite.com/ganache/)
