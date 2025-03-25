Caso você esteja recebendo uma cobrança ou tenha terminado algum curso da Alura e tenha medo de ter esquecido algum recursos que pode gerar custos ligado à AWS, tem uma ferramenta que pode te ajudar. Essa ferramenta apaga **todas as informações que estiverem na conta**, então só use se tiver **certeza** que não terá problema apagar todos os dados.

A ferramenta se chama _**aws nuke**_. Começaremos lendo a documentação dela para descobrirmos como utilizá-la e algumas questões de segurança. Para encontrar a documentação, acessaremos o Google e buscaremos por "aws nuke".

Nessa busca, abriremos em uma nova guia o resultado "rebuy-de/aws-nuke", que nos direciona para a [documentação do aws-nuke no GitHub](https://github.com/rebuy-de/aws-nuke). Outro resultado que abriremos também é uma [página da AWS com informações sobre o aws-nuke](https://docs.aws.amazon.com/pt_br/prescriptive-guidance/latest/patterns/automate-deletion-of-aws-resources-by-using-aws-nuke.html).

## Página da AWS

_Por que a AWS tem uma página sobre uma ferramenta que, apesar de funcionar na AWS, não foi feita por ela?_ Essa ferramenta ficou muito popular e muitas pessoas usam, então a AWS decidiu adotá-la, porque ela soluciona um problema real da AWS. Por esse motivo, ela decidiu adicionar uma página de explicação.

A parte mais importante na explicação da página da Amazon é um aviso que encontramos logo no início:

> Aviso: o aws-nuke é uma ferramenta de código aberto que exclui quase todos os recursos na conta alvo da Amazon Web Services (AWS) e nas regiões da AWS. Certifique-se de compreender totalmente o impacto que a ferramenta terá no ambiente de destino antes de usá-la para excluir recursos. Essa solução não é destinada ao uso em um ambiente de produção. Recomendamos implementar essa solução somente em ambientes de _sandbox_ ou de desenvolvimento. Execute uma operação a seco para confirmar que a solução não exclui nenhum recurso que ainda seja necessário. Para obter mais informações, consulte a [seção Cuidado do aws-nuke README (GitHub)](https://github.com/rebuy-de/aws-nuke#caution).

Então **não devemos utilizá-la no ambiente de produção**, porque ela apaga muitas informações da nossa conta, incluindo o serviço que está em produção, servindo nossos clientes. A única circunstância em que podemos usar essa ferramenta no ambiente de produção é se quisermos **apagar a produção inteira**: banco de dados, APIs, serviços, backups e assim por diante.

O recomendado é usar a aws-nuke apenas em ambientes de _sandbox_ ("caixa de areia") ou desenvolvimento, seja de aplicação ou individual. Portanto, usamos somente em ambientes em que podemos destruir tudo que ele contém.

## Documentação do aws-nuke

Agora podemos [acessar a documentação da ferramenta](https://github.com/rebuy-de/aws-nuke), que está no README do GitHub. A documentação está em inglês, então leremos com calma para entendermos todos os pontos que ele avisa para tomarmos cuidado (_caution_) e o que precisaremos para executar o aws-nuke.

Logo no começo ele nos avisa que o **_aws-nuke_ é uma ferramenta muito destrutiva**, e nos pede cuidado ao usá-la, ou acabaremos deletando dados de produção. Eu vou repetir muito essa parte de dados de produção, porque caso executemos o aws-nuke no ambiente de produção, perderemos a linha de produção, como os bancos de dados e todos os dados que ele continha.

### Dicas de segurança

A documentação mais uma vez nos avisa para ter cuidado ao usar a ferramenta em uma conta da AWS, principalmente quando não podemos perder todos os recursos. Além disso, ela passa algumas medidas de segurança, que analisaremos para fazer algumas configurações na nossa conta.

> Dicas de segurança
> 
> 1. Por padrão, o aws-nuke lista apenas todos os recursos com armas nucleares. Você precisa adicionar `--no-dry-run` para realmente excluir recursos.
>     
> 2. aws-nuke pede duas vezes para você confirmar a exclusão inserindo o alias da conta. A primeira vez é logo após o início e a segunda vez após listar todos os recursos com armas nucleares.
>     
> 3. Para evitar apenas exibir um ID de conta, que pode ser facilmente ignorado por humanos, é necessário definir um [Alias de conta](https://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html) para sua conta. Caso contrário, o aws-nuke será abortado.
>     
> 4. O Alias da conta não deve conter a string `prod`. Essa string é codificada e é recomendável adicioná-la a cada conta de produção real (por exemplo, `mycompany-production-ecr`).
>     
> 5. O arquivo de configuração contém um campo de lista de bloqueio. Se o ID da conta que você deseja destruir fizer parte dessa lista de bloqueio, o aws-nuke será interrompido. É recomendável adicionar todas as contas de produção a esta lista de bloqueio.
>     
> 6. Para garantir que você não ignore o recurso de lista de bloqueio, a lista de bloqueio deve conter pelo menos um ID de conta.
>     
> 7. O arquivo de configuração contém configurações específicas da conta (por exemplo, filtros). A conta que você deseja destruir deve estar explicitamente listada lá.
>     
> 8. Para garantir que uma conta aleatória não seja excluída acidentalmente, é necessário especificar um arquivo de configuração. Recomenda-se ter apenas um único arquivo de configuração e adicioná-lo a um repositório central. Dessa forma, a lista de bloqueio de contas é muito mais fácil de gerenciar e manter atualizada.
>     

Primeiramente, por padrão o aws-nuke lista apenas os recursos a serem destruídos. Para realmente executá-lo e fazer com que ele apague tudo, precisamos adicionar o comando `--no-dry-run` depois do nome dele.

Outro ponto é que aws-nuke pede duas vezes a confirmação antes de deletar tudo, entrando com o alias da conta, ou seja, o nome da conta. Nós daremos esse nome para nossa conta e passaremos por essa etapa, não se preocupem.

Esse nome será pedido logo após a inicialização da ferramenta e, em uma segunda vez, após listar todos os recursos apagáveis. Portanto, precisamos nos atentar a isso para inserirmos o alias duas vezes e termos certeza da conta que estamos executando.

Para evitar de colocarmos apenas o ID da conta, que é um número enorme comumente ignorado, que veremos logo mais, é necessário configurar um alias para a conta. Caso não tenha um alias, o aws-nuke vai cancelar toda operação.

Esse alias não pode ter em nenhuma parte escrito "prod", que vem de "produção". Qualquer string com "prod" está travada dentro do código do aws-nuke para evitarmos apagar uma conta de produção.

Sendo assim, é recomendado que adicionemos um alias às nossas contas de produção em um modelo como "nomedaempresa-producao-ecr". Pode ser outro nome, mas o alias precisa ter "prod" em alguma parte do nome.

Outra dica é que o arquivo de configuração precisa ter uma _blocklist_ (lista de bloqueio), ou seja, um espaço para adicionarmos um ID de conta que não será apagada. Além dessa etapa ser **necessária**, é recomendado que adicionemos a ela todos os IDs de conta de produção nessa _blocklist_ para garantirmos que não apagaremos uma conta de produção por engano. É enfatizado que precisa de ao menos um ID na _blocklist_.

O arquivo de configuração precisa ter algumas configurações específicas sobre a conta, como alguns filtros. Inclusive, a conta que queremos apagar precisa ser **explicitamente listada** nesse arquivo de configuração, e descobriremos como fazer isso também.

Para ter certeza de que não deletemos por acidente uma conta aleatória logada no nosso computador, **é necessário especificarmos o arquivo de configuração**, porque nele estará a conta que queremos deletar. Por isso é recomendado termos apenas um arquivo de configuração no repositório central, deixando mais fácil o manejo da lista de bloqueio.

### Casos de uso

Na [seção **_Use cases_ (Casos de uso)**](https://github.com/rebuy-de/aws-nuke#use-cases), o segundo caso listado é bem parecido com o nosso caso. Nesse exemplo ele fala sobre pessoas desenvolvedoras usando contas na AWS para criar um cluster Kurbenetes para serviços de testes. Com o aws-nuke é muito fácil limpar essas contas no final do dia, mantendo os custos baixos.

O outro caso de uso é, ao terminar um curso da Alura, não ter certeza que apagou tudo. Rodando o aws-nuke teremos certeza de que tudo foi apagado.

### Lançamentos

Encontramos o aws-nuke na [seção **_Releases_ (Lançamentos)**](https://github.com/rebuy-de/aws-nuke#releases), onde tem um [link para página de lançamentos do aws-nuke](https://github.com/rebuy-de/aws-nuke/releases). Acessaremos essa página depois para fazermos o download e executar essa ferramenta, mas antes vamos ler a seção sobre o uso.

### Uso

Na [seção _Usage_ (Uso)](https://github.com/rebuy-de/aws-nuke#usage), encontramos mais informações sobre o arquivo de configuração. Logo no começo temos um exemplo de código para o arquivo de configuração mínimo

```makefile
regions:
- eu-west-1
- global

account-blocklist:
- "999999999999" # production

accounts:
  "000000000000": {} # aws-nuke-example
```

A primeira informação que especificamos é as regiões (`regions`) onde queremos apagar dados, ou deixamos a configuração como `global`, para apagarmos tudo em todas as regiões. Em seguida temos o `account-blocklist`, onde adicionamos o ID de uma conta que não será apagada. Por fim, temos o `accounts`, onde passamos o ID da conta que queremos apagar.

Nessa seção também tem um exemplo do retorno da execução, onde vemos que ele tenta apagar também o nome de usuário IAM que está sendo usado para acessar essa conta. É melhor não remover esse usuário, ou não conseguiremos logar com ele, apenas com o nome de usuário principal.

Para evitar a exclusão de usuário IAM, usamos alguns filtro (`filters`), como a documentação mostra no segundo exemplo de código.

```makefile
regions:
- eu-west-1

account-blocklist:
- "999999999999" # production

accounts:
  "000000000000": # aws-nuke-example
    filters:
      IAMUser:
      - "my-user"
      IAMUserPolicyAttachment:
      - "my-user -> AdministratorAccess"
      IAMUserAccessKey:
      - "my-user -> ABCDEFGHIJKLMNOPQRST"
```

Nesses filtro passamos o `IAMUser` com o nome de usuário. Esse usuário precisa ter uma política específica e uma chave de acesso. Usaremos um arquivo de configuração parecido com esse.

## Conclusão

Após acessarmos todas essas informações, no próximo vídeo executaremos o aws-nuke.