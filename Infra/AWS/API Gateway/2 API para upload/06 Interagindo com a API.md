Agora que temos a API pronta, podemos começar a testá-la. Assim, verificamos se cometemos algum erro ou se está funcionando corretamente.

Começaremos testando os métodos `POST` e `DELETE`. Por meio do `POST` vamos inserir as imagens e com o `DELETE` remover as imagens, caso necessário.

# Testando o método `POST`

Na AWS, na área de estágios, clicamos no método `POST`. Na lateral direita, copiamos a **URL de invocação desse método**.

Feito isso, abriremos outro software, o Postman. Com ele conseguiremos **montar requisições** e assim, verificar se a API está funcionando.

> Ao abrir o Postman, se o menu de histórico, na lateral esquerda da tela, estiver aberto, pressione "CTRL + " para escondê-lo.

Para fazer a requisição, na lateral superior esquerda da tela, precisamos escolher o tipo de requisição. Clicamos e selecionamos a opção `POST`. No campo ao lado, colamos a URL.

Feito isso, podemos começar a enviar as imagens. Mas, antes, vamos verificá-las. Então, abrimos a pasta das imagens no computador. Repare que o nome da imagem possui a mesma estrutura, um ID, o que ela é, o tema e a escola. Por exemplo, "1-Capa_Artigo-BI-DataScience". São um total de sete imagens. Vamos testar a imagem um. Então, copiamos o caminho em que ela está no computador.

> Lembrando que disponibilizamos as imagens no GitHub. Para testar, basta baixá-las e testá-las no Postman.

Feito isso, voltamos ao Postman. Mas, onde vamos inserir a imagem, é na URL? Na verdade, não. Logo abaixo da URL, encontramos algumas abas com os parâmetros.

Clicamos em "Body" e depois selecionamos a opção "binary", pois esse é um conteúdo binário. NA lateral esquerda, clicamos em "Select fire". Abre uma janela, na qual clicamos na imagem 1 e depois em "Abrir".

> Lembre-se de copiar o nome da imagem, pois precisamos trocar o `item` da URL e passar esse caminho.

Então, no campo de URL, apagamos o `{item}` e colamos o caminho da imagem `1-Capa__Artigo-BI-DataScience.jpg`. Em seguida, cicamos no botão "Send" na lateral superior direita da tela.

Feito isso, visualizamos a mensagem abaixo:

```json
{
    "mensagem": "Envio com sucesso"
}
```

Vamos verificar o _bucket_. Voltamos para AWS no navegador e acessamos o Bucket S3 de `colecaodefotos-leo`. Clicamos na aba "Objetos" e depois no ícone indicado por uma seta circular, na lateral superior esquerda, para recarregar.

Repare que não está aparecendo nenhum objeto. O que será que aconteceu? O envio foi feito com sucesso, a API recebeu a imagem, porém ela não veio para o _bucket_. Então, provavelmente temos algum problema com as permissões.

Para conferir, na AWS, o IAM `colecaodefotos-aPIgateway-S3`. Ao descer a tela, clicamos em "corlecaodefotos-S3-policy". Descemos a tela até a seção **Permissões definidas nesta política** e clicamos em "Editar".

Na nova janela, selecionamos o editor "Visual". Abaixo, identificamos o S3 com 15 ações e S3 com Todas as ações. Clicamos na segunda opção. A opção **Permitir todas as ações**, está selecionada, assim como os Recursos específicos.

Ao descermos a tela, descobrimos que esse erro aconteceu, pois não demos permissão para mexer nos objetos. A API pode listar qual _bucket_ existe, ler informações do _bucket_, criar um novo, deletar, mas mexer nos objetos não.

Para mudarmos isso, na lateral direita, selecionamos o box "Qualquer", para liberar o uso de qualquer objeto dentro do _bucket_. No fim da página, clicamos em "Próximo" e na nova janela em "Salvar alterações".

Vamos conferir se agora funcionou. Voltamos para o Postman e clicamos em "Send". Feito isso, a mesma mensagem aparece. Em seguida, abrimos o S3, em Objetos, e clicamos no botão para atualizar. Feito isso, a imagem aparece, isso significa que conseguimos subir nosso primeiro arquivo.

# Testando o método `DELETE`

Suponhamos que subimos a imagem errada para testarmos o método `DELETE`. Então, no Postman, abrimos uma nova aba clicando no símbolo "+", no centro superior da tela.

Na nova aba, selecionamos o método `DELETE`. Feito isso, voltamos na aba em que usamos o método `POST`, copiamos a URL e colamos na aba `DELETE`. Feito isso, clicamos em "Send".

> Como queremos apagar a foto, não precisamos indexá-la.

Feito isso, a mensagem que aparece é a seguinte:

```json
{
        "mensagem": "Deletado com sucesso"
}
```

No navegador, acessamos o bucket, na aba Objetos, clicamos no botão para atualizar. Feito isso, a imagem some. Deu certo. Nossa API está funcionando.

Ficamos sabendo que a equipe de desenvolvimento está terminando a nova parte da API. Em sequência, descobriremos no que estão trabalhando.

**Te esperamos lá!**