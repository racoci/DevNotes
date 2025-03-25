Agora que você criou as permissões para que seja possível ler a tabela do DynamoDB, está na hora de ajudar a sua equipe a integrar os serviços do API Gateway e deste banco de dados. No entanto, você ficou em dúvida sobre qual é a melhor ação a ser utilizada para filtrar por muitos itens, uma vez que só temos uma chave primária criada na tabela.

Selecione a alternativa com a ação que pode realizar a recuperação das informações.

Selecione uma alternativa
- GetItem
	- Apesar do `GetItem` poder pegar itens da tabela, temos que realizar a operação de um item por vez, e temos que usar a chave primária, o ID no nosso caso o que o torna inviável para uma pesquisa.
- UpdateItem
- CreateTable
- Query
	- O `Query` recupera vários itens, mas é necessário uma chave de partição que decidimos não usar.
- **Scan**
	- O `scan` recupera todos os itens na tabela ou no índice especificado com a possibilidade de aplicar uma condição de filtragem para retornar apenas os valores de interesse e descartar o restante.