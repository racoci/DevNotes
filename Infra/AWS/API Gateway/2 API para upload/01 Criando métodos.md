Já temos a API com o método `POST` para salvarmos as imagens dentro do _bucket_.

Mas, e se alguém subir uma imagem com o nome errado, o que acontece? Ou então, se a pessoa subir a imagem antes da hora? Essa é uma situação complicada, alguém terá que entrar no _bucket_, encontrar e apagar a imagem.

Estamos montando nossa API justamente para evitar que alguém tenha que fazer isso no _bucket_ manualmente. Então, melhoraremos a API para podermos deletar um item. Para isso, criaremos um método `DELETE`.

# Criando o método `DELETE`

No navegador, acessamos o "API Gateway > APIs > Recursos - ColecaoDeFotos". Feito isso, na lateral esquerda, na área de Recursos, clicamos em "/{item}".

Após, no centro direito da tela, clicamos no botão chamado "Criar método". Somos encaminhados para uma nova página. Nela, precisamos definir o tipo de método, como queremos apagar uma imagem selecionamos `DELETE`.

Abaixo, precisamos escolher o tipo de integração, ou seja, o que executaremos. Selecionamos "Serviço da AWS", para integrarmos com o `S3`.

No campo referente a **Região da AWS**, selecionamos "us-weast-1" e em **Serviço da AWS** a opção "Simple Storage Service S3", ou seja, o Serviço de Armazenamento Simples.

Em **Subdomínio da AWS** deixamos em branco, pois não temos. O **Método HTTP** selecionamos a opção `DELETE`, seguido do **Tipo de ação**. Nesse caso, selecionamos a opção "Usar a substituição de caminho".

Assim, na **Substituição de caminho**, passaremos o nome do _bucket_ do `S3`, então, "colecaodefotos-leo/{item}". Colocamos entre chaves para podermos fazer a substituição depois.

No campo **Perfil de execução** passaremos a credencial que criamos no IAM, nesse caso "arn:aws:iam::962752222089:role/colecaodefotos-APIgateway-S3".

Em **Cache de credencial**, não precisamos selecionar nenhuma opção, pois nossas credenciais não precisam ficar em cache. Por fim, deixamos marcado a opção "Tempo limite padrão", de 29 segundos.

Feito isso, na lateral inferior direita, clicamos no botão "Criar método". Assim, o método é criado e o encontramos na lateral esquerda da tela.

### Editando a solicitação de integração

Porém, esse método não está completamente pronto. Faremos agora os ajustes necessários. No centro da tela, clicamos na aba "Solicitação de integração". Logo abaixo, clicamos o botão "Editar".

Feito isso, abre a mesma página que criamos o método anteriormente. Porém, ao descer a tela, encontramos outras abas, que ao serem clicadas, possuem novos campos de preenchimento.

Clicamos na aba "Parâmetros de caminho de URL". Você pode estar se perguntando sobre o que é esse parâmetro. Lembra que no campo Substituição de caminho colocamos "colecaodefotos-leo/{item}"? Utilizaremos o parâmetro para substituir o `{item}` pelo que a pessoa usuária colocar quando acessar a API.

Então, no campo Nome, da aba Parâmetro de caminho de URL, colocamos "item". No campo Mapeado de informações, clicamos em "informações", pois é um link clicável.

Feito isso, na lateral direita da tela, abre uma documentação. Ao descermos, encontramos o parâmetro de caminho `method.request.path.param`. Copiamos esse código e colamos no campo Mapeado de informações, mudando o `param` para `item`.No fim da página, clicamos no botão "Salvar". Feito isso, a solicitação de integração está pronta.

Vamos entender um pouco esse caminho. Quando a pessoa cliente manda uma requisição, cai na **solicitação de método**, onde verificamos se ela tem permissão para acessar. Em seguida, vai para **solicitação de integração**, quando entra na parte da AWS.

Essa solicitação de integração acertará toda a requisição para o serviço que enviará. Estamos enviando para o `S3` que vai reconfigurar toda a solicitação. Ele processa, responde e volta na resposta de integração.

Assim, a resposta de integração arruma novamente, conforme a pessoa cliente mandou. Depois, volta na resposta do método, onde colocamos alguns cabeçalhos e informações adicionais, e volta para a pessoa cliente.

### Editando a resposta de integração

Agora, precisamos verificar a resposta de integração. Para isso, clicamos nessa aba e descemos a tela. Se tudo estiver certo, a resposta será o método "200". É isso que queremos.

Abaixo, na seção Mapeamentos de cabeçalho, temos os Modelos de mapeamento definido como "application/json". Vamos verificar como isso está definido no `POST`. PAra isso, na lateral esquerda da tela, clicamos em "POST" e notamos que está definido como `{"mensagem":"Endio com sucesso"}`.

Então, copiamos esse trecho, voltamos para o método "DELETE". Na seção **Padrão - Resposta**, clicamos no botão "Editar". Na nova página, clicamos na aba "Modelos de mapeamento" e no campo "Corpo do modelo", colamos o código da mensagem, mudando para "Deletado com sucesso". Conforme abaixo:

```json
{"mensagem":"Deletado com sucesso"}
```

Feito isso, clicamos no botão "Salvar". Agora, o método `DELETE` está pronto. Percebeu como esse processo foi rápido? Essa é a vantagem do API Gateway.

Em seguida, colocaremos essa API no ar e vamos testá-la. **Até lá!**