Agora que já temos todos os dados das fotos no banco de dados, podemos começar a implementar a parte de **consulta**, isto é, a parte de **pesquisa** da nossa API. Por onde começaremos a implementar? Por qual campo vamos iniciar?

## Consulta por ID

Existem vários campos: ID (`id`), assunto (`assunto`), coleção (`colecao`), e descrição (`descricao`). Sugerimos começar pelo **ID**, pois além de ser o primeiro campo que temos, ele é um número único e, provavelmente, será o mais utilizado na hora de obter informações sobre alguma imagem.

### Criando um novo recurso

Para começar, vamos acessar o _API Gateway_ e **criar um novo recurso**, um novo método. Para isso, clicamos em "Recursos" no menu lateral esquerdo. Com a tela de recursos aberta, podemos fechar o menu à esquerda para ganharmos um pouco mais de área para trabalhar.

Agora precisamos criar o recurso, o que será feito no início da API, ou seja, em `/`. Para criar, clicamos em "Criar recurso". Chamaremos o recurso de `fotos`; assim, teremos `/fotos`.

Com o recurso criado, precisaremos criar um **novo recurso** dentro dele para conseguirmos obter informações através do ID. Nesse caso, faremos no mesmo estilo de `/{item}`.

Dito isso, vamos clicar em "Criar recurso" novamente e definir o nome como `{id}`. Uma vez criado o segundo recurso, precisamos adicionar um **método** dentro dele.

### Adicionando um método

Dessa vez, vamos à seção "Métodos", clicamos em "Criar método", e selecionamos o tipo de método **GET**, pois queremos obter informações, e não colocar imagens ou apagar informações.

Primeiramente, vamos integrar esse método como "Serviço da AWS". Em seguida, a **região da AWS** em que subimos tudo é a `us-east-1`, então selecionamos essa opção logo abaixo.

Quanto ao **serviço da AWS**, poderíamos acessar o S3 e ler todas as informações, mas para adiantar, já colocamos tudo no _DynamoDB_, então selecionaremos este serviço.

Qual **método HTTP** o DynamoDB recebe? No nosso caso, faremos uma consulta ao DynamoDB. Ao fazer isso, ele usa o método **POST**. Dessa forma, o cliente manda para nós o método GET para obter a informação, e nos conectamos ao DynamoDB através de um método POST.

Depois, essa informação irá voltar e devolveremos para o cliente. Quem acessa a nossa API não precisa saber que esse método é POST. Por isso, ele pode usar o GET, que é o método mais comum.

Como **tipo de ação**, vamos selecionar a opção "Usar o nome da ação". Porém, quais são as ações que o DynamoDB utiliza? Para descobrir, vamos fazer uma breve pesquisa.

Em uma nova guia no navegador, vamos pesquisar por "DynamoDB API" e acessar o primeiro link ([API do DynamoDB](https://docs.aws.amazon.com/pt_br/amazondynamodb/latest/developerguide/HowItWorks.API.html)) para conferir na documentação qual API o DynamoDB fornece.

Existem algumas áreas na documentação da API: primeiro, temos a parte de "Ambiente de gerenciamento", que não precisaremos no momento; e na sequência, a parte de "[Plano de dados](https://docs.aws.amazon.com/pt_br/amazondynamodb/latest/developerguide/HowItWorks.API.html#HowItWorks.API.DataPlane)", onde encontramos a seção "**APIs clássicas**" na qual iremos trabalhar.

Nessa seção, encontramos primeiro a parte de criar dados. Nesse caso, não queremos criar, mas sim ler, então acessaremos logo abaixo a parte de "**Leitura de dados**". Há algumas opções disponíveis de leitura:

> - `GetItem`;
> - `BatchGetItem`;
> - `Query`;
> - `Scan`.

Usaremos a opção `Scan`. Vamos entender o que ela faz?

> `Scan`: recupera todos os itens na tabela ou no índice especificado. É possível recuperar itens inteiros, ou apenas um subconjunto dos seus atributos. Opcionalmente, você pode aplicar uma condição de filtragem para retornar apenas os valores de interesse e descartar o restante.
> 
> (Fonte: [Documentação da API do DynamoDB](https://docs.aws.amazon.com/pt_br/amazondynamodb/latest/developerguide/HowItWorks.API.html))

É justamente o que queremos: recuperar todos os itens ou filtrá-los através de um subconjunto de atributos. No caso, o **ID** é o atributo pelo qual iremos filtrar.

Dito isso, vamos retornar ao API Gateway e definir o nome da ação como `Scan`, com "S" maiúsculo. Precisamos ter atenção a isso, pois as ações têm diferença entre minúsculos e maiúsculos.

Qual será o **perfil de execução**? Precisamos ter as permissões de um perfil, o qual já criamos antes. Sendo assim, vamos acessar o IAM (_Identity and Access Management_) e analisar os perfis que temos.

Na página "Funções", vamos pesquisar pelo nome da função digitando "colecao". Feito isso, encontraremos a função `colecaodefotos-apigateway-dynamodb-leo`. Após clicar nela, vamos copiar o ARN:

```plaintext
arn:aws:iam::962752222089:role/colecaodefotos-apigateway-dynamodb-leo
```

Com o ARN copiado, vamos voltar para o API Gateway e colar em "Perfil de execução". Com isso, temos o perfil de execução configurado.

Para finalizar, podemos manter a opção "Não adicionar credenciais de chamador à chave do chave" em "**Cache de credenciais**", além de manter o **tempo limite padrão**.

Com todas as opções configuradas, podemos clicar em "Criar método" no canto inferior direito. Ao fazer isso, surgirá um _pop-up_ com a mensagem "Método 'GET' criado com êxito em '{id}'".

### Adicionando um modelo de mapeamento

Para conseguir utilizar o método criado, precisamos acessar a aba "**Solicitação de integração**" e converter o ID que vem na URL (`{id}`) para algo que o DynamoDB possa utilizar.

Para ajudar nessa conversão, a equipe de Devs já fez uma parte de código. Nesse caso, precisaremos mexer apenas no **modelo de mapeamento**. Portanto, na seção "Configurações de solicitação de integração", vamos clicar em "Editar" e acessar a categoria "Modelos de mapeamento".

Nessa categoria, clicaremos em "Adicionar modelo de mapeamento". Primeiramente, queremos um conteúdo do tipo `application/json`. Em seguida, qual modelo vamos utilizar?

O modelo que vamos utilizar já está no repositório do _GitHub_, no arquivo `json de controle.json`, então vamos acessá-lo. O que queremos em relação ao `id` é o primeiro trecho JSON do código, que vai da linha 1 à linha 7, contém a entrada de parâmetro `id`, e irá filtrar pela expressão `id`.

> _`json de controle.json`:_

```json
{
    "TableName" : "***** TABLE NAME *****",
    "FilterExpression" : "id = :v1",
    "ExpressionAttributeValues" :  {
        ":v1" : { "N" : "$input.params('id')" }
    }
}

// código omitido
```

> Observe que o código deixa avisado que precisamos preencher o nome da tabela. No lugar dos asteriscos envolvendo o texto "TABLE NAME", colocaremos o nome da tabela de fato.

Com o código copiado, vamos voltar para o API Gateway e colar esse trecho em "**Corpo do modelo**". Feito isso, vamos pegar o nome da tabela no DynamoDB. Se errarmos o nome da tabela, ele retornará vários tipos de erro. Além disso, o nome da tabela também é sensível a maiúsculas e minúsculas.

Após copiar o nome da tabela (`colecaodefotos-leo`), podemos voltar para o API Gateway e substituir na linha 2 do código. Ao final, teremos o seguinte resultado:

```json
{
    "TableName" : "colecaodefotos-leo",
    "FilterExpression" : "id = :v1",
    "ExpressionAttributeValues" :  {
        ":v1" : { "N" : "$input.params('id')" }
    }
}
```

Feita a substituição, basta clicar em "Salvar" no canto inferior direito da página. Nesse momento, já devemos ter a pesquisa por ID em funcionamento. Vamos testar?

### Testando o novo recurso

Por enquanto, faremos o teste sem implementar a API. Como podemos fazer isso? Junto às abas "Solicitação de método", "Solicitação de integração", "Resposta de integração" e "Resposta do método", encontramos ao final a aba "Teste". Vamos acessá-la para testar.

Nesse caso, testaremos o `id` de valor 1, então basta digitar "1" e clicar em "Teste" na parte inferior. Como retorno, ele traz: a latência, ou seja, o tempo que demorou; o status 200; o corpo da resposta; e os cabeçalhos de resposta.

```plaintext
/fotos/{id} - Resultados do teste de método GET
Solicitação /fotos/1

Latência
61

Status
200

Corpo da resposta

{"Count":1,"Items":[{"assunto":
{"S":"Capa_Artigo"},"id":{"N":"1"},"colecao":
{"S","BI"},"descricao":
{"S":"DataScience"}}],"ScannedCount":7}

(retorno omitido)
```

Ele conseguiu passar por tudo, filtrar as informações do DynamoDB, e trazer somente o que precisávamos, conforme esperado.

## Conclusão

Na sequência, vamos **implementar as próximas consultas**!