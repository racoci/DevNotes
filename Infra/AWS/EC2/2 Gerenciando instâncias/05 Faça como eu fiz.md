Nessa aula nós aprendemos mais sobre o modelo de regiões da AWS além de termos também visto como criar uma instância já com software pré-instalado.

Chegou a hora de você colocar em prática o que vimos neste capítulo e praticar a gestão de instâncias EC2.

Caso tenha dúvidas, confira o andamento do seu projeto clicando na **Opinião do Instrutor**.


1. Encerre a instância criada no capítulo anterior;
2. Crie uma nova instância e na sessão de imagem, clique em “Procurar mais AMIs” para selecionar uma imagem diferente;
3. Em “AMIs do AWS Marketplace” procure por “nginx” e selecione a imagem gratuita chamada “NGINX Open Source packaged by Bitnami”;
4. Continue a criação da instância normalmente, atrelando a ela os grupos de segurança já criados;
5. Dê um nome (algo como “nginx”) para a instância recém criada;
6. Nos detalhes da instância, clique para acessar o endereço de DNS público dessa instância. Na aba aberta, substitua “https” por “http”. A página de boas-vindas da imagem deve ser exibida com sucesso;
7. Se conecte, via ssh, à instância usando o usuário “bitnami”.