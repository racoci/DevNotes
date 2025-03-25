Agora vamos aprender a operar pela _AWS CLI_, a linha de comando do _Amazon Web Services_.

Vamos pesquisar "aws cli install" no _Google_ e clicar no primeiro link. Essa é a página da documentação que ensina a instalar a _AWS CLI_. Há instruções para cada um dos sistemas operacionais.

No _Windows_, basta baixar o instalador no link ou rodar o comando no seu terminal.

No _macOS_, também há as opções de instalador e de linha de comando.

No _Linux_, basta executar os três comandos presentes na documentação. É isso que o instrutor fará.

É importante que tenhamos pelo menos a versão 2.7.29 da _AWS CLI_. Podemos verificar isso executando o comando `aws --version`:

```css
aws --version
```

Temos a _AWS CLI_ instalada, mas ainda não podemos utilizá-la. Precisamos fazer a configuração, rodando o comando `aws configure`. Ao fazer isso, o terminal nos solicitará a "AWS Access Key".

Vamos voltar ao _Dashboard_ da _AWS_. Um dos serviços exibidos nessa página é o _IAM_. Essa é uma interface que controla o acesso aos recurso da nossa conta, e nós vamos abri-la.

> Obs: É importante que o usuário raiz da conta tenha autenticação multifatores (_MFA_). Sua segurança precisa ser redobrada.

Vamos criar outro usuário, acessando "Gerenciamento de acesso > Usuários". Vamos clicar em "Adicionar usuários", porque não utilizaremos a _CLI_ como usuário raiz. Vamos criar outro usuário gerenciável.

O nome do usuário será "teste". Em seguida, escolheremos o tipo de credencial. No caso, selecionaremos "Chave de acesso: acesso programático". Vamos avançar à próxima página, onde gerenciaremos permissões.

Como só temos um usuário, selecionaremos a opção "Anexar políticas existentes de forma direta". Adicionaremos a política "AdministratorAccess", que concede acesso de administrador. Poderíamos adicionar tags, mas não faremos isso. Avançaremos para a revisão.

Chegou a hora de clicar em "Criar usuário". Ao fazer isso, receberemos o _ID_ da chave de acesso. Vamos copiá-lo, pois precisamos levá-lo ao terminal, que há pouco nos solicitou essa informação.

Agora, o terminal solicita a "AWS Secret Acess Key", que está ao lado do ID da chave de acesso no navegador. Basta copiá-la e levá-la para o terminal.

Vamos adicionar outra configurações. Vamos definir a "Default region name" em "us-east-1", que é o padrão, "Default output format" também será o padrão. Agora nossa _AWS_ está configurada. Se executarmos o comando `aws help`, veremos o que podemos fazer:

```bash
aws help
```

No próximo vídeo, vamos conhecer alguns dos comandos que podemos executar na _EC2_.