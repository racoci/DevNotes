Criamos duas instâncias, um _load balancer_ e um grupo de destino que balanceia a carga entre as duas instâncias. Tudo isso está funcionando.

Agora vamos configurar o seguinte: caso uma instância, por qualquer motivo, seja desligada, outra será ligada automaticamente. E, caso vários requisições cheguem ao mesmo tempo, queremos que mais instâncias sejam criadas também automaticamente.

No menu lateral, vamos acessar "Auto Scaling > Grupos Auto Scaling > Criar grupo do Auto Scaling". Antes de criar o grupo, porém, precisamos de um modelo. O nome do grupo será "sistema-web". Vamos manter o padrão de Modelo de execução, clicando em "Criar um modelo de execução".

O nome do modelo será "modelo-nginx". Mais abaixo, em "Imagens de aplicação e de sistema operacional", vamos selecionar "Minhas AMIs" e, na sequência, "De minha propriedade". Assim, utilizaremos a imagem que criamos, "my-bitnami-nginx".

O tipo da instância será "t2.micro", para que continuemos no nível gratuito. O par de chaves será "ec2". Vamos selecionar, entre os grupos de segurança existentes, "launch-wizard-1". O grupo "acesso-web" não é mais necessário.

Agora é só clicar em "Criar modelo de execução".

Vamos atualizar a aba do "Criar grupo de Auto Scaling" e selecionar nosso modelo _NGINX_. Agora vamos entender onde o _Auto Scaling_ criará as instâncias. Em "Zonas de disponibilidade e sub-redes", vamos selecionar as zonas "a" e "d".

Na próxima página, vamos configurar o balanceamento de carga. Vamos anexar o grupo de _Auto Scaling_ ao balanceador que já criamos, "tg-principal | HTTP". Vamos clicar em "Pular para revisão". Depois, vamos clicar em "Criar grupo de Auto Scaling".

A capacidade desejada de instâncias do grupo é de 1, mas vamos modificá-la, clicando em "Editar". Vamos alterar "Capacidade desejada" e "Capacidade mínima" para 2. "Capacidade máxima" será alterada para 3. Com isso, teremos sempre no mínimo 2 instâncias e no máximo 3. Agora basta clicar em "Atualizar".

Além disso, já que se trata de um _auto scaling_, duas novas instâncias serão criadas automaticamente. Vamos voltar a "Balanceamento de carga > Grupos de destino". Veremos que, agora, nosso _target group_ principal tem 3 _targets_ agora: a instancia da "nginx-2", a da "nginx" e um terceiro.

Quando clicamos no terceiro, descobrimos que se trata do grupo de _auto scaling_.

Vamos manter apenas esse terceiro target e remover os outros dois, que criamos manualmente, selecionando-os e clicando em "Deregister". Agora vamos excluir as intâncias, em "Instâncias > Estado de Instância > Encerrar instância".

No próximo vídeo, executaremos alguns testes e aprenderemos a criar a terceira instância.