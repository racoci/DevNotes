Imagine que você está trabalhando em um projeto chamado DEVSPOT, portfólio digital para o qual implementou uma API Gateway para gerenciar o acesso às diferentes partes da aplicação. Para garantir a segurança e o funcionamento da aplicação, você adicionou uma chave de acesso `x-api-key` para a parte de DEV do portfólio. Agora, é crucial testar se a configuração está correta, assegurando que a API pública seja acessível sem senha e a parte de DEV exija a chave de acesso correta.

Após realizar um novo deploy da sua API no projeto DEVSPOT, como você pode verificar se a configuração de acesso está funcionando corretamente?Imagine que você está trabalhando em um projeto chamado DEVSPOT, portfólio digital para o qual implementou uma API Gateway para gerenciar o acesso às diferentes partes da aplicação. Para garantir a segurança e o funcionamento da aplicação, você adicionou uma chave de acesso `x-api-key` para a parte de DEV do portfólio. Agora, é crucial testar se a configuração está correta, assegurando que a API pública seja acessível sem senha e a parte de DEV exija a chave de acesso correta.

Após realizar um novo deploy da sua API no projeto DEVSPOT, como você pode verificar se a configuração de acesso está funcionando corretamente?

- Alternativa incorreta
    
    Acessando a parte de DEV com a chave de acesso `x-api-key` correta e esperando uma resposta 404 Not Found, para confirmar que a chave está funcionando.
    
- Alternativa incorreta
    
    Fazendo um deploy sem modificar qualquer configuração e esperando que tudo funcione corretamente sem testes adicionais.
    
- Alternativa incorreta
    
    Alterando a chave de acesso `x-api-key` no código fonte e fazendo um deploy, para verificar se a aplicação deixa de funcionar.
    
- Alternativa correta
    
    Realizando uma requisição GET para a API pública e esperando uma resposta 200 OK, e uma requisição GET para a parte de DEV sem fornecer a chave de acesso `x-api-key`, esperando uma resposta 401 Unauthorized.
    
    Esta é a maneira correta de testar a configuração de acesso, pois confirma que a API pública está acessível sem autenticação e a parte de DEV está protegida e exige autenticação.
    
- Alternativa incorreta
    
    Enviando uma requisição POST para a API pública com a chave de acesso `x-api-key` para verificar se a chave é rejeitada, como esperado.
    

Parabéns, você acertou!