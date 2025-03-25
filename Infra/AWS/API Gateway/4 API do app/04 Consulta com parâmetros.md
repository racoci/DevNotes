Neste momento, já temos a pesquisa pelo ID implementada. O próximo passo será **implementar os outros métodos**!

## Consulta com parâmetros

### Criando um novo recurso

O próximo tipo a ser implementado será a **pesquisa por assunto**. Para isso, vamos selecionar o recurso `/fotos` e criar um novo recurso chamado `/assunto`. Com isso, teremos o recurso `/fotos/assunto` e podemos fechar o menu lateral esquerdo.

### Adicionando um método

Na sequência, dentro do recurso `/assunto`, precisamos criar o **método _GET_**. Para isso, clicamos em "Criar método" e definimos o tipo de método como GET, que será um **serviço AWS**.

Assim como antes, a **região** será `us-east-1` e o **serviço** será _DynamoDB_. O **subdomínio da AWS** permanecerá vazio, e o **método HTTP**, conforme visto anteriormente, será _POST_.

A **ação** novamente será `Scan`, com "S" maiúsculo. O **perfil de execução** está no _IAM_, então basta copiar e colar no campo "Perfil de execução".

```plaintext
arn:aws:iam::962752222089:role/colecaodefotos-apigateway-dynamodb-leo
```

Da mesma forma, não precisamos de **cache de credenciais**, então mantemos a opção padrão "Não adicionar credenciais de chamador à chave do chave". Por fim, podemos deixar o **tempo limite padrão**.

Para finalizar, basta clicar em "Criar método" no canto inferior direito.

### Adicionando um modelo de mapeamento

Com o método GET de `/assunto` criado, o que precisamos fazer nele? A mesma coisa que fizemos no método anterior: vamos em "Solicitação de integração", clicamos em "Editar", descemos até o final, acessamos "**Modelo de mapeamento**" e clicamos em "Adicionar modelo de mapeamento".

Nesse caso, queremos um modelo do tipo `application/json`. Da mesma forma, o corpo do modelo está no _GitHub_, no arquivo `json de controle.json`, da linha 12 à 19.

> _`json de controle.json`:_

```json
// código omitido

{
    "TableName" : "***** TABLE NAME *****",
    "ProjectionExpression" : "id, descricao, colecao",
    "FilterExpression" : "assunto = :v1",
    "ExpressionAttributeValues" :  {
        ":v1" : { "S" : "$input.params('nome')" }
    }
}

// código omitido
```

Com esse trecho copiado, vamos voltar para o _API Gateway_ e colar em "Corpo do modelo". Novamente, precisamos do nome da tabela para substituir, então vamos ao DynamoDB. Na parte superior da página, basta copiar o nome (`colecaodefotos-leo`). Depois, voltamos para o API Gateway e colamos no código.

```json
{
    "TableName" : "colecaodefotos-leo",
    "ProjectionExpression" : "id, descricao, colecao",
    "FilterExpression" : "assunto = :v1",
    "ExpressionAttributeValues" :  {
        ":v1" : { "S" : "$input.params('nome')" }
    }
}
```

Com isso, temos a pesquisa por assunto implementada. Um ponto importante dessa pesquisa é que temos o filtro por `/assunto`, mas a variável é `nome`. Vamos entender melhor isso quando formos testar todos os métodos criados. Finalizadas as configurações, podemos clicar em "Salvar".

### Testando o novo recurso

Para garantir que funcionou, vamos fechar o menu à esquerda e acessar a área de testes. Agora, em "Strings de consulta", vamos definir o parâmetro 1 (`param1`) como `nome` igual ao valor.

Podemos conferir o valor nas tabelas, conforme os assuntos que já temos. Na coluna `assunto`, vamos copiar `Capa_Artigo`. Feito isso, colaremos em "Strings de consulta" e teremos `nome=Capa_Artigo`. Em seguida, vamos ao final da página e clicaremos em "Teste".

```plaintext
/fotos/assunto - Resultados do teste de método GET
Solicitação
/fotos/assunto?nome=Capa_Artigo

Latência
55

Status
200

Corpo da resposta

{"Count":5,"Items":[{"id":{"N":"3"},"colecao":
{"S":"DesignSystem"},"descricao":{"S":"Design_UX"}},
{"id":{"N":"2"},"colecao":
{"S":"Boas_praticas_midias_socials"},"descricao":
{"S": "Design_UX"}},{"id":{"N":"4"},"colecao":
{"S":"Automatizacao_de_testes"},"descricao":
{"S":"DevOps"}},{"id":{"N":"1"},"colecao":
{"S":"BI"},"descricao":{"S":"DataScience"}},{"id":
{"N":"5"},"colecao":{"S":"JS_Arrays"},"descricao":
{"S":"LATAM"}}], "ScannedCount":7}

(retorno omitido)
```

Como retorno, temos o status 200, seguido do corpo da resposta. Ele encontrou 5 itens dessa vez: o `id` número 3; o número 4; o número 1; e assim por diante. Aparentemente, essa requisição funcionou, então podemos seguir para as próximas.

### Desafio

Há mais corpos de resposta no arquivo `json de controle.json`, os quais deixaremos para você criar. Para isso, disponibilizamos uma atividade extra como guia. Caso queira, você também pode criar novos, ou seja, não é necessário se prender aos que já temos no código.

Observe o que temos, mude alguns parâmetros, e teste. O objetivo é que você **explore e pratique**, para treinar e verificar se funciona como esperado e se consegue fazer as modificações necessárias.

## Conclusão

Na sequência, trabalharemos na **documentação da API**!