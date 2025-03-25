Já temos a nossa função Lambda teoricamente funcionando e com os disparadores. Mas, que tal **testar** para verificar se ela realmente está funcionando?

## Teste do disparo da função

Podemos fazer esse teste realizando o upload de uma imagem no S3 e verificando se a função é disparada.

Para isso, vamos abrir o Postman e abrir a aba do POST que criamos anteriormente, que já contém a imagem no Body (corpo da requisição), chamada `1-Capa_Artigo-BI-DataScience.jpg`, e já tem o local da imagem na URL da requisição. Vamos enviar clicando em "**Send**" no canto superior direito da tela. A envio foi feito com sucesso!

Vamos verificar se a imagem apareceu no _bucket_ do S3. Na guia do S3, já no nosso _bucket_ "_colecaodefotos-leo_", clicamos na aba "**Objetos**" e no botão de **Atualizar**. Temos um novo objeto chamado `1-Capa_Artigo-BI-DataScience.jpg`. Correto!

Como a função Lambda escreve essas informações do objeto no DynamoDB, vamos consultar os itens contidos no nosso DynamoDB.

Na guia do DynamoDB, na página da tabela "_colecaodefotos-leo_", vamos clicar em "**Explorar itens da tabela**", na parte superior direita da tela.

Na seção "Verificar ou consultar itens", vamos selecionar a opção "**Verificar**". No campo da tabela deixamos "_colecaodefotos-leo_", e no campo de atributos selecionamos "Todos os atributos", depois clicamos em "Executar".

Temos zero itens retornados no DynamoDB. Então, a nossa função **não funcionou**.

O que aconteceu? Por que ela não funcionou? Porque não demos **permissão** para isso. Vamos para o IAM para configurar essa permissão.

## Configurando a permissão

No console do IAM, vamos entrar em "Gerenciamento de acesso > **Funções**" e pesquisar pelo nome da nossa aplicação.

Com esse nome, temos a função "colecaodefotos-apigateway-dynamodb-leo", que criamos há pouco, "colecaodefotos-APIgateway-S3", que também criamos anteriormente, e uma função chamada "colecaodefotos-dynamodb-atualizar-leo-role-035rvs4v".

Essa última função foi **criada automaticamente** pelo Lambda. No entanto, se entrarmos nela, notaremos que ela não tem a política de acesso para o DynamoDB.

Vamos criar essa política e anexá-la.

### Criando a política

No menu esquerdo do IAM, clicamos em "**Políticas > Criar Política**". Qual serviço queremos acessar? Queremos acessar o DynamoDB.

Quais ações queremos permitir? A nossa função tem que ler, gravar, fazer várias coisas diferentes. Vamos dar permissões para todas as ações do DynamoDB dentro da nossa tabela (não no DynamoDB inteiro).

Sendo assim, marcamos a opção "**Todas as ações do DynamoDB**" e, na seção de "Recursos", selecionamos a opção "**Específico**". Vamos descer até achar a opção `table` e clicamos em "**Adicionar ARN**".

Vamos voltar ao DynamoDB e pegar o ARN da nossa tabela "colecaodefotos-leo". Para isso, vamos para a guia do DynamoDB e clicamos em "Tabelas" no menu esquerdo. Entramos na tabela "colecaodefotos-leo" e, em Visão Geral, descemos a aba até "Informações Gerais > **Informações Adicionais**". O último item é o _Nome de Recurso da Amazon_.

Vamos copiar o ARN, voltar para o IAM e colá-lo no campo "ARN do Recurso". Podemos adicionar clicar em "**Adicionar ARN**" e pronto, já temos a tabela fixada!

Vamos clicar em "**Próximo**" na página de criação de política. Na próxima tela, daremos o **nome da política** seguindo o padrão de sempre. _Coleção de Fotos_, que é o nome da aplicação, e acesso ao DynamoDB. Depois indicamos que isso é uma política adicionando a palavra "_policy_" na frente. Então: "_colecaodefotos-dynamodb-policy_". Copiamos o nome e colamos no campo de descrição também.

Por fim, descemos a página e clicamos em "**Criar Política**". Política criada!

### Anexando a política

Vamos voltar nas Funções, na guia do IAM, e pesquisar pelo nome da nossa aplicação: "colecaodefotos". Vamos localizar a função que tem o mesmo nome da nossa função do Lambd: "_colecaodefotos-dynamodb-atualizar-leo-role-035rvs4v_". Clicamos nela.

Vamos descer até a seção de "Políticas de permissões" e clicar em "**Adicionar permissões > Anexar políticas**". Vamos buscar pela política completa, que acabamos de criar, a "_colecaodefotos-dynamodb-policy_", selecioná-la e clicar em "**Adicionar permissões**". Pronto!

## Novo teste do disparo da função

Primeiro, vamos apagar a imagem que enviamos anteriormente. No Postman, clicamos na aba "DELETE", que teoricamente já está pronta também, e enviar essa requisição clicando em "_Send_". Imagem apagada com sucesso!

Vamos verificar se ela realmente foi apagada no S3. No Console da S3, clicamos para atualizar a aba "**Objetos**". Temos zero imagens no banco!

Vamos enviáar a imagem de novo. No Postman, abrimos a aba "POST" e clicamos em "_Send_". Imagem enviada com sucesso!

Vamos verificar se deu certo. Novamente na aba Objetos do S3, clicamos para atualizar. Temos um objeto! É a imagem que acabamos de enviar.

Agora vamos verificar se aa nossa tabela do DynamoDB contém a imagem. Na guia do DynamoDB, clicamos em "Tabelas > colecaodefotos-leo > Explorar itens da tabela > Verificar > Executar".

Temos uma imagem nos itens retornados, com ID nº1, assunto "Capa_Artigo", coleção "BI" e descrição "DataScience". Temos tudo que precisamos!

Nossa API está funcionando! Ela está conseguindo guardar os arquivos da S3 e preencher a nossa tabela do DynamoDB com todas as informações relevantes, para podermos fazer as pesquisas.

A seguir, vamos montar essas pesquisas.