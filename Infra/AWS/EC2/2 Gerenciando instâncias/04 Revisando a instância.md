Agora vamos testar a instância.

Duas verificações foram feitas. A máquina virtual está funcionando. Quando clicamos na linha de "nginx", abre-se um menu com vários detalhes na parte inferior da tela. O detalhe no qual estamos interessado é o "Endereço IPv4 público".

Além disso, há o _DNS_ público, o nome que aponta para o IP. Se clicarmos em algum deles, esperamos ver uma página do _nginx_. Porém, quando clicamos, recebemos uma mensagem de erro. Isso acontece porque tentamos acessar usando _HTTPS_ sem termos configurado certificados _SSL_.

Para acessarmos, precisaremos substituir o "https" do link do "http" na barra de endereço e acessar novamente. Agora receberemos uma mensagem de sucesso, porque conseguimos executar a imagem "Bitnami NGINX Open Source 1.23.1" via _Cloud_.

Na página, também encontramos detalhes de documentação. Basta clicar no botão "Documentation". Com isso, seremos redirecionados para a página de documentação. Na página "Get Started" há várias informações úteis.

Isso servirá para que compreendamos como utilizar essa imagem e configurá-la, com a ajuda de alguns exemplos. Vamos voltar à página "Instâncias" e clicar em "nginx > Conectar > Cliente SSH". Lá, veremos que o usuário exibido é o "admin".

Já na imagem padrão da _Amazon_ que acabamos de utilizar, o usuário é "ec2-user". É comum que imagens diferentes configurem usuários diferentes.

Porém, se copiarmos o link no final da página e tentarmos acessar a instância via console, vamos nos deparar com um erro. Isso acontece porque o usuário correto para essa imagem não é "admin", mas "bitnami". É na documentação que nós encontramos esses detalhes.

Se formos em "Conexão de instância do EC2" e definirmos o nome do usuário "bitnami", poderemos acessar a instância direto pela interface web com o usuário correto. Agora basta informar na linha de comando.

Com o comando `whoami`, veremos que o usuário se chama "bitnami". Com `uname -a`, vemos que nosso sistema operacional é um _Debian_, com o _nginx_ instalado. Com isso, entendemos que imagens podem ser criadas a partir da configuração de outros softwares.

Vamos voltar para página "Instâncias". Lá, veremos que criamos a instância nova na mesma zona de disponibilidade, "us-east-1d". Apesar disso, ainda não fomos apresentados à área onde isso é definido.

Vamos clicar em "Executar instâncias", para simular a criação de uma nova instância. Assim, vamos localizar essa informação. Vamos manter todas as opções no padrão e desce até "Configurações de rede > Editar > Sub-rede". Cada uma das sub-redes apresentadas na lista está uma zona de disponibilidade diferente.

É aí que escolhemos, se estivermos em um cenário que exija isso.