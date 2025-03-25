Vamos ligar a máquina novamente, clicando em "Ações > Iniciar instância". Quando fizemos isso, nosso _IP_ e nosso _DNS_ mudaram.

Precisamos resolver isso. De algum forma, precisamos criar um _IP_ fixo para essa máquina.

> Obs: Mesmo que você nunca desligue sua máquina, ela pode ter uma pane. Por isso, o ideal é alocar um _IP_.

No menu da esquerda, vamos acessar a página "IPs elásticos", o serviço de registro de _IP_ da _Amazon_. Vamos clicar em "Aloca endereço IP elástico". Deixaremos todas as opções no padrão e clicar, simplesmente, em "Alocar".

Com o _IP_ alocado, podemos clicar no seu endereço e, em seguida, na opção "Associar endereço _IP_ elástico". Vamos manter "Instância" selecionada em "Tipo de recurso". Vamos inserir nossa instância logo abaixo. Agora basta clicar em "Associar"

A partir de agora, o _IP_ apresentando na tela será redirecionado à nossa instância. Podemos copiá-lo e tentar acessá-lo em uma nova aba. Teremos sucesso nisso.

O _IP_ antigo não está mais associado à nossa instância. Porém, agora podemos desligar nossa máquina quantas vezes quisermos, porque o _IP_ permanecerá o mesmo.

Como os _IPs_ são separados das instâncias, eles também geram cobranças. Por isso, quando remover a instância, poderá ainda ser cobrado pelo _IP_. O endereço de _IP_ só não é cobrado se estiver associado a uma instância em funcionamento. Caso a instância estiver parada ou o _IP_ não estiver associado a uma instância, ele resultará em cobrança.

> Obs: Se sua máquina tiver mais de um _IP_ associado a ela, os _IPs_ extras serão cobrados.

Podemos ver todos os detalhes de precificação na documentação do _AWS EC2_.

Dessa forma, definimos um _IP_ estático para a nossa instância.

No próximo vídeo, vamos manipular bancos de dados com _RDS_.