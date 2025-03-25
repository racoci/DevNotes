Agora que já configuramos a _AWS_ na nossa linha de comando, vamos descobrir o que podemos fazer.

No terminal, se digitarmos o comando `aws help`, encontraremos uma lista com todos os comando que podemos utilizar. Para que nos aprofundemos, porém, vamos acessar a documentação em [https://docs.aws.amazon.com/cli/index.html](https://docs.aws.amazon.com/cli/index.html).

Acessando o guia do usuário, vamos buscar pelos comandos relacionados ao _EC2_. Vamos voltar ao consolee acessar nossa lista de instâncias. Quando removermos o filtro que mostra apenas as instâncias em execução, veremos que há cinco instâncias criadas.

Voltemos ao terminal. Se apertarmos a tecla "Q", sairemos das ajudas. Vamos executar o comando `aws ec2 describe-instances"`. Isso nos apresentará todas as instâncias. Para filtrarmos os campos que serão trazidos, podemos utilizar o parâmetro `--query="Reservations[*].Instances`.

```sql
aws ec2 describe-instances --query="Reservations[*].Instances
```

Assim, pegaremos apenas as instâncias.

Há também o parâmetro `--filter`. Para executá-lo, precisamos do nome do filtro, que pode ser encontrado com o comando `help`. Podemos verificar os comandos possíveis para as instâncias assim:

```bash
aws ec2 describe-instances help
```

Vamos buscar pelos filtros, digitando `filters` na linha de comando. Depois que localizarmos o nome, vamos copiá-lo e usá-lo no comando abaixo:

```sql
aws ec2 describe-instances --filters="Name=instance-state-name, Values=running"
```

Vamos copiar apenas o _ID_ da instância e adicioná-lo ao comando:

```graphql
aws ec2 describe-instances --filters="Name=instance-state-name, Values=running" -query=Reservations[*].Instances[*].[InstanceId, State]"
```

Assim, trazemos apenas o _ID_ da instância e o seu estado, as duas informações que, no caso, estão entre colchetes.

Vamos tentar derrubar uma das instâncias, para que outra seja criada automaticamente. No vídeo, o instrutor seleciona a instância "i-05249de62f1444f37". Vamos pará-la com a ajuda do comando `aws ec2 stop-instances help`. Assim, receberemos o tutorial de utilização desse comando.

Descobriremos que precisamos passar o parâmetro `--instance-ids` e adicionar o _ID_:

```css
aws ec2 stop-instances help
aws ec2 stop-instances --instance-ids i-05249de62f1444f37
```

A instância, depois disso, será derrubada. Tudo que fazemos pelo navegador, também conseguimos fazer via _CLI_.

Os comandos não são simples de digitar. Por isso, o ideal é que criemos scripts. Para adicionar nossa última ação ao _script_, vamos passar o comando abaixo:

```json
[
        [
                [
                        "i-093b00d8c84926149",
                        {
                                "Code": 16,
                                "Name": "running"
                        }
                [
        [
[
```

Outra maneira de definir a saída em configurando o _output_ como "table" via linha de comando. Para fazer isso, porém, precisaríamos ter apenas um objeto. No nosso caso, temos dois `InstanceId` e `state`. Basta remover algum dos dois.

É possível definir o formato via linha de comando. Para defini-lo em _yaml_, por exemplo, faríamos assim:

```graphql
aws ec2 describe-instances --filters="Name=instance-state-name, Values=running" -query=Reservations[*].Instances[*].[InstanceId, State]" --output yaml
```

> Obs: Também é possível fazer tudo isso enviando chamadas para _APIs_.