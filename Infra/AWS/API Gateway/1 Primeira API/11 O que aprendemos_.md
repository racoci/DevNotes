## Nessa aula começamos a criar a API pelo API Gateway. Para tal, aprendemos que:

- API Gateway representa a porta de entrada para as requisições que chegam até a aplicação, nos permitindo espalhá-la em vários serviços da AWS;
- API unifica e simplifica o acesso ao serviços usados por baixo dos panos, o que nos ajuda quanto a muitas mudanças de interface ou se precisarmos de vários serviços separados;
- As funções têm uma política que define qual serviço vamos usar através da API. Com elas podemos criar os permissionamentos para as aplicações;
- No API Gateway podemos importar um arquivo Swagger, clonar ou criar uma nova API. No nosso caso, importamos uma API Swagger com um método POST já definido;
- Podemos mapear uma requisição do API Gateway para outro método HTTP, o que ocorre no bucket. É possível criar imagens no bucket usando o PUT, apesar da nossa requisição ser do tipo POST.