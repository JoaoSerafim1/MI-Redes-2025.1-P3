// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ListaCodificada {
    string[] public listaJson;

    function adicionarLista(string memory json) public {
        listaJson.push(json);
    }

    function obterLista(uint index) public view returns (string memory) {
        require(index < listaJson.length, "Indice invalido");
        return listaJson[index];
    }

    function totalListas() public view returns (uint) {
        return listaJson.length;
    }
}
