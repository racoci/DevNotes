Imagine que você está desenvolvendo um portfólio digital para pessoas desenvolvedoras chamado DEVSPOT no qual cada um tem um perfil único. Para facilitar a busca e acesso aos perfis, você decide implementar uma funcionalidade de consulta por ID através do API Gateway, já que é um método eficiente, pois cada ID é exclusivo para cada perfil. Por fim, seria necessário testar seu conhecimento sobre a implementação dessa funcionalidade.

Ao implementar uma funcionalidade de busca por ID no API Gateway para o DEVSPOT Portfolio, qual das seguintes opções melhor descreve como você deveria proceder para realizar uma consulta por ID de forma eficiente?

Selecione uma alternativa

- **Implementar uma rota no API Gateway que aceite o ID como parâmetro e utilize esse ID para buscar diretamente o perfil correspondente no banco de dados.**
	- Esta é a abordagem mais direta e eficiente, pois utiliza o ID, que é um identificador único, para realizar uma consulta direta ao banco de dados, minimizando o processamento e tempo de resposta.
    
- Utilizar uma consulta genérica que retorne todos os perfis e, em seguida, filtrar pelo ID desejado no lado do cliente.
    
- Criar uma função específica no backend que aceite qualquer tipo de parâmetro e retorne o perfil correspondente, sem se preocupar com a unicidade do ID.
    
- Evitar o uso de IDs para consultas, optando por métodos de busca baseados em nomes ou outras informações não únicas.
    
- Implementar um sistema de cache que armazene todos os perfis acessados recentemente, independentemente do método de consulta utilizado.
    

 [Discutir no Fórum](https://cursos.alura.com.br/forum/curso-amazon-api-gateway-integrando-protegendo-servicos/exercicio-entendendo-a-consulta-por-id/152817/novo)