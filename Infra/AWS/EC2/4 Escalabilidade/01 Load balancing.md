Nesse vídeo, vamos falar sobre escalabilidade.

Para que nosso sistema não saia do ar em caso de queda de uma instância, podemos criar outra, para dividir a carga do nosso sistema entre as duas.

Assim, conseguiremos lidar com o dobro de requisições.

_Load balancing_, balanceamento de carga em português, não é algo específico da _AWS_. Vamos configurar o _load balancer_ na _AWS_.

No console da _AWS,_ vamos selecionar a instância e seguir o caminho "Ações > Imagem e modelos > Executar mais como esta". Com isso, criaremos outra instância idêntica. Mudaremos o nome para "nginx-2". O par de chaves será o "ec2", para viabilizar o acesso via _SSH_.

Vamos selecionar, porém, uma sub-rede diferente: será a finalizada em "1a". Agora temos duas instâncias, cada uma em um local diferente. Vamos habilitar a atribuição automática de _IP_ público e não configuraremos mais nada. Vamos só clicar em "Executar instância".

É possível filtrar as instâncias pela barra de busca. Vamos selecionar apenas as instâncias "Executando" e "Pendente", para observarmos as nossas duas. Quando a nova não estiver mais pendente, vamos deixar apenas o filtro "Executando".

Vamos criar, agora, o balanceador de carga entre as duas instâncias. No menu da esquerda, vamos selecionar "Balanceamento de carga > Load balancers > Criar Load Balancer". Vamos selecionar o "Application Load Balancer".

Em "Basic configuration", vamos definir o nome do balanceador como "lb-teste". Em "Scheme", manteremos a opção "Internet-facing", o que significa que ele ficará aberto para o mundo. Em "IP address type" vamos manter "IPv4".

O _load balancer_ só distribuirá carga para as nossas instâncias, que são "us-east-1a" e "us-east-1d", se as marcarmos em "Mappings". Vamos marcá-las.

Em "Security groups", precisamos habilitar o "default", porque o _load balancer_ precisa localizar nossas instâncias. Também adicionaremos "acesso-web", para que o mundo externo consiga acessá-lo também.

Em "Listeners and routing", vamos adicionar roteamento. Vamos clicar em "Create target group", para criar nosso primeiro grupo de alvos. Vamos mantê-lo na opção "Instances", porque vamos manipular apenas instâncias.

O nome do target group será "tg-principal". Vamos utilizar o protocolo HTTP. Em "Health checks", ou verificações de segurança, vamos definir os critérios da avaliação de saúde das requisições. Em "Sucess codes", vamos escrever "200-299". No resto, manteremos o padrão.

Agora vamos adicionar nossas duas instâncias ao grupo de alvos. Depois, clicaremos em "Include as pending below". Por fim, criaremos o target group.

Vamos voltar à aba do _load balancer_ e selecionar o _target group_ que acabamos de criar e, na sequência, criar o _load balancer_.

Vamos clicar em "View load balancer", para analisar nossa lista de _load balancers_. Ele estará no estado "Provisionando" e, em breve, estará "Ativo". Depois disso, podemos copiar a _URL_ ao lado de "Nome do DNS" para executar um teste.

Vamos abrir uma nova aba e colar a _URL_. Teremos sucesso: conseguimos acessar.

Se voltarmos às instâncias e nos conectarmos como cliente _SSH_, podemos inserir o endereço no terminal, com o comando `ssh -i ec2.pem bitnami`. Agora vamos acessar através de `vim /opt/bitnami/nginx/index.html`. É nessa pasta que está a maior parte da configuração.

No arquivo _HTML_, adicionaremos, logo depois de `<body>`, um `<h1>` com "Serviço 1". Vamos salvar com "ESC + : + X" e fechar o arquivo.

Vamos sair e voltar ao console da _AWS_. Vamos nos conectar ao "nginx-2", copiar o endereço em "Cliente SSH" e nos conectaremos a ele repetindo os comandos anteriores. Também acessar o arquivo "index.html".

Porém, dessa vez vamos adicionar uma tag `<h1>` com "Serviço 2". Portanto, cada instância exibirá um título diferente. Caso atualizemos a página constantemente, poderemos notar a alteração no navegador.

Vamos desligar o serviço 1, acessando "Estado da instância > Interromper instâncias > Interromper". Isso desligará a máquina. Depois disso, só conseguiremos acessar a outra instâncias. Podemos religar serviço 1 a qualquer momento.

No próximo vídeo, vamos configurar um domínio.