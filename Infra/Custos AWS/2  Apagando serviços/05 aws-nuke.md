Agora que já entendemos como o AWS-nuke funciona, vamos executá-lo e apagar todos os recursos da conta.

> Lembre-se de jamais executar o AWS-nuke em uma conta que não pode perder os recursos vinculados a ela.

Abriremos o Console do AWS no navegador. Na barra de busca, escreveremos "IAM" e selecionaremos a primeira opção que aparece como resultado da busca.

No Painel do IAM, logo abaixo do título "Conta da AWS", na lateral direita, teremos o ID da conta e o Alias da conta. No começo, você não terá um Alias criado. Além disso, o ID de cada conta é único.

### Criando um Alias

Logo abaixo do título "Alias da conta", temos um número associado à nossa conta, ao lado do qual está um botão escrito "Criar". Ao clicar nesse botão, uma janela abrirá com um campo de texto a ser preenchido sob o título "Alias preferenciais". Escreveremos "contatesteleo" nesse campo e clicaremos no botão "Salvar alterações".

O Alias criado precisa ser exclusivo para a sua conta, então não podemos repeti-lo. Com isso, o nome do Alias criado aparecerá no painel à direita da página, com as informações da Conta AWS.

### Criando usuário IAM

Além disso, precisaremos criar um usuário IAM para acessar a conta via console. Abaixo do título "Recursos do IAM", temos o subtítulo "Grupos de usuários", com o número zero em azul, logo abaixo. Clicaremos nesse número e seremos redirecionados(as) para uma nova página, a de Grupos de Usuários. Nela, clicaremos no botão "Criar grupo", à direita da interface.

O site solicitará que criemos um nome para o grupo, o qual chamaremos de "root". Logo abaixo, temos um campo opcional para adicionar usuários ao grupo. Por enquanto, deixaremos esse campo vazio porque ainda não temos nenhum perfil de usuário.

No campo "Associar políticas de permissões", podemos definir quem poderá ter modificações no AWS. No nosso caso, queremos permitir acesso total às pessoas usuárias que fazem parte desse grupo. A melhor maneira de fazer isso é dar um duplo clique na coluna "Tipo" da tabela disposta nesse campo. Assim, ele apresentará as categorias de tipo organizadas por ordem alfabética.

A tabela mostrará todas as políticas da categoria "Gerenciadas pela AWS - função de trabalho" primeiro. A partir daqui, marcaremos a caixa de seleção à esquerda dos seguintes nomes de política:

- AdministratorAccess
- PowerUserAccess
- SecurityAudit
- SupportUser
- SystemADministrator
- DatabaseAdministrator
- DataScientist
- NetworkAdministrator
- Billing

Com isso, selecionamos nove funções. Podemos agora clicar no botão "Criar grupo", no fim da página. Com isso surgirá uma mensagem no topo da página "Grupo de usuários root criado".

### Criando usuário

Voltaremos no Painel do IAM para criar um usuário. Podemos fazer isso clicando em "IAM", no topo da página. Clicaremos no número zero logo abaixo da palavra "Usuários" em "Recursos do IAM".

Na página seguinte, clicaremos no botão "Adicionar usuários", no topo direito da interface. No campo "Nome de usuário", escreveremos "acesso CLI". Esse é só um exemplo, você pode escolher o nome que preferir. Após definir o nome de usuário, clique no botão "Próximo", na parte inferior direita da página.

Na página "Definir permissões", desceremos até "Grupos de usuários" e marcaremos a caixa de seleção ao lado do grupo "root", que acabamos de criar. Em seguida, clicaremos no botão "Próximo".

Na página "Revisar e criar", não precisamos fazer nenhuma alteração. Clicaremos no botão "Criar usuário", no canto inferior direito. Isso nos levará à página que exibe a lista de usuários. Lá, encontraremos o recém-criado "acessoCLI".

### Criando uma chave de acesso

O usuário serve para podermos criar uma chave de acesso. Clicaremos no nome do usuário e, na página com as informações detalhadas dele, clicaremos na aba "Credenciais de segurança". Desceremos a página até o título "Chaves de acesso". Clicaremos no botão "Criar chave de acesso".

Na próxima página, marcaremos a opção "Command Line Interface (CLI)", que fornecerá permissão de acesso somente por meio do Terminal. Desceremos a página toda, marcaremos a caixa "Compreendo a recomendação acima e quero prosseguir para criar uma chave de acesso" e clicaremos no botão "Próximo". Não adicionaremos nenhuma etiqueta na chave, então clicaremos no botão "Criar chave de acesso".

A próxima página nos dá a chave de acesso e uma chave de acesso secreta.

> **Atenção**: Jamais guarde a sua chave de acesso secreta dentro de códigos ou em repositórios de código.

Uma opção para salvar essas chaves é baixar um arquivo .csv. Clicaremos no botão "Baixar arquivo .csv" no fim da página. Assim, ele fica salvo no nosso computador. Depois disso, podemos clicar no botão "Concluído".

### Editando o arquivo de configuração

Agora, abriremos o GitHub do AWS-nuke e usaremos o arquivo de configuração que vimos anteriormente, copiando o exemplo que há nele.

Abriremos o Terminal e criaremos o arquivo de configuração. O Leo gosta de usar o nano para criar esses arquivos, mas você pode usar um editor de texto gráfico de sua preferência. Escreveremos "nano config.yaml". É nesse arquivo que colaremos o código copiado no GitHub.

```makefile
regions:
- eu-west-1

account-blocklist:
- "999999999999" # production

accounts:
    "000000000000": aws-nuke-example
        filters:
            IAMUser:
            - "my-user"
            - IAMUserPolicyAttachment:
            - "my-user -> AdministratorAccess"
            IAMUserAccessKey:
            - "my-user -> ABCDEFGHIJKLMNOPQRST"
```

Editaremos esses dados para que eles funcionem na nossa conta. Manteremos os campos `regions` e `account-blocklist` como estão. Em `accounts`, excluiremos todos os zeros e preencheremos as aspas com o nosso número de conta.

Para resgatar esse número, abriremos o Painel do IAM novamente e, à direita, clicaremos no ícone ao lado do número que corresponde ao ID da conta. Observaremos uma mensagem que surge logo acima dizendo "ID da conta copiado". De volta ao terminal, colaremos o número dentro das aspas logo abaixo de `account-blocklist`.

Trocaremos o usuário do IAM (`IAMUser`), as políticas de usuário (`IAMUserPolicyAttachment`) e a chave de acesso (`IAMUserAccessKey`) para `acessoCLI`, escrevendo esse nome nos dois campos onde antes estava escrito `"my-user"`.

Onde estão as letras do alfabeto, inseriremos a chave de acesso da nossa conta.

> **Atenção**: aqui colaremos a chave de acesso, **não a chave secreta**.

Vamos copiá-la do arquivo "acessoCLI_accessKey.csv", que baixamos anteriormente. O código atualizado seguirá os seguintes padrões:

```makefile
regions:
- eu-west-1

account-blocklist:
- "999999999999" # production

accounts:
    "316529025296": aws-nuke-example
        filters:
            IAMUser:
            - "acessoCLI"
            - IAMUserPolicyAttachment:
            - "acessoCLI -> AdministratorAccess"
            IAMUserAccessKey:
            - "acessoCLI -> (USER_KEY)"
```

Assim, não precisaremos nos preocupar em criar uma nova chave toda vez que quisermos executar o AWS-nuke. Do contrário, ele apaga até a chave de acesso usada pelo próprio AWS-nuke. Com o arquivo de configurações pronto, vamos salvá-lo.

### Formas de autenticar o AWS-nuke

Para passar o arquivo, observaremos que precisamos escrever no Terminal "aws-nuke -c", seguido do arquivo de configuração.

Para autenticar o AWS-nuke, podemos usar as credenciais ou os perfis. Um perfil é quando instalamos o AWS CLI, fazemos o config, criando um arquivo de credencial e salva tudo.

O jeito mais prático agora é usar o comando "--access-key-id" e "--secret-access-key".

### Instalando o programa

Se você usar o **macOS**, pode instalar o programa com o comando "brew install aws-nuke". Se você usar o Windows, pode acessar os _released binaries_ no GitHub.

O arquivo "README.md" tem um tópico chamado "Install", onde você encontrará o link para baixar a última versão do GitHub.

Na página de releases do GitHub, a última versão aparecerá primeiro. Opte sempre pela versão mais recente. Desceremos até a lista sob o título "Assets".

No nosso caso, clicaremos com o botão direito do mouse em "aws-nuke-v2.23.0-linux-amd64.tar.gz" e clicaremos na opção "Copiar endereço do link".

Voltaremos ao Terminal e escreveremos "wget", colando o link recém copiado em seguida e pressionando a tecla "Enter".

Assim que o download for finalizado, vamos descompactar o arquivo. Voltaremos à página do GitHub e encontraremos o comando "tar -xz -C $HOME/bin" para fazer a extração. Copiaremos esse comando e colaremos no Terminal, editando-a para "tar -xzf aws-nuke-v2.23.0-linux-amd64.tar.gz". Em seguida, usaremos o comando "ls".

Com isso, o Terminal exibirá um executável:

> aws-nuke-v2.23.0-linux-amd64 config.yaml

### Executando o programa

Para executar o programa, inseriremos os seguintes comandos de uma só vez:

> "./aws-nuke-v2.23.0-linux-amd64 -c config.yaml --access-key-id (USER_KEY) --secret-access-key (Add here the secret access key)"

Em seguida, pressionaremos a tecla "Enter". O Terminal exibirá a seguinte pergunta:

> Do you really want to nuke the account with the ID 316529025296 and the alias 'contatesteleo'? Do you want to continue? Enter account alias to continue.

Ou seja, ele está nos perguntando "Você quer mesmo apagar tudo o que estiver na conta com o ID 316529025296 e o Alias 'contatesteleo'?".

Para prosseguir, digitaremos "contatesteleo" e pressionaremos a tecla "Enter". O Terminal carregará tudo o que o AWS-nuke julga que pode ser removido da conta. Em seguida, exibe o texto:

> _The above resources would be deleted with the supplied configuration. Provide --no-dry-run to actually destroy resources._

Com isso, escreveremos "./aws-nuke-v2.23.0-linux-amd64 -c config.yaml --access-key-id (USER_KEY) --secret-access-key 055x5iBA14v8A28C/n25wzI9E11GFIPihNUhNUkr --no-dry-run" no Terminal e pressionaremos a tecla "Enter" para confirmar que desejamos excluir os arquivos identificados.

Em seguida, ele exibirá novamente a mensagem perguntando se desejamos prosseguir. Para continuar, escreveremos o Alias da nossa conta ('contatesteleo') e pressionaremos "Enter".

Os itens passíveis de remoção aparecem com um "_would remove_" escrito em azul no Terminal. Tudo o que estiver com anotações amarelas não pode ser excluído.

Com isso, o AWS-nuke começa a tentar apagar os itens passíveis de remoção. Os itens apagados com sucesso aparecerão com o texto "_triggered remove_" em azul, aqueles que falharem terão o texto "_failed_" em vermelho.

Com o fim da primeira rodada, o Terminal exibirá uma mensagem como essa:

> Removal requested: 6 waiting, 4 failed, 58 skipped, 0 finished.

Isso indica que quatro remoções falharam. Ele continuará tentando até terminar todas. No fim desse processo, você poderá observar uma mensagem semelhante a esta:

> Nuke complete: 0 failed, 58 skipped, 10 finished.

Os 58 itens que foram pulados são padrão da AWS, ou seja, não há motivo para eles serem removidos. Assim, tivemos um total de 10 recursos que poderiam ser removidos.

A prática adotada pelo Leo quando ele termina de fazer um curso para a Alura é rodar o AWS-nuke, apagar todos os recursos e, assim, evitar custos indesejados.

Esperamos que esse programa seja útil para você. Nos vemos no vídeo de conclusão!