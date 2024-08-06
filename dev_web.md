## Desenvolvimento Web - aula 03

### Web 

Sempre que nos referimos a aplicação web, estamos falando de aplicações que funcionam em rede.

- Dois ou mias dispositivos interconectados.
- Local (LAN): como em sua casa ou em uma empresa.
- Longa distância (WAN): Como diversos roteadores interconectados.
- Mundial: como a própria internet 

A ideia é a comunicação entre esses dispositivos.

### Cliente - Servidor 

Nesse modelo, temos clientes, como aplicativos móveis, terminais de comando, navegadores, etc., acessando recursos fornecidos por outro computador, conhecido como servidor.

Exemplo do restaurante, cliente chama o garçom que faz o pedido na cozinha e depois serve para você. 

Precisa de uma aplicação que esta sendo servida por alguém (uvicorn) nesse caso, e por esse servidor que estamos mandando algumas requisições, ele emite algumas respostas pra gente.

<center> Cliente <--> Servidor <--> Aplicação Python </center> <br>

O Uvicorn é um "servidor de aplicação", ASGI.  

<center>Cliente <-Requisita-> Uvicorn <-Repassa-> Aplicação Python </center>

### Rede local 
Até o momento era o "loopback", o nosso pc é o cliente e o servidor ao mesmo tempo. 