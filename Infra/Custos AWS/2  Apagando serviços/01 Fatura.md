Como todos os serviços que são cobrados, a AWS também tem uma fatura, ou seja, um registro com esclarecimento de todos os itens que estão sendo cobrados. Podemos acessar essa fatura da AWS através do painel, verificando quais serviços estão sendo cobrados e por quanto.

Com essas informações, podemos tentar reduzir o serviço ou interrompê-lo para removermos esse custo. Porém se lembrem de nunca remover serviços que estão em aplicações ativas e que nossos clientes estão acessando.

Juntando essa fatura com os avisos que já vimos, temos uma ferramenta muito boa para conter os dados da AWS ao mínimo possível. Portanto, vamos acessar nossa fatura para descobrirmos o que está sendo cobrado e analisar esses serviços.

Na seção de Orçamentos (_Budgets_), que já estávamos anteriormente, nós criamos nosso aviso de custos. No caso, o instrutor tem outra conta tem uma conta pessoal na AWS onde ele tem uma fatura referente ao que produzo para Alura. Pode ser que a sua página de fatura esteja vazia.

Para acessar as faturas, navegamos na coluna da esquerda por "Faturamento > Faturas". Ao abrirmos essa página, encontramos todos os itens. A futura atual na conta do instrutor está cobrando US$ 1,39 (um dólar e 39 centavos) até o momento da gravação.

Rolando a fatura para baixo, temos informações sobre alguns custos e estimativas desses valores. Rolando ainda mais para baixo, temos uma barra horizontal de navegação onde a primeira seção é "Cobranças por serviço", que é exatamente o que queremos.

Nessa seção, conseguimos o detalhamento do que está sendo cobrado e por qual valor. Por exemplo, o primeiro serviço é o _Elastic Compute Cloud_ (EC2). Ao clicarmos no botão de "+" à esquerda do nome, temos a informação da região, no caso, "US East (N. Virginia)".

À esquerda do nome da região tem outro botão de "+" que, ao clicarmos, temos acesso a mais informações. No caso, temos o EC2 rodando o Linux em uma máquina _On Demand_ t2.nano, aquela que simulamos e é ainda menor que a t2.micro. Ele já está rodando por 133 horas, o que gerou o custo de US$ 0,77, então precisamos ter mais cuidado quando formos mexer.

Além disso, existem dados que estão sendo armazenados no EC2, e as informações sobre isso estão na seção "EBS". Temos dois discos que foram criados: um que já está custando US$ 0,11 e outro que está já está no valor de US$ 0,09. Esses não são valores grandes, mas todo mês terá essa cobrança. Portanto, se não estiverem em execução, podem ser finalizados.

Outro serviço que está sendo cobrado é o _Secrets Manager_. Ao expandi-lo, encontramos mais uma vez a região em que esse serviço está rodando, a US East (N. Virginia), que podemos expandir novamente.

Nesse serviço temos o valor de US$ 0,40 cobrado por segredo a cada mês, o que gerou uma cobrança de US$ 0,24 nesse mês. Outra cobrança desse serviço é por acessos, então são cobrados US$ 0,05 a cada 10.000 acessos. Como só fizemos 4 acessos, esse serviço ainda não foi cobrado até o momento. Quanto mais acessos forem feitos, maior será esse custo.

Outro serviço que tem uma cobrança nessa fatura é o _Cost Explorer_: um serviço com o qual podemos explorar alguns custos da AWS. Ele cobra US$ 0,01 por acesso à API. Como até o momento só foi feito um acesso, a cobrança foi de apenas US$ 0,01.

Precisamos ter cuidado porque nem sempre precisamos criar algo para recebermos cobranças. Às vezes acessar algum recurso já pode gerar um custo.

Existem vários outros serviços ativos que aparecem na fatura e podem ser cobrados, mas alguns não estão sendo, por exemplo o Lambda, que está no final da lista. Ao expandir as informações desse serviço, observamos que estamos no "_Compute Free Tier_" (Nível de Computação Gratuito).

Da mesma forma, existem cobranças por requisições, mas estamos no "_Request Free Tier_" (Nível de Requisição Gratuito). Nesse nível, podemos fazer até um milhão de requisições por mês e só foram utilizadas quatro. Sendo assim, esse serviço é gratuito.

Como aprendemos anteriormente, o Lambda é sempre gratuito, desde que usemos o _Free Tier_. Caso passemos do valor máximo de requisições, a cobrança será apenas pelo excedente, até um milhão é gratuito.

Existem algumas **formas de apagarmos** esses serviços que não formos usar. Uma delas é fazer **manualmente**, entrando em cada serviço e apagando os recursos que geram custos. Outra forma é usarmos um **programa para apagar tudo**, então tenham cuidado com esse programa, porque ele apaga todos os dados da conta.

A seguir vamos descobrir como esse programa funciona.