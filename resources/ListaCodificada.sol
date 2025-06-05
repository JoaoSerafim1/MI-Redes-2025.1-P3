// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ListaCodificada {
    string[] private listaJson;

    event ListaAdicionada(string jsonData);

    function adicionarLista(string memory jsonData) public {
        listaJson.push(jsonData);
        emit ListaAdicionada(jsonData);
    }

    function obterLista(uint index) public view returns (string memory) {
        require(index < listaJson.length,'indice invalido');
        return listaJson[index];
    }

    function totalListas() public view returns (uint) {
        return listaJson.length;
    }
}
