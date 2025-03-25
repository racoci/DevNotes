Neste momento, já temos a API completamente pronta. No entanto, ainda falta uma parte importante: a **documentação da API**. Onde vamos manter essa documentação?

## Documentação por _mock_

Existem algumas possibilidades. Uma delas é manter a documentação em um repositório do _**GitHub**_, o que, apesar de estar publicamente disponível, não é ideal, pois não está junto à API. A API está na _Amazon_ e a documentação, no GitHub, então não é prático ter essa documentação separada da API.

Também poderíamos colocar a documentação em uma página web, em um **servidor**. Isso é possível, mas criar um servidor inteiro apenas para manter uma página web da documentação parece ser um pouco demais e irá gerar custos, entre outras coisas que não precisamos.

Sendo assim, que tal usar o próprio _**API Gateway**_ para documentar? Sim, isso é possível, então vamos acessar o API Gateway e entender como podemos utilizar essa função que ele oferece.

### Criando um novo método

Primeiramente, precisamos escolher **onde** ficará a documentação. Nesse caso, queremos colocá-la em `/fotos`. Dessa forma, se acessarmos o caminho `/fotos`, aparecerá a documentação. Por outro lado, se acessarmos, por exemplo, `/fotos/{id}`, começaremos a fazer as pesquisas.

Para iniciar, criaremos um método em `/fotos`. Selecionaremos o tipo de método _**GET**_, enquanto o tipo de integração será uma **simulação** (em inglês, _**mock**_). Configuradas essas opções, basta clicar em "Criar método" no canto inferior direito. Com isso, temos o método GET criado com sucesso.

### Editando a resposta de integração

Na sequência, precisamos mexer na **resposta de integração**, visto que a solicitação chegará para a simulação, e a simulação retornará uma resposta que vamos configurar e será a nossa documentação. Sendo assim, na aba "Resposta de integração", vamos editar a resposta padrão.

Nessa resposta, temos o código de status 200, conforme queremos. Em "Modelos de mapeamento", não vamos pegar um modelo `application/json` dessa vez. Nossa documentação é uma documentação HTML, então vamos trocar para `text/html`. Feito isso, podemos seguir para o corpo do modelo.

O corpo do modelo será a página. Para nos ajudar, a equipe de Devs já deixou no GitHub a documentação, no arquivo `Documentação.html`. Com o arquivo aberto, vamos copiá-lo inteiro.

> _`Documentação.html`:_

```html
<html>
    <head>
        <meta charset="utf-8"/>
        <style>
        body {
            color: #333;
            font-family: Sans-serif;
            max-width: 800px;
            margin: auto;
        }
        </style>
    </head>
    <body>
        <h1>Coleção de Fotos API</h1>
        <p>
            A API Coleção de Fotos contem os seguintes recursos:
        </p>
        <p>
            Consulta pelo ID da foto. Metodo <code>GET</code> <code>/fotos/{id}</code>
        </p>
        <pre>
            Exemplo:
            <code>fotos/1</code>
        </pre>
        <p>
            Consulta pelo ASSUNTO da foto. Metodo <code>GET</code> <code>/fotos/assunto</code>
        </p>
        <pre>
            Exemplo:
            <code>fotos/assunto?nome=batman</code>
        </pre>
        <p>
            Consulta por ASSUNTO e COLECAO. Metodo <code>GET</code> <code>/fotos/consulta</code>
        </p>
        <pre>
            Exemplo:
            <code>/fotos/consulta?assunto=batman&colecao=dc</code>
        </pre>
    </body>
</html>
```

Feito isso, podemos voltar para o API Gateway e colar em "Corpo do modelo". Dessa forma, temos todo o código da documentação, que será a nossa página web.

> **Importante:** se você adicionou novos pontos de pesquisa, isto é, novos _endpoints_, adicione-os à documentação. É essencial que a documentação reflita exatamente como a API está.

### Ajustes finais

Com as configurações anteriores salvas, ainda precisamos adicionar mais duas partes importantes. Primeiro, vamos acessar a aba "Resposta do método" e editar "Resposta 200".

Nessa resposta, temos o status HTTP 200, e vamos definir um **nome de cabeçalho**. Para isso, clicamos em "Adicionar cabeçalho" e definimos o nome como `Content-Type`.

> **Importante:** o "C" de "_Content_" e o "T" de "_Type_" **precisam ser maiúsculos**.

Além disso, vamos remover o corpo da resposta. Feito isso, podemos salvar.

Com essa alteração, poderemos mapear o `Content-Type` para a nossa resposta. Assim, não mandaremos apenas texto e o navegador entenderá que aquilo é uma página que deve ser renderizada.

Para mapear, vamos retornar à aba "Resposta de integração" e **editar a resposta padrão** novamente. Agora aparece um novo campo, chamado "Mapeamentos de cabeçalho".

Nesse campo, logo abaixo de "_Mapping value_", colocaremos entre aspas simples exatamente o tipo de conteúdo definido em "Modelos de mapeamento". Assim, teremos `'text-html'`.

Para finalizar, clicar em "Salvar" no canto inferior direito.

## Conclusão

A partir desse momento, já temos nossa documentação pronta. O próximo passo é seguir para os **testes** e conferir se tudo funciona conforme esperado!