Testamos a API e a deixamos completa e funcionando. Ela é exclusiva da nossa conta na AWS, por isso, não conseguimos tirá-la de lá, movê-la para algum outro lugar, para outra conta ou compartilhar com outras pessoas, correto?

Na verdade, conseguimos. É possível fazer esse compartilhamento e conseguimos mover essa API de um lugar para o outro.

Existem apenas algumas coisas importantes a serem lembradas. Nós a criamos dependendo de vários serviços oferecidos pela AWS, portanto, é complicado movê-la entre provedores — por exemplo, retirá-la da AWS, colocá-la no Google, depois na Azure, ou em nosso próprio servidor. Entretanto, compartilhá-la entre contas da AWS é mais fácil.

> Lembrando que, para essa API poder funcionar em outras contas, precisamos criar o _S3_, a _Lambda_, o _DynamoDB_ e todas as permissões que temos.

## Compartilhando a API

Vamos para a página da AWS pelo navegador, acessar a aba lateral esquerda e clicar em "APIs". Na tela central, vamos selecionar a nossa API "ColecaoDeFotos" e clicar em estágios, novamente na aba lateral.

Na tela central veremos a tela "Estágios" que possui duas abas. Na aba esquerda, onde temos as opções "Dev" e "Prod", vamos selecionar esta última para o estágio de produção. Acima da aba direita, temos o botão de lista suspensa "Ações de estágio", no qual selecionaremos "Exportar".

Isso vai abrir uma janela modal, na qual ele vai gerar um arquivo de texto contendo todas as informações da API, igual tínhamos na API base, que inclusive era uma API em _Swagger_ e ela estava em YAML. Vamos repetir essa configuração, clicando nas opções "Swagger" no campo "Tipo de especificação de API" e "YAML" no campo "Formato".

Mais abaixo, na seção "Extensões", podemos também exportar sem nenhum tipo de extensão, selecionando a opção "Exportar sem extensões". No canto inferior direito da janela, vamos clicar no botão "Exportar API", o qual exibirá uma janela com o explorador de arquivos, solicitando o local de download. Vamos manter na pasta "Downloads" e clicar em "Salvar".

Vamos abrir a API que salvamos, `ColecaoDeFotos-Prod-swagger.yaml`, no Visual Studio Code, só para verificar como ela está aparecendo.

Em seu interior, temos a mesma versão do _Swagger_, a 2.0, e o mesmo título da API, "ColecaoDeFotos". Abaixo destes, temos o `host` com o local por onde a pessoa deve que acessar, o `basePath` com o ambiente selecionado — nesse caso, o de produção, e todos os _endpoints_ com seus métodos: `post`, `delete`, `get` e assim por diante.

Além disso, cada método indica, no bloco `security`, a necessidade de uma `api_key`.

Concluímos que a API está completa nesse arquivo YAML. Podemos salvá-lo no _GitHub_ ou num repositório à nossa escolha, já que ele informa que existe uma chave de API, **mas não traz essa chave**.

Isso é muito importante, porque **nenhum tipo de chave pode ser salva em repositórios**. Se salvarmos esse arquivo como um backup, por exemplo, no _GitHub_, esse arquivo não pode ter a chave de API salva dentro dele. Porque se acontecer alguma coisa e alguém achar essa chave, a pessoa vai ter acesso não só à chave de API, como a toda a documentação e referências que ela possui. Isso é um problema de segurança gigantesco.

Agora que temos esse arquivo, podemos salvá-lo ou compartilhá-lo com outras pessoas, carregá-lo em outras contas AWS e estudá-lo para ver como podemos criar APIs diretamente pelo _Swagger_, caso queiramos.

Com isso, cumprimos o objetivo proposto no início do curso: subir uma API na qual conseguimos guardar, deletar e pesquisar imagens no _S3_, sem subir nenhum servidor e protegendo a parte administrativa da API com uma chave de segurança.