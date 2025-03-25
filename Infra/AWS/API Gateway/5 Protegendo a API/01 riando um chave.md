Neste momento, nossa API está completa e testada. No entanto, ainda não abordamos um ponto muito importante: a questão da segurança.

Nossa API tem duas partes:

1. A parte administrativa ou de desenvolvimento `/bucket`, na qual podemos fazer upload de imagens, apagar imagens e alterar informações;
2. A parte pública `/fotos`, a qual pessoas podem acessar para pesquisar as imagens que a equipe de desenvolvimento inseriu.

Atualmente, estamos trabalhando com um sistema de segurança por **obscuridade**. Isso significa que estamos informando que o `/fotos` existe, mas mantendo em segredo que o `/bucket` existe. No entanto, se alguém descobrir que o `/bucket` existe, essa pessoa também conseguirá utilizá-lo.

Isso não é uma boa prática. A segurança por obscuridade funciona, mas nunca é a melhor opção. Nossa melhor opção é **criar uma senha** para ter acesso ao `/bucket`. Assim, mesmo que alguém descubra que a parte administrativa existe, essa pessoa não terá acesso por falta de credenciais.

## Criando uma Senha

Portanto, vamos criar essa senha para proteger a parte administrativa da nossa API. Para isso, vamos à página do console do _API Gateway_ pelo navegador.

No menu lateral à esquerda, vamos descer até encontrar a opção "Chaves de API", na qual poderemos criar nossa chave.

No interior dessa página, no canto superior direito, clicaremos no botão "Criar chave de API", o que exibirá uma nova tela chamada "Detalhes da chave de API".

Precisamos apenas de um nome para essa chave. No campo "Nome", digitaremos "colecaodefotos-administrativa". O nome dessa chave identifica a qual projeto ela está atrelada (coleção de fotos) e qual área do projeto ela vai proteger (parte administrativa).

```plaintext
colecaodefotos-administrativa
```

No campo "Descrição", colocaremos o mesmo nome. Na seção "Chave de API", podemos manter a opção "Gerar automaticamente" marcada, pois a chave pode ser gerada automaticamente pela AWS — não precisamos escolher métodos e outros detalhes. Deixamos a AWS cuidar disso para nós.

Por fim, no canto inferior direito, clicaremos no botão "Salvar", o que nos levará para a tela da chave criada.

A partir desse momento, já temos uma chave de API. Abaixo do título "colecaodefotos-administrativa", há o botão "Adicionar ao plano de uso". Ou seja, precisamos criar um plano de uso.

## Criando um Plano de Uso

Vamos ao menu da esquerda para selecionar "Planos de utilização". Na tela central, selecionaremos o botão "Criar plano de uso", o que exibirá a tela "Detalhes do plano de uso".

Na criação do plano de uso, ele solicita um nome. No campo "Nome", vamos colocar "Administrativo", já que nossa API vai cuidar da parte administrativa, ou seja, da parte da equipe de desenvolvimento. Não queremos colocá-la na parte pública.

```plaintext
Administrativo
```

A descrição também terá o texto "Administrativo".

Abaixo da descrição temos um botão de alternância ativado, que se chama "Controle de utilização", e abaixo dele, os campos "Taxa" e "Pico". O que são esses valores?

A taxa é o número de solicitações por segundo que nossa API pode responder, independentemente do número de clientes. Se houver uma pessoa acessando ou 1 milhão, todas estarão fazendo solicitações. Na taxa, definimos o número de solicitações por segundo. Ou seja, o número máximo é sempre um limitador.

Já o pico é o número de solicitações simultâneas que uma única entidade cliente pode fazer por vez. Como cliente, podemos enviar quantas solicitações quisermos. O pico vai definir quantas solicitações a API vai responder para essa entidade cliente.

Por fim, temos um botão de alternância ativado denominado "Cota", que representa o número de solicitações que a entidade cliente pode fazer por mês, por semana ou por dia — a depender da opção que selecionamos no botão de lista suspensa à direita do campo "Solicitações". Com isso, estabelecemos uma limitação, impedindo que a entidade cliente faça, por exemplo, mais de 20 consultas às nossas imagens por dia. Existe essa possibilidade.

Entretanto, no nosso caso, vamos desabilitar tanto o controle de utilização quanto a cota. Não vamos precisar de nenhum deles. Por fim, no canto inferior direito, clicaremos no botão "Criar plano de uso".

Pronto! Nosso plano de uso está criado.

Nossa API já está funcionando e precisando da chave administrativa? Ainda não. Vamos ativar essa chave a seguir.