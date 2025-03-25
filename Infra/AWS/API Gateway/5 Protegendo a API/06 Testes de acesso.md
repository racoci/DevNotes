Completamos a API e inserimos a chave de acesso para garantir a segurança dela e realizamos o _deploy_. Nesse vídeo, vamos testar e verificar se a chave de acesso realmente está funcionando e se está bloqueando o acesso apenas na parte administrativa, onde as pessoas desenvolvedoras estão. Vamos lá!

## Testando a Chave da API

Vamos abrir o _Postman_ e testar. Primeiramente, já que estamos com o `GET` na parte pública, vamos testar essa parte para ver se está precisando da chave. Vamos clicar em "Send" e enviar a solicitação.

Nos resultados, como podemos ver, temos tudo normal. A parte pública está funcionando.

Vamos para a parte privada, selecionando a guia do "DELETE" que tínhamos criado antes, clicando nela na parte superior da tela. Em seu interior, lembraremos de trocar o ambiente de `Dev` para `Prod` (Produção).

Vamos tentar apagar a imagem número 1, enviando o `DELETE` ao _endpoint_ abaixo.

```plaintext
https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/bucket/1-Capa_Artigo-BI-DataScience.jpg
```

Ao enviar essa solicitação, recebemos a mensagem "forbidden" (proibido), indicando que não temos credenciais para realizar essa ação.

```javascript
{
    "message": "Forbidden"
}
```

Como podemos utilizar essa chave de API? Vamos focar nas guias logo abaixo do campo de requisição, acima parte do retorno, onde temos a guia "Params" (parâmetros) selecionada. À direita dela, temos as guias "Authorization" e "Headers". No nosso caso, vamos selecionar diretamente a "Headers".

Em seu interior, na parte inferior, temos os campo "key", à esquerda, e "Value", à direita, que representam um par chave-valor para entrar. A chave que temos é "x-api-key", que é a chave de API. Vamos digitar esse nome no campo "Key" e selecionar a sugestão da página apresentada na lista suspensa.

```plaintext
x-api-key
```

E qual é o valor dessa chave? Vamos conferir na página da AWS.

No interior da tela da _API Gateway_, no menu lateral, vamos descer e selecionar "Chaves de API". Na tela central, temos a tabela com o nome "colecaodefotos-administrativa" e, no canto direito, o campo "Chave de API" que exibe um conteúdo oculto, exibido em forma de pontos. Basta clicar no ícone de copiar, acima desse conteúdo oculto, e já teremos a chave.

Voltando para o _Postman_, na guia do `DELETE`, vamos inserir a chave no campo vazio à direita da chave "x-api-key". Como podemos ver após colar, se trata de uma chave grande, com muitos caracteres aleatórios, então não precisamos nos preocupar.

Agora, vamos tentar enviar a solicitação, clicando em "Send". Na aba inferior, veremos que ele retornou "deletado com sucesso". Então, funcionou.

```javascript
{
    "message": "Deletado com sucesso"
}
```

Vamos verificar se o `POST` também está assim. Vamos acessar a guia do `POST`, à esquerda do `DELETE`.

Em seu interior, faremos a requisição — lembrando de substituir o trecho `Dev` por `Prod` — para subir a mesma imagem que deletamos.

```plaintext
https://suzeltfq41.execute-api.us-east-1.amazonaws.com/Prod/bucket/1-Capa_Artigo-BI-DataScience.jpg
```

Na guia "Headers", desceremos até o final, entraremos no campo "Key" para adicionar uma nova `x-api-key`, e no campo "Value", à direita, inserir a chave.

Após esse processo, ao enviar essa requisição clicando em "Send", veremos na área de retorno que a solicitação foi enviada com sucesso.

```javascript
{
    "message": "Envio com sucesso"
}
```

Podemos concluir que todo o processo da API está funcionando e chave de segurança está protegendo.

> **Importante** Não adianta ter duas chaves de segurança — por exemplo, uma para a parte administrativa e outra para a parte pública — se quisermos controlar as pessoas usuárias. Isso porque a chave de segurança, uma vez criada, será válida na API de forma geral.
> 
> Não é possível definir que a chave de segurança administrativa seja válida para alguns métodos, e a chave de segurança pública para outros. Não há essa separação.
> 
> Se precisar fazer essa separação, divida sua API em dois projetos separados no _API Gateway_, assim você conseguirá colocar uma chave para cada um.

A última coisa que precisamos ver agora é como exportar essa API, para podermos criar um backup dela. Vamos lá?