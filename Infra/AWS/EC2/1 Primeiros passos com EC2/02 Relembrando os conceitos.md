Agora que você já sabe os conceitos de _cloud computing_ e criou máquinas virtuais com a _AWS_, vamos praticar e focar em _EC2_, o serviço de máquinas virtuais da _Amazon_.

Antes de criar nossas máquinas virtuais, porém, vamos relembrar conceitos importantes. É importante perceber que não vamos precisar gastar dinheiro para estudar sobre o _AWS S2_. Basta acessar aws.amazon.com/free, seremos apresentados ao "Nível gratuitos da AWS".

Nessa página, temos acesso a bastante coisa gratuita, como o acesso ao _EC2_. Temos, aproximadamente, 750 horas por mês para estudar de forma livre, com poucas restrições. Se clicarmos sobre "Amazon EC2 750 horas", seremos redirecionados à descrição da ferramenta.

O nome significa "Elastic Compute Cloud", uma nuvem de computação elástica que suporta instâncias maiores, menores e várias instâncias, por exemplo. Encontramos informações importantes, sobre clientes que usam a ferramenta, para que a usam e mais.

Nosso foco, porém, é garantir que não paguemos nada. Clicando em "Nível gratuito da AWS" somos redirecionados a uma página com detalhes de preço. Nela, veremos que o nível gratuito dá 750 horas grátis com a utilização de um tipo específico de instância, _t2.micro_.

> Obs: Em regiões onde _t2.micro_ não está disponível, será possível utilizar _t3.micro_. Esses números estão relacionadas à geração das máquinas.

Esses são os métodos de precificação: "Sob demanda", que nos cobra conforme o utilizarmos, um modelo mais flexível e mais caro; e "Instâncias spot", que reserva um tempo em determinados tipos de máquina, o que faz a _AWS_ te disponibilizar contas ociosas. A segunda opção é mais barata.

Existem outros tipos de precificação. Quando for trabalhar especificamente com isso, não esqueça de dar uma lida e conhecer todas as possibilidades.

Agora vamos relembrar como criamos uma instância de _EC2_. Na página inicial do _console_, temos informações importantes. O primeiro _widget_, "Visitados recentemente", como o próprio nome já diz, apresenta os recursos que utilizamos recentemente.

Acessaremos o _EC2_, buscando-o na barra de pesquisa. Vamos clicar em "Instâncias > Instâncias > Executar instâncias". Depois disso, vamos dar o nmome "ec2-first" para a tag. Abaixo, selecionaremos a imagem que criaremos na instância.

Basicamente, esse é o modelo que usaremos para subir nosso ambiente. Em início, vamos trabalhar com o padrão: _Amazon Linux_. Ao selecionar essa opção, podemos selecionar a arquitetura, mas vamos manter a do padrão.

Em "Tipo da instância", vamos manter "t2.micro", que se qualifica para o nível gratuito. Todas essas informações estarão atreladas à região que você seleciona. No vídeo, o instrutor selecionou "Norte da Virgínia".

Abaixo, em "Par de chaves (login)", geraremos uma chave pública e outra privada. Com elas, teremos acesso ao servidor. Precisamos ter uma na nossa máquina e outra no servidor, para garantir que acessemos o servidor sem a necessidade de inserir senha ou abrir nossa instância pro mundo geral.

Vammos clicar em "Criar par de chaves" e, a partir disso, vamos dar o nome "ec2". Vamos manter os detalhes padrão em "Tipo de par de chaves" e "Formato de arquivo de chave privada". Faremos isso porque vamos digitar comandos _Linux_ dentro do _Windows_ e usaremos o _OpenSSH_.

Depois, vamos clicar em "Criar par de chaves" e salvá-las. O instrutor as salvou em "wsl5 > Ubuntu > tmp". Agora vamos abrir o terminal e acessar a pasta com `cd /tmp/` e mover o arquivo "ec2" para a pasta `ssh/`:

```bash
cd /tmp/
mv ec2.pem ~/.ssh/
cd ~/ .ssh/
```

Depois, vamos executar o comando `ls -l`, para que vejamos detalhes. Com isso, descobriremos que a chave "ec2.pem" tem muitas permissões. Vamos diminuir o número de permissões, para deixar a chave mais segura, com `chmod 400 ec2.pem`. Isso limitará a leitura da chave para o usuário.

De volta ao navegador, vamos manter as "Configurações de rede" inalteradas. Em "Configurar armazenamento", vamos "acoplar" um HD à máquina. Também não vamos alterar as informações padrão, porque estão dentro do limite gratuito.

Poderíamos configurar mais detalhes avançados, mas só faremos isso mais à frente no treinamento. Agora que finalizamos a configuração, vamos revisar e clicar em "Executar". Essa etapa pode ser demorada, mas isso depende de vários fatores.

Se acessarmos a documentação, no penúltimo link da página, encontraremos diversas formas de conexão, usando um cliente _SSH_, conectando diretamente ao painel e mais.

De volta a "Instâncias", na página do _EC2_, perceberemos que não há instâncias configuradas. Se atualizarmos a página, porém, veremos que a que acabamos de criar será exibida.

Vamos clicar no _ID_ da instância. Lá, veremos mais informações, como o botão "Conectar". Clicando nele, vamos acessar a opção "Cliente SSH", que será utilizada pelo instrutor no vídeo. Vamos copiar o comando do exemplo e levá-lo até o terminal, dentro da parte da chave "ec2.pem".

A chave será utilizada para acessar o terminal remoto da imagem da _Amazon_. Esse domínio foi criado pela _Amazon_ e atribuído à nossa máquina.

Quando digitamos o comando, o terminal informa que ainda não conhece esse _host_ e pergunta se queremos adicioná-lo. Daremos "OK" e depois "yes". Agora a máquina foi adiciona à lista de hosts conhecidos.

Agora já estamos conectados à nossa instância remota no _EC2_.

No próximo vídeo, vamos relembrar o conceito de _security groups_.