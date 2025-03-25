Imagine que você está desenvolvendo um portfólio online para desenvolvedores chamado DEVSPOT. Este portfólio permite que desenvolvedores mostrem seus projetos, habilidades e experiências profissionais. Para armazenar os dados dos usuários e projetos, você decidiu usar o DynamoDB na AWS. Agora, você está na fase de configurar as políticas de acesso ao DynamoDB para garantir que os dados sejam acessíveis de maneira segura e eficiente. Você se lembra de que, durante o curso, aprendeu sobre a importância de configurar corretamente as políticas de acesso através da interface gráfica da AWS.

Você precisa decidir qual política de acesso é mais adequada para permitir que seu aplicativo DEVSPOT acesse o DynamoDB de forma segura. Qual das seguintes políticas de acesso você deve configurar?

Selecione uma alternativa

- Negar acesso ao DynamoDB para todos os usuários.
- Permitir acesso somente leitura ao DynamoDB para usuários autenticados e acesso de escrita para o administrador.
- Permitir acesso somente leitura ao DynamoDB para todos os usuários.
- Permitir acesso total ao DynamoDB para todos os usuários.
- Criar uma política de acesso personalizada que permita operações de leitura e escrita no DynamoDB apenas para o aplicativo DEVSPOT.
	- Esta é a melhor opção, pois permite que o aplicativo realize todas as operações necessárias no banco de dados de forma segura, sem conceder acesso excessivo a outros usuários ou serviços.