Já temos a função Lambda que atualiza o DynamoDB com as informações que chegam dos arquivos do S3. Agora faltam os **gatilhos** dessa função, ou em inglês, os _**triggers**_. Eles servem para "disparar" a função.

## Gatilho de adicionar fotos

Na página da função no Lambda, temos o botão "**Adicionar gatilho**" no fim da seção de Visão geral. Vamos clicar nele.

A primeira informação que essa página pede é uma **origem**, ou seja: de onde virá esse gatilho? No nosso caso, queremos que o S3 avise o Lambda quando aparecer um arquivo novo. Então, selecionamos o **S3** no campo de origem.

Depois, selecionamos o _**bucket**_. Nosso _bucket_ é o `colecaodefotos-leo`. Ele vai verificar se o _bucket_ está na mesma **região** da função do Lambda - nesse caso, "_us-east-1_". Eles precisam estar na mesma região, senão não podemos criar gatilho. Atente-se bem a isso!

Em seguida, configuramos os **tipos de eventos**. Vamos remover o que já tem por padrão, "_All object create events_". Depois, vamos abrir a lista de possíveis eventos. Vamos selecionar eventos do tipo **`PUT`**.

A nossa API está usando o tipo `POST` externamente, mas quando ela fala com o S3, ela converte a requisição para um tipo `PUT`, porque podemos colocar **novos arquivos** dentro do S3.

O próximo campo é para adicionar um **Prefixo**, o que configura a execução da função apenas se criarmos um arquivo em uma pasta específica ou se o arquivo começar com uma palavra específica.

Não vamos usar o prefixo, mas vamos usar o **Sufixo**, que configuraremos no próximo campo. O sufixo funciona de forma parecida, mas considera o final do nome do arquivo. No nosso caso, vamos usar uma extensão como sufixo.

A função só vai ser executada se a extensão do arquivo for `.jpg`. Então, escrevemos ".jpg" nesse campo. Assim, se alguém subir um arquivo de texto, uma imagem com um formato diferente ou um arquivo de backup, a nossa função não vai ser disparada. Ela só vai acontecer se for no arquivo `.jpg`.

Por fim, na seção "_**Recursive invocation**_", temos que marcar a _checkbox_ para confirmar que sabemos não ser recomendado utilizar o mesmo _bucket_ do S3 para tanto ler quanto guardar informações, porque isso pode fazer com que a nossa função seja chamada várias vezes. Após marcar, clicamos em "**Adicionar**" no final da página.

Temos o gatilho para adicionar fotos! Mas, e para quando formos apagar uma foto?

## Gatilho de apagar fotos

Para criar um novo gatilho para a mesma função, podemos apenas descer a página da função no Lambda e clicar em "Adicionar gatilho", como fizemos antes. Mas, vamos seguir outro caminho para conhecer todas as possibilidades.

Para esse outro caminho, vamos à guia do S3. Dentro do nosso _bucket_ "colecaodefotos-leo", vamos clicar na aba "**Propriedades**". Descendo a aba, vamos encontrar a seção "**Notificações de eventos**".

No momento temos uma notificação sendo indicada nessa seção - a que acabamos de criar na função do Lambda. Vamos criar uma nova, clicando em "**Criar notificação de evento**".

Na próxima tela, podemos dar um **nome** para o evento. Pode ser "_deletar imagens_". Ou seja, se deletarmos imagens, esse evento será chamado.

Não precisamos do prefixo, e o sufixo será `.jpg` novamente, para rodar com imagens.

No **tipo de evento**, vamos até a seção de "Remoção de objetos" e marcar a opção "**Excluído permanentemente**". Ou seja, a função será disparada se excluirmos um objeto permanentemente - `s3:ObjectRemoved:Delete`.

Por fim, temos a seção de **Destino**. Vamos marcar a opção "Função do Lambda" e depois "**Escolher entre suas funções do Lambda**" para selecionar uma função existente. No campo de "Função do Lamda" vamos abrir a lista suspensa e selecionar nossa única função: `colecaodefotos-dynamodb-atualizar-leo`.

Podemos **salvar as alterações** clicando no botão do canto inferior direito da página.

Pronto! Temos a nova notificação.

Ambas aparecem na seção "**Notificação de eventos**" do nosso _bucket_ - tanto o evento de inserção de imagens quanto o evento de remoção. Ambas estão funcionando, e ambas estão apontando para a função do Lambda. Ou seja, temos **dois gatilhos** para a função do Lambda!

Agora que a função já está pronta e já temos os gatilhos, vamos **testar**?!