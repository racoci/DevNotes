Neste momento, já temos a chave criada e o plano de utilização. No entanto, precisamos associá-los à API.

É importante lembrar que precisamos associá-los apenas à parte administrativa da API, pois queremos que a parte pública permaneça sem nenhum tipo de chave, permitindo que qualquer pessoa possa entrar e pesquisar dentro das nossas imagens.

## Associando a Chave à API

Para associar a chave à parte administrativa da API, temos a tela "Planos de utilização" exibindo o plano de utilização que já criamos. Vamos entrar nele, clicando em cima do seu nome — nesse caso, "Administrativo". Isso exibirá a tela "Detalhes do plano de uso".

Vamos descer essa tela até a seção "Estágios associados" e clicar no botão "Adicionar estágio", o que exibirá a tela "Detalhes do estágio".

Será solicitado qual é a API no campo "API". Selecionaremos "ColecaoDeFotos". No campo "Estágio", escolheremos no botão de lista suspensa o estágio dessa API, entre as opções "Dev" e "Prod" (produção). Vamos entrar no estágio de produção, portanto, vamos selecioná-lo.

Por fim, clicaremos no botão "Adicionar ao plano de uso", na parte inferior direita. Com isso, o estágio já está adicionado ao plano de uso, e retornaremos para a tela dos detalhes do plano.

Na seção "Estágios associados", temos uma guia com o nome desta seção e, à sua direita, outra guia chamada "Chaves de API associadas". Vamos selecioná-la.

Na seção "Chaves de API associadas", vamos adicionar uma chave de API, selecionando o botão com esse nome. Isso exibirá a tela 'Detalhes da chave de API".

Na opção "Tipo", manteremos a opção "Adicionar chave existente" selecionada, pois já criamos a chave e não precisamos criar de novo. No campo "Chaves de API", clicaremos no botão de lista suspensa e selecionaremos "colecaodefotos-administrativa". Por fim, vamos ao canto inferior direito e clicaremos no botão "Adicionar chave de API", o que nos fará voltar para a tela de detalhes do plano de uso.

Neste momento, a chave está valendo, mas não é necessário usá-la em nenhum momento da API. Vamos forçar essa utilização.

## Forçando o Uso da Chave de API

Vamos ao menu lateral do API Gateway, selecionar a opção "APIs" e, na tela central, selecionar a API "ColeçãoDeFotos". Na tela "Recursos", fecharemos o menu lateral para adicionar um pouco de espaço e veremos duas áreas: à esquerda, a árvore de recursos, e à direita, os detalhes do recurso.

Na seção esquerda, selecionaremos o método `DELETE`. Na seção direita, desceremos a tela até a seção "Configurações de solicitação de método" e vamos clicar no botão "Editar", no canto direito.

Isso exibirá a tela "Editar solicitação de método". Na seção "Configurações de solicitação de método", temos a parte relacionada a chaves e autorização de acesso.

No campo "Autorização", manteremos a opção "Nenhuma" selecionada. Este campo possui a opção "AWS IAM" que serve para autorizar alguém a acessar via AWS IAM.

O campo "Validador de solicitação" serve apenas para verificar se a solicitação chegou corretamente. Também podemos manter a opção "Nenhuma". Em seguida, marcaremos a caixa de seleção "Chave de API obrigatória".

Pronto, isso é o que precisamos fazer. Vamos descer até o final da tela e clicar em "Salvar", no canto direito. Com isso, o `DELETE` está protegido e voltaremos para a tela de recursos.

Vamos fazer o mesmo processo em `POST`, clicando nele pela aba esquerda com a árvore de recursos. Na aba direita, desceremos até "Solicitação de método", clicaremos em "Editar" e marcaremos a caixa de seleção "Chave de API obrigatória". Vamos até o final e clicaremos em "Salvar".

Com isso, temos os dois métodos com a chave obrigatória.

Na tela de recursos, acima das duas abas, vamos clicar no botão "Implantar API", no canto direito. Lembrando que, sem implantar, todas as alterações que estamos fazendo não entram em produção e não são válidas, sendo mantidas apenas no ambiente de teste dentro do AWS.

No momento em que fazemos o _deploy_ da API, tudo passa a valer. Na janela modal "Deploy API", vamos fazer o _deploy_ em produção, selecionando a opção "Prod" no campo "Estágio". No campo "Descrição da implantação", vamos colocar uma descrição:

```plaintext
Implementando a chave de acesso
```

Clicaremos no botão "Implantar", no canto inferior direito, e seremos redirecionados à tela "Estágios".

Com isso, a API, agora em produção, já está com a chave de acesso. A seguir, vamos testar para ver se isso realmente está acontecendo.