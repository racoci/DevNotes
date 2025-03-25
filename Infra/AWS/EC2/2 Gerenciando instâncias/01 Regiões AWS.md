Vamos continuar nosso aprofundamento do _AWS EC2_.

É hora de aprender mais um pouco sobre as regiões da _AWS_. Vamos acessar "EC2 > Instâncias > Instâncias > Zona de disponibilidade". Nossa zona de disponibilidade é nossa região, "us-east-1" com um d ao final, ficando "us-east-1d".

Em uma nova aba, acessaremos [https://aws.amazon.com](https://aws.amazon.com/). Vamos descer até que encontremos o mapa abaixo de "Rede global de regiões da AWS". No mapa, há vários pontos pelo mundo, que representam as regiões da _AWS_.

Vamos clicar no ponto de São Paulo. Quando passamos o cursos sobre esse ponto, descobrimos que dentro dessa região há três zonas de disponibilidade. Essas diferentes zonas podem estar em andares, ou até mesmo prédios, diferentes.

Quando os servidores de uma zona caem, não necessariamente os das outras zonas cairão. Essa é uma forma a mais de termos redundância.

Poderíamos criar uma instância em uma zona de disponibilidade, outra em outra zona e ter um _load balancer_ à frente, dividindo a carga entre as duas. Dessa forma, se uma zona sair do ar, a instância continua a funcionar através da outra.

Assim, garantimos serviços mais tolerantes a falhas.

> Obs: As zonas de disponibilidade são independentes. Elas não estão diretamente ligadas, mas podemos viabilizar sua comunicação manipulando as configurações de rede, como vimos no treinamento de _VPC_.

No mapa, os pontos verdes representam regiões existentes e os em laranja regiões que serão criadas.

No próximo vídeo, vamos bater um papo sobre instâncias pré-configuradas.