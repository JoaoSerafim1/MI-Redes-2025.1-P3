#Base Image
FROM python:3.9-slim

#Main work directory
WORKDIR /python_redes


#Atualizar pacotes
RUN apt-get update -y

#Install pip
RUN apt-get install -y python3-pip

#Install fontconfig
RUN apt-get install -y fontconfig

# Install Tkinter
RUN apt-get install -y tk
# Install CustomTkinter
RUN pip install customtkinter

#Install Paho MQTT
RUN pip install paho-mqtt

#Install requests
RUN pip install requests

#Install web3
RUN pip install web3

#Install solc-x
RUN pip install py-solc-x

#Install npm
#RUN apt-get install -y npm

#Install Ganache
#RUN npm install -g -y ganache

#Install Mosquitto Broker and Client
RUN apt-get upgrade -y && \
    apt-get install -y mosquitto && \
    apt-get install -y mosquitto-clients


#Expose Ports
EXPOSE 1883
EXPOSE 7545
EXPOSE 8001
EXPOSE 8002
EXPOSE 8025
EXPOSE 8545