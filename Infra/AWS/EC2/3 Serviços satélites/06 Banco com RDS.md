Hoje, vamos relembrar os conceitos relacionados ao sistema de gerenciamento do banco de dados da _Amazon_, o _RDS_.

Vamos nos conectar à instância que criamos e instalar um banco de dados nela. Vamos abrir o terminal e dar início à conexão.

Como nossos sitema operacional é um _Debian_, o sistema gerenciador de pacotes é o _APT_. Podemos executar o comando `sudo apt update` para atualizar os pacotes com a ajuda do super usuário. Agora, vamos instalar o _PostgreSQL_, com o comando `sudo apt install postgresql`.

Agora já temos um banco de dados instalado. Podemos configurá-lo, expor a porta no _security group_ e mais. Mas não vamos fazer isso. De volta à _AWS_, vamos selecionar a barra de pesquisa e digitar "RDS". Vamos abrir a página em uma nova aba.

Nessa página, veremos que a _Amazon_ nos trará muitas vantagens no gerenciamento de bancos de dados. Ela consegue, por exemplo, implantar o banco em várias zonas de disponibilidade. Isso diminui a latência.

Descendo a página até a seção "Criar banco de dados", podemos restaurar um banco salvo anteriormente no _S3_, mas clicaremos em "Criar banco de dados", porque não temos nenhum salvo. Vamos começar o nosso do zero.

Na nova página, selecionaremos "Criação fácil" como o método de criação de banco de dados. Isso nos trará alguns padrões pré-configurados. Nosso tipo de mecanismo será o _PostgreSQL_. Não podemos esquecer de selecionar seu "Nível gratuito", logo abaixo.

O identificador da instância será o nome da máquina que será criada, "instancia-pgsql". O nome do usuário será "postgres" e criaremos, abaixo, nossa senha.

Vamos clicar em "Criar banco de dados" e subir nossa instância, que criará uma máquina, instalará servidor de banco de dados, o tornará mais acessível e otimizado.

Quando criamos o banco, podemos ver seus detalhes de conexão clicando em "View connection details".

> Obs: Se você permitiu que a _AWS_ criasse sua senha automaticamente, essa será a única oportunidade de ver sua senha. Portanto, nesse caso, não esqueça de anotá-la.

Vamos clicar no nome da instância "instancia-pgsql" e dar uma olhada em seus detalhes. Vemos o quanto da CPU está sendo utilizado, quantas conexões temos, qual o mecanismo e mais. Há também informações de conexão, como o _Endpoint_, popularmente conhecido como host, e a porta.

Vamos tentar nos conectar ao _Endpoint_ via terminal. Lá, vamos executar o comando `psql -U postgres -W -h` com o link do _Endpoint_. No caso do instrutor, o comando foi o seguinte:

```undefined
psql -U postgres -W -h instancia-pgsql.cbxev7kfqbeb.us-east-1.rds.amazonaws.com
```

Depois, o terminal solicitará nossa senha e tentará se conectar. Se voltarmos ao navegador, veremos que ainda não há conexões. Isso acontece porque não adicionamos o grupo de segurança à instância do _EC2_.

Para resolver isso, vamos acessar a instância e, em seguida, "Ações > Segurança > Alterar grupos de segurança". Na página, vamos adicionar o grupo _default_. Agora podemos salvar e acessar.

De volta ao terminal, teremos sucesso ao tentar novamente. Estamos dentro do banco de dados.

Conseguimos nos conectar no _PostgreSQL_ através de uma instância.

Só poderemos fazer isso através dos serviços da Amazon que estiverem na região, fazendo parte da _VPC_ e tiverem o grupo de segurança habilitado.

No próximo vídeo, vamos dar uma olhada em _load balancing_.