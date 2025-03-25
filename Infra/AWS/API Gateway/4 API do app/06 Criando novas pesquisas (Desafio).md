Agora que você já implementou todos os métodos disponibilizados pela equipe de Dev, você pode criar outros métodos para a implementação, o método de funcionamento do Json é:

- Nome da tabela que vamos usar:

```markdown
  "TableName" : "***** TABLE NAME *****",
```

- Quais parâmetros vamos colocar na requisição. No caso, definimos `v1` como uma variável com o parâmetro `assunto` e `v2` como o parâmetro `colecao`.

```bash
  "ExpressionAttributeValues" :  {
    ":v1" : { "S" : "$input.params('assunto')" },
    ":v2" : { "S" : "$input.params('colecao')" }
```

- Quais filtros que queremos aplicar na tabela, sendo `v1` o valor do parâmetro `assunto` e `v2` do parâmetro `colecao`, com `"assunto = :v1` e `colecao = :v2` o que será buscado no banco de dados.

```json
  "FilterExpression" : "assunto = :v1 AND colecao = :v2",
```

Com esse funcionamento, realize outras buscas, por exemplo, por todos os campos ou um campo específico que não foi implementado ainda.

Continue com os seus estudos, e se houver dúvidas, não hesite em recorrer ao nosso fórum!