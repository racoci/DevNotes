Já finalizamos a configuração e teste da nossa API. Ela já está funcionando! Mas ainda não terminamos. Você se lembra de que comentamos no início que o time de desenvolvimento estava trabalhando em uma **nova atualização**? Ela acabou de sair e vamos implementá-la.

Essa atualização consiste em podermos pesquisar entre as imagens que subimos no _bucket_, ou seja, entre os nossos objetos do S3, para obter **informações** deles, como ID, categoria, escola de origem dos banners, quantas e quais imagens temos, etc.

Para acelerar esse processo, vamos ter que criar algumas coisas para além da nossa API: um **banco de dados** para guardar todas as informações e alguma **aplicação** que vai preencher esse banco de dados de acordo com os objetos que já temos no _bucket_.

Mas, para criar tudo isso, vamos precisar criar servidor, manejar containers e assim por diante? Na verdade, não precisamos nos preocupar, pois vamos utilizar os serviços que a própria **AWS** oferece para fazer tudo isso sem precisar mexer em servidores.

## Arquitetura de uma aplicação com servidores

Para fazer isso, podemos ter um **site** ou um **aplicativo** com a função de consulta das imagens. Esse site vai acessar a nossa **API** e a nossa API, por sua vez, consulta o **DynamoDB**, que será o nosso banco de dados oferecido pela AWS.

E para preencher esse DynamoDB sem ter que entrar nele e preenchê-lo manualmente, vamos ter uma função rodando no **LAMBDA**, um serviço da AWS onde podemos executar nossos códigos também sem nos preocupar com os servidores. Ele vai pegar informações do nosso _bucket_ do S3.

![Diagrama de arquitetura de uma aplicação com servidores, mostrando o fluxo de dados do aplicativo para a API de consulta ao banco de dados e então para o banco de dados DynamoDB. Há também um fluxo de dados do S3 Bucket para o DynamoDB, passando por uma função Lambda. Os ícones são estilizados e representam cada componente: um celular para o APP, símbolos de conexão para a API ConsultaDB, o logotipo do AWS Lambda e um grid que representa o DynamoDB.](https://cdn1.gnarususercontent.com.br/1/795715/cc449545-efc2-4e67-b45d-65971a3277c1.png)

Vamos lá, então? Começaremos pelo banco de dados!

## Criando o banco de dados

Antes de tudo, vamos **entrar** no banco de dados, o DynamoDB.

Para isso, clicamos na barra de pesquisa do menu superior da AWS e pesquisamos por "DynamoDB". Clicamos na primeira opção dos resultados, o que abre uma nova guia na página inicial do DynamoDB.

Vamos clicar diretamente em "**Tabelas**", no menu esquerdo dessa página, depois em "**Criar tabela**", o botão laranja no canto superior direito.

Primeito, vamos inserir o **nome** da tabela. Como padrão, primeiro colocamos o nome da nossa aplicação: "_colecaodefotos_". Depois, colocamos quem cuida da tabela. Nesse caso, o instrutor colocou seu próprio nome depois de um hífen: "colecaodefotos-leo".

> **Note:** o nome da tabela deve ter entre 3 e 255 caracteres, contendo apenas letras, números, sublinhados (_underline_), o hifens (sinal de menos) e pontos, sem vírgulas ou acentuação.

Depois, vamos preencher a **Chave de partição**. Essa chave é um número ou string única para cada imagem. No nosso caso, a nossa chave de partição pode ser o nosso ID, então vamos escrever "_id_" no campo de nome da chave. Nesse caso, vamos indicar que essa chave é um Número, mudando a configuração na lista suspensa à direita do campo de nome.

A **Chave de classificação** é opcional, e não vamos utilizá-la. Ela serve para acelerar alguns tipos de busca, mas nossa tabela não está nem perto de ser grande o suficiente para precisar dessa tipo de chave. Então, vamos pular esse campo.

Depois, temos uma seção de **Configuração da tabela**. Podemos deixar marcada a opção de "Configurações padrão", ou marcar a opção "Personalizar configurações". As configurações padrão funcionam muito bem, habilitando muitos acessos antes de começar a ter problema de tempo de leitura e escrita na nossa tabela. Então, vamos começar com a padrão.

Por fim temos a seção de **Tags**, que também não são necessárias para nós.

Para finalizar, vamos clicar em "**Criar tabela**" no canto inferior direito da tela. Temos a nossa tabela! O processo de criação demora um pouco, por tratar-se de um banco de dados. Assim que ele estiver pronto, podemos começar a utilizá-lo.

Em seguida, precisamos criar as **políticas de acesso** para essa tabela. No momento atual, a nossa API só consegue acessar o S3, mas não consegue acessar o DynamoDB. Vamos ajustar isso no próximo vídeo.