Chegou a hora de você colocar em prática o que vimos neste capítulo e praticar a gestão de instâncias EC2.

Caso tenha dúvidas, confira o andamento do seu projeto clicando na **Opinião do Instrutor**.

Ver opinião do instrutor

### Opinião do instrutor

1. No console da AWS, busque por IAM. Neste serviço, crie um novo usuário com chave de acesso e dê a ele permissões de admin;
2. Instale a AWS CLI em seu sistema operacional seguindo o passo a passo exposto da documentação;
3. Execute o comando `aws configure` para configurar o acesso da CLI à sua conta;
4. Cole a chave de acesso e depois a chave secreta. Ambas chaves são disponibilizadas no momento da criação do usuário (etapa 1). Deixe as demais opções como padrão;
5. Execute `aws ec2 describe-instances --query="Reservations[*].Instances" --filters="Name=instance-state-name,Values=running"` para ver a lista de todas as instâncias que estão executando;
6. Interrompa uma das instâncias com `aws ec2 stop-instances --intance-ids {id da instância}`. Confira que a instância está interrompida parada e que outra será criada pelo auto scaling group.