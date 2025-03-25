Antes de começar a explorar o que vamos criar e o serviço que vamos utilizar, precisamos fazer um **planejamento**. Vamos organizar tudo para conhecer exatamente o nosso passo a passo.

## Planejamento

Estamos em uma equipe de DevOps e recebemos um pedido da equipe de Front-end para salvar algumas imagens na AWS. Podemos criar diversos métodos diferentes para isso, mas, para acelerar nosso trabalho, sugerimos utilizar o _**API Gateway**_. Dentro dele, vamos **criar uma API** para facilitar o acesso da equipe de Front-end à AWS.

Outra questão importante: onde serão salvas essas imagens que a equipe deseja armazenar? Podemos usar outro serviço da AWS, o **S3**, que é um serviço onde podemos guardar imagens e arquivos sem nos preocuparmos com servidores.

Vamos entender como funciona essa API, como ela vai operar e qual será a sua estrutura. A equipe de Front-end vai acessar diretamente a API, subindo as imagens e a API guarda tudo no _bucket_ do S3. O _bucket_ (balde) é o nome da pasta que temos no S3.

![Fluxograma de coleção de imagens com fundo escuro. À esquerda, a equipe de Frontend se conecta a uma API Bucket que, por sua vez, se conecta a um S3 Bucket.](https://cdn1.gnarususercontent.com.br/1/795715/0d8261c8-3c82-435e-bf52-d28f6c52e229.png)

Mas, por que a equipe de Front-end não acessa diretamente o _bucket_? Temos alguns motivos para isso.

## Vantagens de usar uma API

Primeiro, a questão de **segurança**. Se a equipe de Front-end for acessar diretamente o _bucket_, precisaremos criar usuários para cada pessoa que vai acessar essa função da AWS. E essas pessoas terão acesso completo. Assim, corremos o risco de algum desses usuários ter o login e a senha vazados, o que pode gerar um problema de segurança na AWS.

Além disso, a interface do S3 está sempre mudando. A AWS faz **atualizações de interface** constantemente. Portanto, a API torna tudo isso um pouco mais fácil para a equipe. Uma vez que você aprendeu a usar, não mudará.

Essas são as vantagens em criar uma API para acessar o S3.

> Vale lembrar que a AWS adora atualizar as interfaces. Portanto, pode ser que algum botão ou algo que vamos criar possa mudar de lugar. Mas todas as opções continuarão disponíveis, às vezes em um lugar um pouco diferente.

E também, já vou adiantar uma informação para vocês. A equipe de Front-end, junto com a equipe de Dev, já estão pensando em uma mudança para essa API. Então, talvez ela apareça no meio do curso.

Agora, vamos criar essa API?