Agora já sabemos que podemos migrar uma aplicação de uma arquitetura de VM, por exemplo, para uma arquitetura Serverless. Contudo, existe uma série de problemas nesse processo. Um deles é a **manutenção do estado**.

Na pasta "api", vamos abrir o arquivo `handlers.js`. Na terceira linha, temos o **mapa**, que salva todos os resultados anteriores na memória. Como cada execução do Serverless é única, toda vez que executamos, perdemos tudo que estava em memória. Não conseguimos passar de uma função para outra o que foi salvo anteriormente.

Para solucionar esse problema, vamos **terceirizar o estado com um banco de dados**. Criaremos um banco no MongoDB e guardaremos esses dados lá. Quando necessário, recuperaremos os estados do banco.

E como faremos esse processo localmente? Nesta aula, focaremos em desenvolvimento e, na próxima aula, em produção. É importante que você tenha lido o material disponibilizado na plataforma antes deste vídeo, pois nele temos as instruções de como preparar o ambiente com a instalação do Docker.

## Criação de contêiner

No terminal, vamos verificar a instalação do Docker com o seguinte comando:

```undefined
docker -v
```

> Docker version 20.10.21, build baeda1f

Na sequência, podemos executar o comando `docker run` seguido do nome do nosso contêiner, que será "sls-mongo". Além disso, usaremos a _flag_ `-d` para desacoplar o contêiner do nosso terminal e `-p` para informar as portas. Tanto localmente quanto dentro do contêiner, mapearemos para a porta 27017. Por fim, definiremos a imagem. No caso, optaremos pela `mvertes/alpine-mongo`, pois ela está instalada numa versão menor do Linux.

**Não vamos executar o comando**, mas ele ficaria assim:

```css
docker run --name sls-mongo -d -p 27017:27017 mvertes/alpine-mongo
```

Toda vez que tivéssemos que criar um banco de dados, teríamos que rodar esse comando extenso, o que não seria muito prático. Vamos resolver esse problema com o Docker Compose.

Voltando ao Visual Studio Code, criaremos um arquivo chamado `docker-compose.yml` na raiz do projeto. Nele, definiremos quais contêineres devem ser criados. Vale lembrar a importância de tomar cuidado com a indentação — em arquivo `.yml`, usa-se dois espaços.

Primeiramente, daremos um nome "database" para nosso serviço. Em seguida, definiremos a imagem e as portas:

```yml
services:
  database:
    image: mvertes/alpine-mongo
    ports:
      - "27017:27017"
```

Após salvar esse arquivo, vamos voltar ao terminal. Na pasta que que criamos o arquivo `docker-compose.yml`, executaremos o seguinte comando:

```undefined
docker compose up -d
```

Assim, subiremos a estrutura, deixando-a desacoplada do terminal, e o Docker criará os recursos necessários. Ao rodar o comando `docker ps`, é possível verificar o contêiner:

```undefined
docker ps
```

## Conexão com o contêiner

Para nos conectar a esse contêiner, usaremos uma extensão do Visual Studio Code chamada **MongoDB for VS Code**. Na lateral da IDE, basta acessar a aba de extensões, pesquisar por MongoDB e instalar a extensão oficial do MongoDB.

Após a instalação, haverá uma nova aba no menu lateral, referente ao MongoDB, com o símbolo de uma folha de árvore. Vamos clicar nela e pressionar o botão "_Add connection_".

Uma nova aba será aberta no editor do VS Code. No topo, temos o título "MongoDB" com uma breve descrição da ferramenta. No canto direito superior, há um link escrito "_Resources_". No corpo da página, inicialmente temos o texto "_Not connected_", com um asterisco vermelho. Em seguida,há dois quadrados dispostos horizontalmente. À direita, está escrito "_Advanced Connection Settings_" seguido do botão "_Open form_". À esquerda, está escrito "_Connect with Connection String_" seguido do botão "_Connect_".

Clicando no botão "_Connect_", um pequeno terminal será aberto no topo do VS Code. Vamos digitar a _connection string_ com o _host_, a porta e o nome do banco de dados:

```bash
mongodb://localhost:27017/alura-serverless
```

Após pressionar "Enter", a frase "_Not connected_" será substituída por "_Connected to:_ locahost:27017". Na aba da extensão, agora consta a seção "localhost:27017". Podemos expandi-la, temos as seguintes opções:

- admin
- config
- local

Conseguimos nos conectar ao banco de dados localmente!

## Conexão de funções

A seguir, vamos explorar como conectar as nossas funções ao banco. Para tanto, vamos editar o arquivo `serverless.yml` novamente, adicionando os _params_ — **parâmetros de funções, que são como variáveis de ambiente**.

Como comentamos anteriormente, o Serverless tem aplicações e, dentro de cada uma delas, podemos ter vários serviços. Uma aplicação pode ter várias variáveis de ambiente padrões que são passadas por todas as funções desse mesmo serviço, de forma que são acessíveis para todos.

Em `serveless.yml`, após a linha em que consta o `frameworkVersion`, vamos pular duas linhas e escrever `params`. Em seguida, vamos colocar `default` e incluir `dbName`, a única de ambiente que não muda entre funções:

```yml
org: khaosdoctor
app: alura-serverless
service: api
frameworkVersion: '3'

params:
  default:
    dbName: alura-serverless

# ...
```

No ambiente `dev`, colocaremos uma variável chamada `connectionString`:

```yml
org: khaosdoctor
app: alura-serverless
service: api
frameworkVersion: '3'

params:
  default:
    dbName: alura-serverless
  dev:
    connectionString: mongodb://localhost:27017/alura-serveless

# ...
```

Note que incluímos o nome do banco de dados na _string_ de conexão. O Serverless conta com um recurso interessante chamado **inflexão**, com o qual podemos referenciar o próprio documento em que estamos para selecionar o valor que está na chave `dbName`. Basta usar o símbolo de cifrão `$` seguido de um par de chaves. Dentro das chaves, colocaremos `self:params.default.dbName`. Trata-se de um _placeholder_:

```yml
org: khaosdoctor
app: alura-serverless
service: api
frameworkVersion: '3'

params:
  default:
    dbName: alura-serverless
  dev:
    connectionString: mongodb://localhost:27017/${self:params.default.dbName}

# ...
```

Por padrão, o Servesless não passa tudo que está em _params_ para a função como variáveis de ambiente. Ele passará somente o que explicitamente definirmos que ele deve passar. Então, ainda no arquivo `serverless.yml`, em `provider`, vamos escrever `environment` e definir as variáveis de ambiente:

```yml
# ...

provider:
  name: aws
  runtime: nodejs14.x
  environment:
    MONGODB_CONNECTIONSTRING: ${param:connectionString}
    MONGODB_DB_NAME: ${param:dbName}

# ...
```

**Como boa prática, usa-se letras maiúsculas para as variáveis de ambiente**. Sendo assim, a primeira variável chama-se `MONGODB_CONNECTIONSTRING` e aponta para a _connection string_ que passamos em _params_. A segunda variável chama-se `MONGODB_DB_NAME` e aponta para o nome do banco de dados definido em _params_.

O próprio Serverless identificará em que ambiente estamos rodando o projeto e quais parâmetros ele deve utilizar. Como não temos um parâmetro `dbName` no ambiente de desenvolvimento, ele usará o `dbName` definido em `default`.

Conseguimos fazer as conexões necessárias, agora vamos trabalhar na função.

## Detalhes no arquivo `handlers.js`

Na pasta "api", vamos abrir o arquivo `handlers.js`. Antes de desenvolver a função, vamos remover tudo que não precisamos mais nesse arquivo.

Vamos remover a constante `previousResults`, dado que não usaremos mais o mapa:

```js
'use strict'
const { randomUUID } = require('crypto')

function extractBody(event) {
  if (!event?.body) {
    return {
      statusCode: 422,
      body: JSON.stringify({ error: 'Missing body' })
    }
  }
  return JSON.parse(event.body)
}

// ...
```

Também apagaremos a constante `resultId`, pois o MongoDB gera um ID automaticamente. Dessa forma, também podemos remover a importação do UUID no início do arquivo:

```js
'use strict'

function extractBody(event) {
  if (!event?.body) {
    return {
      statusCode: 422,
      body: JSON.stringify({ error: 'Missing body' })
    }
  }
  return JSON.parse(event.body)
}

// ...

  const result = {
    name,
    correctAnswers,
    totalAnswers: answers.length
  }

  return {
    statusCode: 201,
    body: JSON.stringify({
      resultId,
      __hypermedia: {
        href: `/results.html`,
        query: { id: resultId }
      }
    }),
    headers: {
      'Content-Type': 'application/json'
    },
  }
}

// ...
```

Além disso, vamos alterar o nome da constante `correctAnswers` para `totalCorrectAnswers`. Ao selecionar a primeira ocorrência do nome `correctAnswers` com o cursor (linha 18), podemos pressionar "Ctrl + D" para também selecionar a segunda ocorrência (linha 27) e renomeá-las de uma única vez:

```js
// ...

const totalCorrectAnswers = answers.reduce((acc, answer, index) => {
    if (answer === correctQuestions[index]) {
        acc++
    }
    return acc
}, 0)

const result = {
    name,
    totalCorrectAnswers,
    totalAnswers: answers.length
}

// ...
```

Vamos adicionar as respostas do aluno em `result` também:

```js
// ...

const result = {
    name,
    answers,
    totalCorrectAnswers,
    totalAnswers: answers.length
}

// ...
```

Para conectar com o MongoDB, precisaremos do Driver do MongoDB. No terminal, vamos executar o seguinte comando:

```css
npm install mongodb@4.12.1
```

Após a instalação, teremos uma nova dependência ao final do arquivo `package.json`:

```json
"dependencies": {
    "mongodb": "^4.12.1"
}
```

## Criação do banco de dados

Agora, podemos começar a trabalhar na criação do banco de dados, no início do arquivo `handlers.js`. Primeiramente, precisamos desenvolver uma função assíncrona, chamada `connectToDataBase()`:

```js
'use strict'

async function connectToDatabase () {

}

// ...
```

Vamos instanciar um novo cliente do MongoDB, passando o nome da nossa _string_ de conexão. Além disso, faremos uma importação no topo do arquivo:

```js
'use strict'
const { MongoClient } = require('mongodb')

async function connectToDatabase() {
    const client = new MongoClient(process.env.MONGODB_CONNECTIONSTRING)
}

// ...
```

Criamos o cliente, agora precisamos conectá-lo. De início, vamos definir a constante `connection`. Em seguida, retornaremos `connection.db()`, passando o nome do banco de dados:

```js
'use strict'
const { MongoClient } = require('mongodb')

async function connectToDatabase() {
    const client = new MongoClient(process.env.MONGODB_CONNECTIONSTRING)
    const connection = await client.connect()
    return connection.db(process.env.MONGODB_DB_NAME)
}

// ...
```

Essas adições bastam para conseguirmos criar e nos conectar ao banco de dados. Agora, podemos começar a utilizá-lo.

## Utilização do banco de dados

Ainda no arquivo `handlers.js`, após gerar os resultados, vamos fazer a conexão:

```js
// ...

const result = {
    name,
    answers,
    totalCorrectAnswers,
    totalAnswers: answers.length
}

const client = await connectToDatabase()

// ...
```

Em seguida, vamos criar uma coleção chamada "results". No MongoDB, coleções são equivalentes a tabelas:

```js
// ...

const result = {
    name,
    answers,
    totalCorrectAnswers,
    totalAnswers: answers.length
}

const client = await connectToDatabase()
const collection = await client.collection('results')

// ...
```

Depois, vamos inserir um resultado no banco de dados com o método `insertOne()`:

```js
// ...

const result = {
    name,
    answers,
    totalCorrectAnswers,
    totalAnswers: answers.length
}

const client = await connectToDatabase()
const collection = await client.collection('results')
const result = await collection.insertOne(result)

// ...
```

O MongoDB será responsável por gerar um ID e o retornará como `insertedId`, então faremos um _destructuring_ com `insertedId`:

```js
// ...

const result = {
    name,
    answers,
    totalCorrectAnswers,
    totalAnswers: answers.length
}

const client = await connectToDatabase()
const collection = await client.collection('results')
const { insertedId } = await collection.insertOne(result)

return {
    statusCode: 201,
    body: JSON.stringify({
      resultId,
      __hypermedia: {
        href: `/results.html`,
        query: { id: resultId }
      }
    }),
    headers: {
      'Content-Type': 'application/json'
    },
  }
}


// ...
```

Por fim, vamos alterar o retorno. Como esperamos o `resultId`, vamos somente adicionar dois pontos e colocar o `insertedId` como valor. Além disso, em vez de `id: resultId`, usaremos `id: insertedId`:

```js
// ...

const result = {
    name,
    answers,
    totalCorrectAnswers,
    totalAnswers: answers.length
}

const client = await connectToDatabase()
const collection = await client.collection('results')
const { insertedId } = await collection.insertOne(result)

return {
    statusCode: 201,
    body: JSON.stringify({
      resultId: insertedId,
      __hypermedia: {
        href: `/results.html`,
        query: { id: insertedId }
      }
    }),
    headers: {
      'Content-Type': 'application/json'
    },
  }
}

// ...
```

A inserção de dados está pronta. A seguir, exploraremos a busca de informações no banco de dados. Atualmente, nosso código está assim:

```js
// ...

module.exports.getResult = async (event) => {
    const result = previousResults.get(event.pathParameters.id)
    if (!result) {
        return {
            statusCode: 404,
            body: JSON.stringify({ error: 'Result not found' }),
            headers: {
                'Content-Type': 'application/json'
            }
        }
    }
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(result)
    }
}
```

Em `getResult`, no `previousResults`, estamos pegando dados do `pathParameters`, o que não é uma boa prática.

Inicialmente, vamos fazer a conexão com o banco de dados novamente:

```js
// ...

module.exports.getResult = async (event) => {
    const client = await connectToDatabase()
    const collection = await client.collection('results')

    const result = previousResults.get(event.pathParameters.id)

// ...
```

Na constante `result`, em vez de fazer o `.get`, vamos usar o método `findOne()` do MongoDB:

```js
// ...

module.exports.getResult = async (event) => {
    const client = await connectToDatabase()
    const collection = await client.collection('results')

    const result = await collection.findOne()

// ...
```

Como parâmetro do `findOne()`, passaremos uma _query_ que é um objeto que define o campo que estamos procurando. No caso, buscaremos pelo campo `_id` do MongoDB e seu valor será um `ObjectId`. Como `ObjectId` faz parte do mongoDB, é preciso fazer a importação correspondente no início do arquivo:

```js
'use strict'
const { MongoClient, ObjectId } = require('mongodb')

// ...

module.exports.getResult = async (event) => {
    const client = await connectToDatabase()
    const collection = await client.collection('results')

    const result = await collection.findOne({
        _id: new ObjectId()
    })

// ...
```

Como parâmetro do `ObjectId`, passaremos os IDs dos parâmetros do _path_:

```js
// ...

module.exports.getResult = async (event) => {
    const client = await connectToDatabase()
    const collection = await client.collection('results')

    const result = await collection.findOne({
        _id: new ObjectId(event.pathParameters.id)
    })

// ...
```

A função pronta ficará assim:

```js
// ...

module.exports.getResult = async (event) => {
    const client = await connectToDatabase()
    const collection = await client.collection('results')

    const result = await collection.findOne({
        _id: new ObjectId(event.pathParameters.id)
    })

    if (!result) {
        return {
            statusCode: 404,
            body: JSON.stringify({ error: 'Result not found' }),
            headers: {
                'Content-Type': 'application/json'
            }
        }
    }
    return {
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(result)
    }
}
// ...
```

## Testes

No terminal, vamos iniciar o Serverless com o seguinte comando:

```undefined
sls offline
```

No VS Code, acessaremos a extensão Thunder Client. Nessa aba, teremos o histórico de requisições realizadas anteriormente. Vamos clicar na opção que corresponde ao POST na URL `localhost:3000/api/results` e pressionar o botão "*Send".

Teremos um resultado semelhante ao seguinte:

> - Status: 201 Created
> - Size: 121 Bytes
> - Time: 240 ms

```json
{
    "resultId": "6395f2176a76eabaf8a1fca5",
    "__hypermedia": {
        "href": "/results.html",
        "query": {
            "id": "6395f2176a76eabaf8a1fca5"
        }
    }
}
```

Temos um `resultId` bem diferente do que tínhamos antes. Para checar se o sistema está funcionando corretamente, vamos copiar esse ID e utilizá-lo para fazer uma requisição GET. Por exemplo:

```bash
http://localhost:3000/api/results/6395f2176a76eabaf8a1fca5
```

No retorno, constará o ID, o nome, as respostas, o total de respostas corretas e o total de respostas:

> - Status: 200 OK
> - Size: 110 Bytes
> - Time: 183 ms

```json
{
    "_id": "6395f2176a76eabaf8a1fca5",
    "name": "Lucas",
    "answers": [
        1,
        2,
        3,
        4
    ],
    "totalCorrectAnswers": 0,
    "totalAnswers": 4
}
```

Na lateral do VS Code, vamos acessar a extensão do MongoDB. Vamos clicar com o botão direito do _mouse_ sobre `localhost:27017` e selecionar "_Refresh_". Agora, temos listado o banco de dados "alura-serverless" também. Expandindo o banco "alura-serverless", temos a coleção "results". Dentro dela, temos o documento que inserimos há pouco.

**Recapitulando:** o Serverless está passando as variáveis de ambiente para dentro do nosso código e nós estamos as usando para conectar em nosso banco de dados.

Existe outras possibilidades, como o DynamoDB da Amazon, mas teríamos a questão do _vendor lock in_ que comentamos anteriormente.

Conseguimos conectar ao banco de dados localmente em ambiente de desenvolvimento. Na sequência, vamos aprender como fazer a publicação.