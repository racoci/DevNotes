Agora nosso _load balancer_ já está funcional.

Vamos aprender a configurar domínios que já existem e a fazê-los apontar para esse _load balancer_. Vamos copiar o "Nome do _DNS_". Podemos adicionar um _CNAME_, ou seja, um apelido, importado de outro domínio para este.

Para exemplificar, o instrutor acessa um domínio já existente, que lhe é pessoal. Para fazer isso, clicamos em "Gerenciar registros personalizados", para dar início à criação de um novo domínio.

Vamos clicar em "Criar novo domínio" e, na nova caixa de texto que surgirá, vamos digitar "aws". Agora, selecionaremos o tipo "_CNAME_". Na coluna de dados, vamos inserir o endereço do _load balancer_.

Como a propagação de _DNS_ não é instantânea, isso poderá levar algum tempo. Podemos perceber, porém, que não precisaremos configurar nada na _AWS_. Basta aponta para o domínio do load balancer.

> Também é possível registrar e configurar domínios dentro da _AWS_. Para aprender, faça o treinamento de _Amazon Route 53_.

Vamos acessar o terminal para executar testes. Vamos executar o comando `dig` e inserir o domínio. No caso do instrutor, o domínio é "aws.dias.dev":

```undefined
dig aws.dias.dev
```

Com o comando, descobriremos para onde o _DNS_ aponta. Por enquanto, ele aponta apenas para o _Google Domains_. Ainda precisamos mandá-lo para a _AWS_.

Depois de algum tempo, poderá, uma nova sessão surgirá para direcioná-lo também ao _load balancer_. Ao acessar "aws.dias.dev", conseguiremos acessar o balanceador de carga.

O assunto do próximo vídeo é _auto scaling_.