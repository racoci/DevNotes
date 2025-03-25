Vamos conhecer alguns serviços satélites do _EC2_, como o de imagens, por onde começaremos.

Quando criamos nossa instância a partir de uma imagem, precisamos aguardar o registro da conta no serviço de imagem. Isso mostra que essa função está além das instâncias do _EC2_.

Se selecionarmos qualquer instância disponível, podemos clicar em "Ações > Imagem e modelos > Executar mais como esta". Essa opção multiplica as informações da instância. Se selecionarmos "Criar modelo a partir da instância", criaremos um modelo que criará uma imagem com esse hardware.

Se clicarmos "Criar imagem", porém, criaremos uma imagem que terá todo o _software_ instalado, em qualquer _hardware_, com suas configurações de rede específicas. Essa é a opção que vamos selecionar.

Esperamos criar uma imagem que tenha instalados o _NGINX_ e a página configurada da _Bitnami_. Apesar disso, vamos poder manipulá-la: trocar o tipo de instância, mudar configurações de rede e selecionar outro par de chaves, por exemplo.

Selecionaremos "Ações > Imagem e modelos > Criar imagem". Assim, sempre que criarmos uma instância com essa imagem, teremos o _NGINX_ configurado. Vamos chamá-la de "my-nginx" e criar a imagem, sem alterar mais nada na página.

Agora, teoricamente, podemos criar instâncias a partir da imagem. Se formos ao menu lateral esquerdo e clicarmos em "Imagens > AMIs", encontraremos duas imagens: uma delas, a que está marcada como "Pendente", é a que criamos agora. Ela demorará algum tempo a ser processada.

O instrutor, porém, criou outra imagem antes do vídeo, para que pudéssemos seguir com os estudos naturalmente.

Ele criará uma instância a partir da imagem "my-bitnami-nginx". No menu esquerdo, clicaremos em "Instâncias > Executar instâncias". Batizaremos a instância de "instancia-a-partir-de-imagem". Em "Imagens de aplicação e de sistema operacional", vamos selecionar a opção "Minhas AMIs".

Nessa página, temos acesso a todas as imagens que criamos. Vamos selecionar a imagem quando ela estiver disponível.

Agora podemos mudar o _hardware_ da instância por completo. Apesar disso, vamos manter a instância gratuita, "t2.micro". Também poderíamos selecionar outro par de chaves, mas só temos o "ec2" configurado. Em "Firewall", vamos clicar em "Selecionar grupo de segurança existente" e adicionar "launch-wizard-1" e "acesso-web".

Também é possível mudar o armazenamento padrão, mas não faremos isso. Vamos executar a instância, agora, a partir de uma imagem. Com a instância criada, clicamos na sua identificação para que encontremos todos os detalhes.

De volta a "Imagens > AMIs", veremos que a imagem ainda está pendente. De volta a "Instâncias", removeremos o filtro "Estado da instância = running".

Quando a imagem não estiver mais pendente, vamos tentar acessá-la via o DNS público presente nos detalhes. Vamos alterar o "https" da URL por "http". Mesmo fazendo a alteração, não conseguiremos acessar.

Isso aconteceu porque a instância ainda não foi verificada e aprovada. Quando isso acontecer, tentaremos acessar a _DNS_ pública novamente. Agora, conseguiremos acessar substituindo o "https" da URL por "http".

Conseguimos criar uma imagem a partir de uma instância criada a partir de uma imagem. Vamos clicar na instância e seguir o caminho "Verificações de status > Ações > Criar alarme de verificações de status". Não vamos entrar em detalhes agora, mas podemos definir limites de alarme em várias situações, como utilização de CPU e entrada na rede, por exemplo.

O ideal, porém, é criar imagens a partir de instâncias desligadas, porque enquanto a instância roda, arquivos podem ser criados. Logo, a imagem será criada junto à criação desses outros arquivos. Com isso, pode ser criado um relatório de erro que não queríamos ver, por exemplo.

Então, para garantir a qualidade da imagem, o ideal é desligar a máquina, seguindo o caminho "Estado de instância > Interromper instância". Com ela interrompida, aí sim criamos a imagem, seguindo o caminho que seguimos anteriormente.

Como vamos utilizar apenas uma instância, vamos remover as outras, para não gerar custo. No nosso caso, estamos no cenário gratuito. Mas, se não estivéssemos, seríamos cobrados por instância.

Removeremos clicando em "Estado da instância > Encerrar instância". Quando atualizarmos a página, seu status será "Desligando". Depois disso, ela será encerrada.

No próximo vídeo, vamos configurar um IP dedicado específico para essa máquina.