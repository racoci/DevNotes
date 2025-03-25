Temos a tabela pronta para utilizar no DynamoDB. Mas, como a nossa API vai **acessar** essa tabela? Ela ainda não tem permissão para isso. Portanto, precisamos **criar essa permissão**.

> Lembrando que, quando temos uma infraestrutura com servidores, podemos utilizar endereços de IP para um servidor acessar o outro. No entanto, quando estamos usando os serviços da AWS, é importante ter em mente que eles se comunicam através das **permissões**.

## Criando nova política de acesso

Vamos acessar o **IAM** para criar essa permissão. No painel pateral, clicamos em "Gerenciamento de acesso > **Políticas**". Nessa página, clicamos em **"Criar política**".

Primeiro, precisamos selecionar o **Serviço** que vamos acessar - nesse caso, o DynamoDB.

Depois, selecionamos as **Ações permitidas**. No caso, a nossa API só precisa ler o DynamoDB, pois não vai escrever nele. Então, vamos selecionar "**Leitura > Todas as ações de leitura**".

Vamos descer um pouco a tela, até a seção de **Recursos**, para especificar ARNs de recursos para essas ações. Nossa API vai ter acesso a uma tabela, à "_**table**_", o que acabamos de criar. Localizamos a _table_ e clicamos em "_Adicionar ARNs_".

Aberta a modal de Especificar ARNs, voltamos para a guia do DynamoDB e entramos na tabela "_**colecaodefotos**_". Na **Visão geral** da tabela, teremos uma seção de **Informações adicionais**. No fim dela, temos o "**Nome de recurso da Amazon (ARN)**". Vamos copiar esse código e voltar para a guia do IAM.

Vamos colar esse código no campo "**ARN do recurso**". Ao fazer isso, os campos de Região do recurso e de Nome da tabela são preenchidos automaticamente com "_us-east-1_" e "_colecaodefotos-leo_", respectivamente. Por fim, clicamos em "**Adicionar ARN**" no canto inferior direito da telsa.

Feito isso, retornamos à página de criar política. No final dela, vamos clicar em "**Próximo**". Essa página faz um resumo das permissões e pede o nome da nossa política.

O nome começa com o nome da nossa aplicação, "_colecaodefotos_", seguido pelo nome do recurso a que estamos permitindo acesso, o "_dynamodb_". No entanto, essa política não dá acesso ao DynamoDB completo para "colecaodefotos", mas apenas à _leitura_. Por fim, colocamos o nome da pessoa responsável - no caso do instrutor, "_leo_". Então, o nome da política será: "_**colecaodefotos-dynamodb-leitura-leo**_". Assim sabemos tudo o que essa política faz!

Vamos copiar o nome e colar np campo de Descrição, depois rolar a página até o final e clicar em "**Criar política**". Política criada!

## Criando a função

Agora, no menu lateral esquerdo do IAM, vamos clicar em "**Funções**" para agora criar função. Nessa página, clicamos em "**Criar perfil**".

Na próxima tela, selecionamos o tipo de entidade confiável: **Serviço da AWS**. Depois, indicamos o **Serviço ou caso de uso**, ou seja, quem vai criar o acesso. Será a **API Gateway**, então, buscamos esse serviço e selecionamos. Clicamos em "Próximo" no fim da página.

A próxima tela, intitulada **Adicionar permissões**, vai mostrar as permissões que já existem para seleção. Vamos adicionar a nossa permissão mais adiante, então clicamos em "Próximo" novamente.

Na próxima tela, damos um **nome** para a função. Começamos com o nome da nossa aplicação, "colecaodefotos", depois o nome do serviço que está fazendo o acesso, o "apigateway", e depois o serviço que está sendo acessado, o "dynamodb", seguido do nome da pessoa responsável por essa função. No caso do instrutor, o nome da função é "_colecaodefotos-apigateway-dynamodb-leo_".

Vamos copiar esse nome e colar no campo de descrição. Descemos até o final da tela e clicamos em "**Criar perfil**". Perfil criado!

Podemos clicar no botão "Visualizar função" na barra superior verde de sucesso para visualizá-la, ou pesquisar por "colecaodefotos" na barra de pesquisa de funções. Visualizaremos as duas que criamos: "_colecaodefotos-apigateway-dynamodb-leo_" e "_colecaodefotos-APIgateway-S3_". Vamos clicar na que acabamos de criar.

Com isso, podemos verificar todos os detalhes dessa função. Na aba de Políticas de permissões, clicamos em "**Adicionar permissões > Anexar políticas**". Podemos pesquisar o nome da política que criamos, "_**colecaodefotos-dynamodb-leitura**_", selecioná-la e clicar em "**Adicionar permissões**".

Pronto! Temos as permissões para poder acessar o DynamoDB, nosso banco de dados. Falta agora **preencher** esse DynamoDB. Faremos isso no próximo vídeo!