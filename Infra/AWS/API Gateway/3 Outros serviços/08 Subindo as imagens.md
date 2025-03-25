Nesse momento, já testamos e a API está funcionando como deveria com os métodos POST e DELETE, possibilitando a interação com o S3 e com os outros serviços, como o Lambda e o DynamoDB.

Sendo assim, suba as outras imagens para a AWS através da API, e lembre-se de trocar o nome da imagem na URL de requisição, senão a imagem será substituída por uma nova, corrompendo os dados e misturando as informações presentes no DynamoDB.

Se tiver dúvidas, basta seguir para a parte de "Opinião da pessoa instrutora", pois temos um passo a passo para te ajudar neste processo.

Com a URL da API em mãos, abra o Postman e cole-a no campo de requisições, apague o `{item}` no final da URL e troque o tipo de requisição, no caso, de GET para POST.

Logo abaixo do campo de URL temos o campo de "body", no qual temos a opção "binary" para carregar um arquivo binário, ou seja, as imagens, escolha uma imagem, copie o seu nome e a selecione.

Coloque o nome da imagem no final da URL e faça a requisição. Entre no DynamoDB e verifique se as informações estão disponíveis. Repita esse processo até as informações das sete imagens estarem disponíveis no DynamoDB.