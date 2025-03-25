Neste momento, já temos toda a API pronta. Fizemos todas as configurações necessárias e adicionamos a documentação. Portanto, é hora de **testar**!

## Testes em produção

Já conhecemos o _endpoint_ `/fotos/{id}`, testamos pelo console da AWS, e conferimos que está funcionando. Nosso objetivo agora é testar no _**Postman**_.

### Testando a API

Com o Postman aberto, vamos copiar o caminho da requisição _POST_ até `/Dev/`, removendo a partir de `bucket`, pois não precisaremos desse trecho.

```plaintext
https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Dev/
```

Feito isso, vamos abrir uma **nova pesquisa**, agora com o método _**GET**_, e colocaremos o endereço copiado na barra de endereços. Nesse caso, precisaremos adicionar `/fotos/1` ao final do endereço. Vamos começar com o ID 1, correspondente à pesquisa que já fizemos e conferimos que funciona.

> **GET** [https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Dev/fotos/1](https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Dev/fotos/1)

Ao clicar em "_Send_", recebemos a seguinte mensagem:

```json
{
    "message": "Missing Authentication Token"
}
```

Além disso, é retornado o status _**403 Forbidden**_. Se retornarmos à _API Gateway_, podemos identificar que faltou **implementar a API**, ou seja, todas as modificações que fizemos no estágio `Dev` estão indisponíveis por enquanto.

### Implementando a API

Para fazer a implementação, basta clicar em "Implantar API" no canto superior direito. Nesse caso, como estamos com uma nova API que todas as pessoas poderão acessar, é interessante criar um novo estágio.

Sendo assim, vamos selecionar a opção "Novo estágio" e definir o **nome** como `Prod`, referente a "produção". Como **descrição** da implantação, colocaremos "Primeira API com Pesquisa".

> Lembre-se de sempre fazer a implementação da API. Caso contrário, você fará modificações na API Gateway e elas não serão refletidas na API.

### Acessando a página da documentação

Uma vez implementada a API no estágio de produção (`Prod`), vamos pegar diretamente os caminhos dos métodos para evitar qualquer tipo de erro. Começaremos pela **documentação**, então vamos copiar a URL de invocação da documentação:

```plaintext
https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/fotos
```

Com o endereço copiado, vamos abrir uma nova guia no navegador e acessar a página da documentação. Na documentação, primeiro temos a consulta pelo **ID** da foto, com o método `GET /fotos/{id}`.

> Consulta pelo ID da foto. Método **GET** `/fotos/{id}`
> 
> **Exemplo:** `fotos/1`

Temos também a consulta por **assunto**:

> Consulta pelo ASSUNTO da foto. Método **GET** `/fotos/assunto`
> 
> **Exemplo:** `fotos/assunto?nome=Capa_Artigo`

Por fim, temos a consulta por **assunto e coleção**, simultaneamente:

> Consulta por ASSUNTO e COLEÇÃO. Método **GET** `/fotos/consulta`
> 
> **Exemplo:** `fotos/consulta?assunto=Capa_Artigo&colecao=Boas_praticas_midias_socials`

### Testando os métodos

Vamos testar todos esses métodos, começando pelo primeiro exemplo: `/fotos/{id}`. Com o Postman aberto novamente, vamos enviar uma requisição **GET** para o caminho `/Prod/fotos/1`.

> **GET** [https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/fotos/1](https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/fotos/1)

Após clicar em "Send", temos a seguinte resposta:

```json
{
    "Count": 1,
    "Items": [
        {
            "assunto": {
                "S": "Capa_Artigo"
            },
            "id": {
                "N": "1"
            },
            "colecao": {
                "S": "BI"
            },
            "descricao": {
                "S": "DataScience"
            }
        }
    ],
    "ScannedCount": 7
}
```

Funcionou conforme esperado. Vamos voltar à documentação e testar o próximo método. Com o caminho `/fotos/assunto` copiado, voltaremos ao Postman e trocaremos o endereço:

> **GET** [https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/fotos/assunto?nome=Capa_Artigo](https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/fotos/assunto?nome=Capa_Artigo)

Nesse caso, foram encontrados os 5 itens necessários. Por fim, testaremos o método com `/fotos/consulta`. Com o caminho copiado da documentação, retornamos ao Postman e trocamos:

> **GET** [https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/fotos/consulta?assunto=Capa_Artigo&colecao=Boas_praticas_midias_socials](https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/fotos/consulta?assunto=Capa_Artigo&colecao=Boas_praticas_midias_socials)

Nesse caso, foi retornado um erro, pois não alteramos o nome da tabela nesse código específico. Para corrigir, basta retornar para a API Gateway, acessar "Recursos > `/fotos/consulta` > GET > Solicitação de integração", e editar o código em "Modelos de mapeamento".

```json
{
    "TableName" : "colecaodefotos-leo",
    "FilterExpression" : "assunto = :v1 AND colecao = :v2",
    "ExpressionAttributeValues" :  {
        ":v1" : { "S" : "$input.params('assunto')" },
        ":v2" : { "S" : "$input.params('colecao')" }
    }
}
```

Após o ajuste, precisamos implementar novamente a API no estágio de produção (`Prod`). Feito isso, podemos retornar ao Postman e enviar mais uma vez a requisição.

> Pode demorar um pouco até funcionar, devido ao cache que deve ser liberado. Nesse caso, basta esperar alguns instantes.

## Conclusão

Com isso, temos a nossa API em funcionamento em todos os endpoints criados. Agora falta apenas mexer na parte de **segurança da API**, pois não queremos que qualquer pessoa possa subir ou apagar imagens!

 [Discutir no Fórum](https://cursos.alura.com.br/forum/curso-amazon-api-gateway-integrando-protegendo-servicos/exercicio-deploy-em-producao/152682/novo)