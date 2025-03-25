Agora que você já tem uma URL para acessar a API, abra o Postman e envie uma imagem. Depois verifique se ela apareceu no bucket com o nome correto e apague a imagem através da API. Ao fim, verifique o funcionamento do método que criamos.

Você já fez essa atividade? Caso contrário, vamos lá! Se tiver dúvidas quanto ao procedimento, basta clicar em “Opinião da pessoa instrutora”.

Depois do deploy da API temos uma URL disponibilizada para o acesso, mas lembre-se de pegar a URL do método diretamente, pois assim evitamos o problema de por acaso esquecer de colocar o ambiente ou o endpoint na URL.

Com a URL certa em mãos, abra o Postman e cole-a no campo de requisições, apague o `{item}` no final da URL e troque o tipo de requisição, no caso, de GET para POST. Logo abaixo do campo de URL temos o campo de "body" onde temos a opção "binary" para carregar um arquivo binário, ou seja, as imagens.

Escolha uma imagem, copie o seu nome e a selecione. Coloque o nome da imagem no final da URL e faça a requisição. Entre no Bucket e verifique se a imagem está disponível, com o nome correto e se o objeto no bucket está com um tamanho diferente de zero.

Agora volte no Postman, crie uma nova guia e troque o tipo de requisição de GET para DELETE, copie apenas a URL do método POST e execute uma nova requisição. Verifique se a imagem sumiu do Bucket.