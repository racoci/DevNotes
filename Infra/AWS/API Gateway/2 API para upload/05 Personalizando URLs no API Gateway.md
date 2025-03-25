Imagine que você é parte de uma equipe de DevOps em uma empresa de tecnologia chamada DEVSPOT. Recentemente, a equipe recebeu a tarefa de desenvolver um portfólio para desenvolvedores que será acessado através de uma URL específica gerada pelo API Gateway após o deploy de um novo estágio. Você foi designado para manipular e garantir que a URL gerada esteja de acordo com os padrões da empresa e possa ser facilmente compartilhada com clientes e stakeholders.

Qual das seguintes opções permite a manipulação da URL antes, durante ou após o deploy de um novo estágio, de forma a atender às necessidades do portfólio de desenvolvedores da DEVSPOT?

Selecione 2 alternativas

- [x] Alterar a região da API no console da AWS.
	- Com a alteração da região da AWS, a URL pode ser modificada, mas vale lembrar que isso altera fisicamente o local onde a API se encontra, o que pode gerar impactos e atrasos para quem for acessá-la se ela for colocada em uma região afastada dos clientes.
- [x] Utilizar diferentes ambientes no API Gateway para personalizar a URL.
	- Esta opção permite a personalização da URL ao definir um caminho base específico, facilitando a criação de URLs amigáveis e simples de memorizar para o portfólio de pessoas desenvolvedoras.
- [ ] Usar uma função Lambda para reescrever a URL após o deploy.
- [ ] Modificar diretamente o DNS para redirecionar a URL.
- [ ] Alterar o código fonte do aplicativo para gerar uma URL customizada.