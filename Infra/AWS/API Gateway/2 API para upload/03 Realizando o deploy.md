Atualmente, já temos os recursos que nos propusemos a criar na API. Temos o método `POST`, onde podemos enviar as imagens para serem armazenadas no _bucket_, e o método `DELETE`, para apagar essas imagens caso haja algum problema com elas.

Mas, como acessamos essa API? Atualmente, não temos nenhum link que possamos acessar. Então, dentro da AWS, precisamos implementar a API. Sem a implementação, ela não estará disponível, ou seja, não servirá para nosso propósito. Sendo assim, faremos a implementação.

# Implementando a API

Na AWS, acessamos a página do API Gateway. No menu lateral esquerdo, na seção "API: ColecaoDeFotos", clicamos em "Recursos". No centro da tela, abre uma janela de recursos presentes na API, onde temos todos os métodos.

Na parte superior direita, clicamos no botão laranja "Implantar API". Na janela que abre, precisamos definir o **Estágio**. Nesse primeiro momento, criaremos um estágio de `DEV`, pois não testamos a API e ela não está pronta para ser pública.

Então, selecionamos "Novo estágio" e abaixo o nomeamos de `DEV`. Abaixo, no campo **Descrição da implantação**, escrevemos "Primeira versão da API", para sabermos o que está sendo feito. Feito isso, clicamos no botão "Implantar". Assim, a implementação é concluída com sucesso e a API está no ar.

Repare que agora estamos na aba "Estágios". No centro da tela, temos o `Dev` selecionado. Na lateral direita da tela, descemos e encontramos o "Invocar URL", é a partir dessa URL que podemos acessar a API.

Repare que essa URL não é muito profissional, é difícil lembrar desse caminho. Uma solução, caso você tenha um domínio, é direcioná-lo para a API.

> Por exemplo, se tivermos um domínio com o nome do instrutor, como "leonardosartorello.com", podemos direcioná-lo para a API, assim fica mais fácil de gerenciar.

Sugerimos que você não pegue essa URL e sim a **URL do método**. Para isso, abra a janela "Dev > / > /bucket/{item}" e selecione o método que você quer, assim você encontrará a URL. Caso contrário, podem acontecer alguns erros, como o _missing token_, token faltando.

O passo seguinte é testar os métodos. **Te esperamos no próximo vídeo!**