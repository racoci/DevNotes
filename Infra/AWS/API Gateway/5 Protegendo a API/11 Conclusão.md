Parabéns por concluir mais um curso na Alura! Vamos revisar tudo o que desenvolvemos durante este curso?

## O que Aprendemos neste Curso?

Iniciamos com uma API inicial, desenvolvida pelo time de desenvolvimento, para ter nosso primeiro _endpoint_. Essa API já possuía a funcionalidade de salvar arquivos no _S3_, para o qual criamos um _bucket_ com a função de armazenar esses arquivos.

Em seguida, questionamos o que aconteceria se alguém subisse uma imagem em nossa API com um nome errado, ou antes do momento adequado. Concluímos que precisaríamos excluir essa imagem, e pensando nisso, criamos o método `DELETE`, com a função específica de remover esses arquivos.

Com isso, concluímos a primeira versão da API. Logo em seguida, recebemos uma nova demanda para expandir a API e possibilitar a realização de pesquisas dentro dessas imagens.

Para auxiliar nessas pesquisas, criamos uma tabela no _DynamoDB_, um banco de dados fornecido pela AWS, e uma função no _Lambda_ — serviço que permite a execução de código sem servidores —, com o objetivo de automatizar a entrada de dados nessa tabela. Assim, poderíamos lê-la e fazer os filtros enviarem as informações das pesquisas para a API da forma mais rápida possível.

Nossa API possui pesquisa por ID, pesquisa por assunto e uma pesquisa mais genérica, além da documentação. Também criamos uma chave de API para proteger o `/bucket`, a parte administrativa da nossa API, na qua podemos subir e apagar imagens.

Por fim, testamos tudo isso através do _Postman_, verificando se a API estava funcionando e respondendo de acordo com o que queríamos, além de verificar se a chave de acesso estava válida.

Realizamos muitas coisas e também criamos vários recursos diferentes na AWS. Portanto, **não se esqueça de apagar esses recursos caso não vá mais utilizá-los, para evitar cobranças desnecessárias**.

Caso tenha ficado com alguma dúvida, temos o [fórum do curso](https://cursos.alura.com.br/course/amazon-api-gateway-integrando-protegendo-servicos/task/f%C3%B3rum%20do%20curso) para ajudar a esclarecer essas questões. Também temos a [comunidade do Discord](https://discord.gg/SK9bj7hEYD), que é muito ativa e traz vários projetos e novidades.

Além disso, disponibilizamos vários conteúdos extras neste curso para serem explorados. Há muita coisa interessante que vai te ajudar.

Por fim, **não se esqueça de avaliar este curso**. Conte-nos o que gostou, o que não gostou e o que acha que podemos melhorar. Assim, poderemos trazer cursos cada vez melhores.

Esperamos você no próximo curso!