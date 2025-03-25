Na AWS não temos um serviço ou opção de apagar todos os serviços de uma conta. Porém, essa limitação não impediu a comunidade de criar uma ferramenta chamada **aws-nuke**. Com ela podemos apagar todos os recursos criados na AWS, mas para funcionar é necessário um arquivo de configuração.

Quais os campos necessários no arquivo de configuração no aws-nuke?

Selecione 3 alternativas

- [x]     `regions:`
    O campo de `regions:` é usado para descrever qual a região que o aws-nuke deve atuar, e se quisermos que ele atue em todas as regiões podemos usar `- global` no campo de configuração.
- [ ]     `alias:`
    
- [x]     `account-blocklist:`
    O campo de `account-blocklist:` é necessário e descreve quais contas não devem ser mexidas pelo programa sob nenhuma hipótese.
- [x]     `accounts:`
	O campo de `accounts:` é necessário para ter certeza de onde o aws-nuke deve ser executado e evitar que contas não planejadas sejam afetadas.