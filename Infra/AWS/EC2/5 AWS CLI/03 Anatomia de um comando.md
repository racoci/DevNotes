Vimos nesse vídeo como executar comandos que gerenciam nossas instâncias EC2 usando o AWS CLI.

Como é o “formato” de um comando usando a AWS CLI?

- Alternativa correta
    
    ```undefined
    aws servico acao parametros
    ```
    
    Para o serviço EC2, por exemplo, sempre começamos o comando com `aws ec2`. Para executar a ação de parar uma instância, fazemos `aws ec2 stop-instances --instance-ids {id da instância}`. Sendo assim, o serviço é `ec2`, a ação é `stop-instances` e os ids são os parâmetros.
    
- Alternativa incorreta
    
    ```undefined
    aws servico parametros acao
    ```
    
    A ordem de cada parte do comando está incorreta. Seguindo essa lógica, o comando para parar uma instância seria `aws ec2 ec2 --instance-ids {id da instancia} stop-instances`, o que está errado.
    
- Alternativa incorreta
    
    ```undefined
    aws acao servico parametros
    ```
    
    A ordem de cada parte do comando está incorreta. Seguindo essa lógica, o comando para parar uma instância seria `aws stop-instances ec2 --instance-ids {id da instancia}`, o que está errado.