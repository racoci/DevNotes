Vamos acessar "Instâncias > Instâncias". Lá, selecionaremos a primeira das duas instâncias com o nome "-". Depois, clicaremos em "Estado da instância > Encerrar instância". A partir de agora, quando atualizarmos a página, teremos apenas uma instância executando.

Em pouco tempo, nosso grupo de _auto scaling_ perceberá que ela não está mais funcionando. Quando isso acontecer, uma nova instância será criada.

Enquanto isso, vamos lidar com políticas de escalonamento. Para preparar nosso sistema para um evento especial como a _black friday_, por exemplo, temos duas alternativas: a primeira é lidar com dados históricos, fazendo configurações preditivas.

Como não temos dados históricos, ficaremos com a segunda opção, que consiste em fazer a utilização de maneira dinâmica. Essa política usa métricas variadas, como o uso da CPU, por exemplo. Em outras palavras, podemos definir que uma nova instância seja criada sempre que atingirmos 50% de uso da CPU.

Acessando "Grupo Auto Scaling > sistema-web > Escalabilidade automática", poderemos lidar com as "Políticas de escabilidade dinâmica". Clicaremos em "Criar política de escalabilidade dinâmica". O "Tipo de política" escolhido será "Escalabilidade de monitoramento do objetivo". O nome dela será "Política de CPU".

Em "Valor de destino", vamos inserir 10: isso significa que, quando atingirmos 10% da CPU, criaremos uma nova instância. Agora, quando a CPU ultrapassar 10%, teremos a criação de novas máquina virtuais, mas sempre respeitando a capacidade máxima.

Agora nós já temos um bom domínio do que é possível fazer com _EC2_. No próximo vídeo, aprenderemos a utilizar a _AWS CLI_.