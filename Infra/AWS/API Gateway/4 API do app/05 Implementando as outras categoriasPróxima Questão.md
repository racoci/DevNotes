Nós já implementamos a primeira consulta, por `assunto`. Agora chegou a sua vez. Para podermos buscar pelas informações desejadas entre as imagens, você vai implementar a consulta por outros parâmetros.

Vamos lá? Caso tenha dúvidas de como fazer isso, clique na seção “Opinião da pessoa instrutora”.

Para isso, crie um endpoint em `/fotos/consulta`, entre em `solicitação de integração` e vá até os `Modelos de mapeamento`. Verifique se o campo `tipo de conteúdo` está com `application/json` e coloque o json a seguir no campo `Corpo do modelo`.

```bash
 {
  "TableName" : "***** TABLE NAME *****",
  "FilterExpression" : "assunto = :v1 AND colecao = :v2",
  "ExpressionAttributeValues" :  {
    ":v1" : { "S" : "$input.params('assunto')" },
    ":v2" : { "S" : "$input.params('colecao')" }

  }
 }
```

Na sequência, salve as alterações.