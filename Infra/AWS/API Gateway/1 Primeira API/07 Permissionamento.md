Nesse momento já temos o Bucket do S3 criado, mas a nossa API não tem permissão para acessar esse bucket. Sendo assim, sua tarefa é ir até o IAM e crie uma política e uma função para manejar essas permissões.

Você já fez essa atividade? Caso contrário, vamos lá! Se tiver dúvidas quanto ao procedimento, basta clicar em “Opinião da pessoa instrutora”.

Para começar, vá até o IAM através da barra de pesquisa na parte superior da tela. Em seguida, utilize o painel lateral esquerdo para encontrar a opção "Gerenciamento de acesso", dentro de onde temos a opção de "Políticas" e "Funções".

Acesse a opção de "Políticas" e clique para criar uma nova política. Depois selecione qual o serviço **deve ser acessado**, clique em “Próximo” e selecione "Todas as ações do S3 (s3:*)" para dar acesso a todas as ações para a API.

Agora devemos limitar essas ações do S3 a apenas um bucket. Na área de "Recursos", selecione "Específico" e encontre a opção "Bucket", clique em "adicionar ARN" e cole o ARN do Bucket. Na sequência, encontre a opção "Object" e marque a opção "qualquer".

Crie, então, um nome para a política, preferencialmente começando com o nome da aplicação que você está criando, o que facilita a busca por ela mais tarde. Crie a política.

Siga para as funções e clique em "Criar perfil", selecione **qual serviço vai poder usar a política**, no nosso caso, o API Gateway, siga até o final e dê um nome para a função, começando com o nome da aplicação, e crie a função.

Entre na função que acabou de ser criada e clique em "Adicionar permissões" e "Anexar políticas", busque pelo nome da aplicação e selecione a política recém-criada. Por fim, clique em "Adicionar permissões".

Nesse momento, a função já tem permissão para acessar o S3 e o API Gateway já adquire essa função.