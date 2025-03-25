Nesse vídeo, vamos entender como criar instâncias pré-configuradas.

Antes de tudo, vamos nos livrar da instância "ec2-first", que criamos. Faremos isso selecionando e clicando em "Estado da instância > Encerrar a instância". Em seguida, clicaremos em "Encerrar". Isso vai desligar a máquina e removê-la.

Agora, enquanto esperamos a instância ser removida, clicaremos em "Executar instâncias". Nessa nova página, ao invés de selecionarmos uma imagem de início rápido, vamos entender um pouco mais sobre cada uma delas. Faremos isso clicando em "Procurar mais _AMIs_.

Existem _AMIs_ de início rápido, que são imagens com apenas o _Linux, Windows, Amazon_ e outras distribuições simples. Também existem as _AMIs_ do _AWS Marketplace_, disponibilizada para _marketplace_. Nela, podemos baixar imagens gratuitas ou pagas.

Também há _AMIs_ da comunidade. Ao contrário dessas, que são disponibilizadas pelo usuário, todas as outras são disponibilizadas pela _AWS_ ou empresas autorizadas.

Vamos selecionar _AMIs_ do _AWS Marketplace_ e, na barra de pesquisa, buscaremos por _NGINX_. Quando buscarmos, encontraremos alguns resultados. Vamos procurar a opção gratuita, que é o "NGINX Open Source packaged by Bitnami". Há muitas possibilidades, portanto, de instâncias pré-configuradas.

Clicaremos em "Selecionar > Definição de preço > NGINX Open Source packaged by Bitnami". Depois, veremos que não existe cobrança pelo software. Nas abas dessa página, podemos encontrar várias informações e descrições da imagem. Vamos clicar em "Continuar", para seguir à etapa de criação.

Em "Tipo de instância", vamos selecionar "t2.micro", qualificada para o nível gratuito. "Par de chaves" será "ec2". Vamos selecionar a opção "Selecionar grupo de segurança existente" em "Firewall (grupos de segurança)". Vamos selecionar "launch-wizard-1".

Selecionaremos também "acesso-web", que liberará as portas 80 e 443. Selecionamos os grupos de segurança. Eles já estão anexados à nossa nova instância.

Vamos manter o padrão nas outras informações. Agora podemos clicar em "Executar instância". Quando fizermos isso pela primeira vez, o processo levará bastante tempo, porque nossa conta está sendo inscrita no serviço de imagens da _AWS_.

Agora vamos voltar à página "Instâncias" e atualizá-la. Veremos que "er2-first" foi descartada, enquanto a instância que acabamos de criar, ainda sem nome, está sendo executada. Vamos editar o nome para "nginx".

Ela está em processo de inicialização. No próximo vídeo, revisaremos a instância.