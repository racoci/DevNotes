Neste momento, o API Gateway já tem permissão para acessar o banco de dados. No entanto, nosso banco de dados está vazio. Se tivéssemos que preenchê-lo manualmente, seria um processo tedioso e complicado. Além de ser uma tarefa extensa, poderíamos cometer erros e gerar conflitos dentro do banco de dados.

Para evitar esse tipo de problema, sugerimos criar uma **função** para preencher esse banco de dados **automaticamente**. Vamos automatizar o trabalho e deixar a função cuidar do banco de dados.

Mas onde vamos executar essa função? Precisamos criar um servidor, um container, hospedá-lo em algum lugar? Não! Vamos continuar não manejando nenhum servidor. Vamos usar o **Lambda da AWS**.

O Lambda é uma maneira de executar pequenos trechos de código sem ter que nos preocupar com os servidores. Ele tem algumas características interessantes, como não ficar rodando o tempo todo, sendo executado apenas quando é chamado.

## Criando uma nova função no Lambda

Na página inicial do Lambda, à direita, temos o botão "**Criar uma função**". Vamos clicar nele e, na nova tela, selecionar a opção **Criar do zero**.

Primeiro, inserimos o **nome** da função. Vamos começar com o nome da nossa aplicação, "Coleção de Fotos". Depois, com o que essa função vai interagir? Com o "DynamoDB". O que ela executa? Atualização de informações. E quem é a pessoa responsável pela função? No caso do instrutor, Leonardo. Então, o nome fica "_colecaodefotos-dynamodb-atualizar-leo_".

Depois, em "Tempo de execução", precisamos definir a **linguagem** da escrita dessa função. Para isso, vamos descobrir qual ambiente precisamos criar. No projeto do GitHub, temos a função que vamos utilizar, adiantada pela equipe de desenvolvimento. Temos o arquivo `lambda.py`, ou seja, a função foi escrita em **Python**.

## Código da função Lambda

Vamos entender como esse arquivo funciona. Primeiro, ele importa algumas bibliotecas para podermos trabalhar com o DynamoDB:

> `lambda.py`

```py
import boto3

resource_dynamodb = boto3.resource('dynamodb')
```

E toda vez que o Lambda inicia uma função, ela inicia pelo `lambda_handler()`. Dentro do `lambda_handler()`, pegamos o `arquivo` com que estamos trabalhando e qual `evento` está acontecendo. Depois, chama a função `main()`.

```py
def lambda_handler(event, context):
    arquivo = event['Records'][0]['s3']['object']['key']
    evento = event['Records'][0]['eventName'].split(':')
    evento = evento[1]
    main(arquivo,evento)
```

Na função `main`, a primeira coisa que fazemos é **extrair** os atributos do arquivo e, em seguida, **atualizar** o banco de dados:

```py
def main(arquivo,evento):
    atributos = extrai_arquivo(arquivo)
    atualiza_database(atributos, evento)
```

A **função de atualização do banco de dados** tem um ponto importante: `Table()` recebe `TABLE NAME` entre cinco asteriscos: `'***** TABLE NAME *****'`:

```py
def atualiza_database(atributos,evento):
    table = resource_dynamodb.Table('***** TABLE NAME *****')
    if evento == 'Put':
        response = table.put_item(
            Item={
                'id': int(atributos[0]),
                'assunto': atributos[1],
                'colecao': atributos[2],
                'descricao': atributos[3]
            }
        )
    if evento == 'Delete':
        response = table.delete_item(
            Key={
                'id': int(atributos[0])
            }
        )
# código omitido
```

Precisamos substituir essa parte pelo **nome da nossa tabela do DynamoDB**. Caso contrário, a função não saberá qual banco de dados atualizar.

Na condição dessa função, se `evento` for `'Put'`, entramos com os dados, ou seja, colocamos um item. Se for `'Delete'`, apagamos os dados.

Vamos copiar todo o código da função Lambda, pois vamos precisar dele. Não podemos esquecer do `import` do começo do arquivo e nem do `atualiza_database` no final.

Voltamos para o AWS Lambda e, no campo "Tempo de execução", selecionamos o **ambiente** que vamos usar: **Python 3.12**.

> Com o passar do tempo, a AWS vai adicionando novos ambientes. Então, no momento em que você está acompanhando esta aula, é possível que o Python 3.12 esteja na seção "Outros compatíveis" dessa lista suspensa, onde temos outras versões mais antigas. Ou ele já pode ter sido depreciado e removido da AWS. Então, se o 3.12 não está mais disponível para você, selecione a **versão mais recente** e tente executar.

No campo de **Arquitetura**, podemos deixar selecionada a opção "x86_64", pois não precisamos rodar em ARM.

Por fim, descemos ao final da página e clicamos em "**Criar função**". Esse processo de criação da função pode demorar um pouco.

Ao terminar o processo, é possível alterar o código da função e suas configurações. Já copiamos o código da função no GitHub, então vamos descer a página até a aba "**Código**" da função "_colecaodefotos-dynamodb-atualizar_".

Na área do código, vamos substituir o código padrão pelo nosso, colando-o na aba `lambda_function`.

Agora precisamos substituir o nome da tabela (`TABLE NAME`) na linha 20 pelo nome da nossa tabela do DynamoDB: `'colecaodefotos-leo'`:

> `lambda_function` no Lambda AWS

```py
import boto3

resource_dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    arquivo = event['Records'][0]['s3']['object']['key']
    evento = event['Records'][0]['eventName'].split(':')
    evento = evento[1]
    main(arquivo,evento)


def extrai_arquivo(arquivo):
    atributos = arquivo[:-4]
    atributos = tuple(atributos.split('-'))
    return (atributos)


def atualiza_database(atributos,evento):
    table = resource_dynamodb.Table('colecaodefotos-leo')
    if evento == 'Put':
        response = table.put_item(
            Item={
                'id': int(atributos[0]),
                'assunto': atributos[1],
                'colecao': atributos[2],
                'descricao': atributos[3]
            }
        )
    if evento == 'Delete':
        response = table.delete_item(
            Key={
                'id': int(atributos[0])
            }
        )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f'DB atualizado: {atributos}')
    else:
        print('ERRO de atualizacao')

def main(arquivo,evento):
    atributos = extrai_arquivo(arquivo)
    atualiza_database(atributos, evento)
```

Com isso, já temos nossa função com o código atualizado. Por fim, logo acima do editor de código, vamos clicar em "_**Deploy**_" para realizar o _deploy_ do código.

E pronto! O código já está atualizado dentro da função.

Em seguida, precisamos adicionar um **gatilho** para indicar quando a função deve ser executada. Faremos isso no próximo vídeo!