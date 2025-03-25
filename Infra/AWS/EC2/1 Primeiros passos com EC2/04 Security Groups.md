No último vídeo, relembramos alguns conceitos e os colocamos em prática.

Agora vamos relembrar o assunto de _security groups_.

Através das nossas máquinas, nos conectamos ao servidor remoto. Vamos nos desconectar com o comando `exit`.

No menu à esquerda da _AWS_, vamos descer até "Rede e segurança > Security groups". Quando criamos nossa conta, ela recebe um grupo por padrão, o "default". Depois de clicar em qualquer lugar da sua linha, podemos rolar a página para baixo e ver detalhes.

Dentre as abas do grupo, há a aba "Regras de entrada": ela informa que todo o tráfego está liberado para todos os usuários. Logo, o _security group_ padrão libera por completo o acesso à sua rede.

Se acessarmos a aba "Regra de saída", veremos que a mesma coisa também está acontecendo.

Há outro _Security group_, o "launch-wizard-1", que também é criado por padrão, quando criamos nossa instância. Se clicarmos nele e acessarmos a aba "Regras de entrada", veremos uma regra diferente: ele só libera o acesso que utilize _SSH_, mas de qualquer origem.

Podemos alterar essas definições. Vamos permitir apenas o acesso à nossa máquina. Para isso, vamos em "Editar regras de entrada". Vamos apagar "0.0.0.0/0", o código que libera o acesso geral. Vamos selecionar, na seção "Origem", a caixa de seleção para "Meu IP".

Com isso, a _Amazon_ identificará nosso _IP_ público e somente ele poderá acessar essa máquina através de _SSH_. Para identificar melhor mais à frente, vamos adicionar "acesso ssh" à descrição. Depois, vamos salvar a regra.

De volta ao terminal, vamos executar o comando `ssh -i`, somado a chave da _Amazon_ que baixamos e as informações de acesso. No caso do instrutor, foi:

```sql
ssd -i "ec2.pem" ec2-user@ec2-3-87-44-144.compute-1.amazonaws.com
```

Quando tentamos acessar, tudo continua funcionando. Agora vamos testar outra alteração, para impedir a liberação da entrada. Vamos clicar novamente em "Editar regras de entrada".

A partir disso, vamos copiar nosso _IP_ público, removê-lo e, no seu lugar, colar o _IP_ novamente, mas alterando um de seus números, para que seja um _IP_ semelhante ao nosso, mas diferente. No caso do instrutor, ele substituiu "50" por "51", antes da barra inclinada à direita.

Vamos salvar a nova regra. Agora esse outro _IP_ poderia acessar nossa máquina, enquanto o nosso, não.

De volta ao terminal, vamos executar o último comando novamente. Não receberemos resposta do servidor, porque nosso _IP_ não está mais autorizado a acessá-lo.

Vamos voltar o security group "launch-wizard-1" e clicar em "Editar regras de entrada". Vamos apagar o _IP_ fictício e inserir o _IP_ da nossa máquina outra vez. Depois, salvaremos as regras e voltaremos ao nosso terminal, que ainda tenta se conectar.

Vamos interromper isso com "Ctrl + C" e tentar acessar novamente. Como nosso _IP_ voltou a ser liberado, conseguiremos acessar.

> Obs: Os grupos de segurança funcionam como o "firewall" da _AWS_, bloqueando e permitindo acesso de entrada e de saída da instância.

Não precisamos, porém, de um _security group_ para cada instância. Podemos clicar em "Criar grupo de segurança", chamá-lo de "acesso-web" e descrever sua função na caixa de texto abaixo de "Descrição": "Libera acesso a porta 80 e 443 para acesso _HTTP_ e _HTTPS_".

O grupo estará atrelado a uma _VPC_, vamos manter o padrão. Depois, na seção "Regras de entrada", clicaremos em "Adicionar regra". Em tipo, selecionaremos "HTTP". Em "Origem", "Personalizado"= e adicionaremos `0.0.0.0/0,::/0`. Com isso, liberamos o acesso de _IPv4_ e _IPv6_.

Faremos o mesmo processo, adicionando outra regra. Dessa vez, para liberar o acesso _HTTPS_.

Depois, criaremos o grupo de segurança. Nós criamos um grupo de regras que podem adicionadas à nossa instância.

Adicionaremos acessando "Instâncias > Instâncias > ec2-first > Ações > Segurança > Alterar grupos de segurança". Lá, em "Grupos de segurança associados", vamos adicionar "acesso-web", o grupo que acabamos de criar.

Depois que salvarmos, ele será permitido.

Na próxima aula, continuaremos gerenciando instâncias.