Vimos nessa aula como configurar um balanceador de carga para dividir as requisições entre duas instâncias nossas.

Para onde um load balancer consegue redirecionar o tráfego?

- Alternativa incorreta
    
    Diretamente para instâncias EC2.
    
    Precisamos configurar algo antes do tráfego chegar a alguma instância.
    
- Alternativa incorreta
    
    Diretamente para IPs.
    
    Precisamos configurar algo antes do tráfego chegar a algum IP.
    
- Alternativa correta
    
    Para grupos de destino (target groups).
    
    Para usarmos o load balancer da AWS nós precisamos definir um target group que pode ser para instâncias, IPs, etc.