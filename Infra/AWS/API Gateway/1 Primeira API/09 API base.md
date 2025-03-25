Neste momento, já criamos o _bucket_ do S3 para armazenar todas as nossas imagens e também já definimos as permissões da nossa API. Então, vamos criar a nossa API agora?

## Conhecendo a API base

Primeiramente, para evitar muito trabalho, vamos importar uma API já existente. A equipe de desenvolvimento da nossa empresa criou uma **API base**, já com algumas informações do que ela vai precisar. Mas, como é uma API base, vamos ter que ajustar alguns detalhes.

Vamos acessar o [repositório do GitHub](https://github.com/leollo98/3630-API_Gateway/tree/Projeto_inicial), cujo link foi disponibilizado em uma atividade, e conferir essa API base no arquivo `API inicial.yaml`.

A primeira informação é que ela está escrita numa linguagem de `swagger`, uma linguagem para descrever APIs RESTful, versão `2.0`. O nome dessa API é `ColecaoDeFotos`.

É uma API que funciona em cima de HTTP, e ela já tem um _endpoint_, ou seja, já tem um caminho que podemos acessar, que é o `/bucket/{item}`. E dentro dele, temos o método `post` para poder enviar nossas imagens.

> `API inicial.yaml`:

```yaml
---
swagger: "2.0"
info:
  version: "v1.0"
  title: "ColecaoDeFotos"
schemes:
- "https"
paths:
  /bucket/{item}:
    post:
      produces:
      - "application/json"
      parameters:
      - name: "Content-Type"
        in: "header"
        required: true
        type: "string"
      - name: "item"
        in: "path"
        required: true
        type: "string"
      responses:
        200:
          description: "200 response"
          schema:
            $ref: "#/definitions/Empty"
      x-amazon-apigateway-integration:
        credentials: "***** ARN DA ROLE *****"
        uri: "arn:aws:apigateway:us-east-1:s3:path/***** NOME DO BUCKET *****/{item}"
        responses:
          default:
            statusCode: "200"
            responseTemplates:
              application/json: "{\"messagem\":\"Envio com sucesso\"}"
        requestParameters:
          integration.request.path.item: "method.request.path.item"
        passthroughBehavior: "when_no_match"
        httpMethod: "PUT"
        contentHandling: "CONVERT_TO_BINARY"
        type: "aws"
definitions:
  Empty:
    type: "object"
    title: "Empty Schema"
x-amazon-apigateway-binary-media-types:
- "image/jpeg"
```

Mas existem algumas partes importante que vamos precisar ajustar. Nesse curso, sempre que tiver cinco asteriscos seguidos (`*****`), é algo que precisamos alterar.

Precisamos alterar as **credenciais** (`credentials`), que é o ARN da _role_ que acabamos de criar, que a AWS chamada de função ou perfil.

Na linha 29, em `uri`, também temos um ARN. É um ARN do _bucket_, mas não é exatamente o que está na AWS. Nesse caso, vamos apenas substituir o nome do bucket.

> **Atenção**: se você criou o bucket em outra região, que não é a `us-east-1`, também é necessário substitui-la na `uri`.

## Importando a API

Como podemos fazer para importar essa API na AWS? Vamos copiar o código completo da API, inclusive os três hifens do início, pois eles são necessários.

Vamos voltar no console da AWS e pesquisar por "API Gateway". Ao descer a página, estaremos na parte de criar uma API já que ainda não temos nenhuma.

Devemos escolher o **tipo de API** entre API HTTP, API WebSocket, API REST ou API REST privada. No nosso caso, clicamos em "Importar" uma **API REST**.

Após carregar uma tela nova, vamos manter selecionada a opção de "importar API". No campo logo abaixo, vamos colar o código de definição da API.

Agora, o que precisamos fazer? Trocar a credencial.

> Lembre-se sempre de usar as guias do navegador, uma para cada serviço, isso vai facilitar muito o seu processo dentro da AWS.

Voltamos na parte de funções do IAM. Na função `colecaodefotos-APIgateway-S3`, podemos copiar o ARN da função. Feito isso, podemos voltar para o API Gateway e colar na área de `credentials`, que são as credenciais.

E o quem mais está faltando? O nome do _bucket_. Vamos acessar o _bucket_ do S3 para copiar o nome dele, `colecaodefotos-leo`. No API Gateway, devemos colar o nome do _bucket_ no caminho do ARN na linha 29, em `uri`.

Com essas modificações feitas, podemos escolher o **tipo de endpoint da API**, que pode ser regional, otimizado para borda ou privado. Vamos manter o **regional**, pois ele funciona muito bem. Como faremos mais ajustes depois, o regional vai evitar problemas.

Por fim, o que são **avisos**? Na hora que o API Gateway for tentar importar nossa API, ele pode lançar avisos e erros. Se tiver algo escrito errado, ele vai lançar um erro. Se você esqueceu de colocar o nome do _bucket_ ou a credencial, ele vai lançar um aviso.

Vamos manter a opção "falhar nos avisos", porque queremos que ele falhe se ler algum tipo de aviso e nos mostre onde falhou.

Na parte inferior, podemos clicar em "Criar API".

> Êxito ao criar REST API 'ColecaoDeFotos(suzeltfq41)'

Neste momento, a API já foi importada. Na página de "recursos" dessa API, já temos o `/bucket` e `/{item}` com o método POST.

## Próximos passos

Já temos a nossa API importada na API REST. Contudo, a nossa API ainda não está completa.

O que acontece se alguém subir uma imagem errada na nossa API? Teríamos que entrar no S3 e apagar, mas a ideia da API é não precisar entrar no S3. Vamos arrumar isso a seguir.