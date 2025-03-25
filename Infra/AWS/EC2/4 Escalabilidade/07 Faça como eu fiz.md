Chegou a hora de você colocar em prática o que vimos neste capítulo e praticar a gestão de instâncias EC2.

Caso tenha dúvidas, confira o andamento do seu projeto clicando na **Opinião do Instrutor**.

1. Selecione a instância “nginx” e a duplique através da opção “Executar mais como essa”. Crie essa nova instância em outra zona de disponibilidade e chame-a de “nginx-2";
2. Em “Load balancers” crie um novo “Application Load Balancer” nas zonas de disponibilidade de suas 2 instâncias;
3. Adicione a esse load balancer o grupo de segurança “acesso-web” para que ele seja acessível via HTTP;
4. Na parte de roteamento do load balancer, crie um novo target group com as 2 instâncias e selecione esse target group como ação do load balancer;
5. Com o load balancer criado e ativo, acesse o DNS dele para garantir que tudo está funcionando;
6. Edite o HTML em `/opt/bitnami/nginx/html/index.html` em suas duas instâncias com conteúdos diferentes para podermos diferenciá-las;
7. Após editar e salvar, acesse o endereço do load balancer de novo e ao atualizar a página várias vezes você deve ver o conteúdo sendo alternado, mostrando que cada requisição chega em uma instância diferente;
8. Desligue uma das instâncias e veja que o load balancer continua acessível, mandando todo o tráfego para a instância que está de pé;
9. Caso você possua um domínio, crie uma entrada do tipo CNAME apontando para o DNS do load balancer e após a propagação, acesse através desta entrada;
10. Crie um novo grupo de auto scaling usando um modelo de execução. Crie esse modelo com a imagem que criamos anteriormente e as configurações de hardware que já estamos habituados;
11. Selecione quais zonas de disponibilidade serão utilizadas por esse grupo de auto scaling (lembre-se de utilizar as mesmas que selecionou no load balancer, senão o load balancer não conseguirá redirecionar o tráfego);
12. Anexe esse grupo de auto scaling ao nosso balanceador de carga existente;
13. Com o grupo criado, modifique a capacidade desejada e mínima para 2 e máxima para 3;
14. Remova do target group as 2 instâncias que adicionamos manualmente anteriormente. Também encerre essas instâncias já que não serão mais utilizadas;
15. Em nosso grupo de auto scaling, na aba de escalabilidade automática, define uma plítica de escalabilidade dinâmica para criar mais instâncias quando o uso de CPU passar de 10%.