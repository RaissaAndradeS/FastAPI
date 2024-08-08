## Desenvolvimento Web - aula 03

### Web 

Sempre que nos referimos a aplicação web, estamos falando de aplicações que funcionam em rede.

- Dois ou mais dispositivos interconectados.
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

### Modelo padrão da Web

- URL: Localizador Uniforme de Recursos = um endereço de rede pelo qual podemos nos comunicar com um computador na rede.
- HTTP: Um protocolo que especifica como deve ocorrer a comunicação entre dispositivos.
- HTML: A linguagem usada para criar e estruturar páginas na web.

HTTP = Hypertext Transfer Protocol (Protocolo de Transfêrencia de Hipertexto), é o protocolo fundamental na web para a transferência de dados e comunicação entre clientes e servidores. Ele se baseia no modelo de requisição-resposta: onde o cliente faz uma requisição ao servidor, que responde a essa requisição. Essas requisições e respostas são formatadas conforme as regras do protocolo HTTP.

O cabeçalho de uma mensagem HTTP contém metadados essenciais sobre a requisição ou resposta. Alguns elementos comuns que podem ser incluídos no cabeçalho são:

Content-Type: Especifica o tipo de mídia no corpo da mensagem. Por exemplo, Content-Type: application/json indica que o corpo da mensagem está em formato JSON. Ou Content-Type: text/html, para mensagens que contém HTML.
Authorization: Usado para autenticação, como tokens ou credenciais. (veremos mais disso nas aulas seguintes)
Accept: Especifica o tipo de mídia que o cliente aceita, como application/json.
Server: Fornece informações sobre o software do servidor.

### HTTP - verbos 

- GET: utilizado para recuperar recursos. Quando queremos solicitar um dado já existente no servidor.

- POST: deixa criar um novo recurso. Ou seja, envar dados para registrar um novo usuário.

- PUT: atualiza um recurso existente. Ou seja, atualiza as informações de um usuário existente.

- DELETE: exclui um recurso. Ou seja, remove um usuário específico do sistema.

