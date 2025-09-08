# HunyuanWorld-Voyager: Relatório Técnico

# Tencent Hunyuan*

[https://3d-models.hunyuan.tencent.com/world/](https://3d-models.hunyuan.tencent.com/world/) [https://huggingface.co/tencent/HunyuanWorld-Voyager](https://huggingface.co/tencent/HunyuanWorld-Voyager) [https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager](https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager)

## Resumo

Embora o recente HunyuanWorld 1.0 possibilite a geração de mundos 3D exploráveis, desafios permanecem com vistas oclusas e alcance de exploração limitado. Para abordar essas limitações, introduzimos o Voyager para extrapolação consistente de mundos, que é uma estrutura de difusão de vídeo que gera sequências consistentes de nuvens de pontos 3D a partir de uma única imagem com trajetória de câmera definida pelo usuário. Ao contrário das abordagens existentes, o Voyager alcança geração e reconstrução de cena ponta a ponta com consistência inerente entre quadros, eliminando a necessidade de pipelines de reconstrução 3D (por exemplo, structure-from-motion ou estéreo multivisão). Nosso método integra três componentes-chave: 1) Difusão de Vídeo Consistente com o Mundo: Uma arquitetura unificada que gera conjuntamente sequências de vídeo RGB e profundidade alinhadas, condicionadas à observação existente do mundo para garantir coerência global; 2) Exploração de Mundo de Longo Alcance: Um cache de mundo eficiente com remoção de pontos e uma inferência autorregressiva com amostragem suave de vídeo para extensão iterativa de cena com consistência consciente do contexto; e 3) Mecanismo de Dados Escalável: Um pipeline de reconstrução de vídeo que automatiza a estimativa de pose de câmera e previsão de profundidade métrica para vídeos arbitrários, possibilitando a curadoria de dados de treinamento em larga escala e diversos sem anotações 3D manuais. Coletivamente, esses projetos resultam em uma clara melhoria sobre os métodos existentes em qualidade visual e precisão geométrica, com aplicações versáteis. ∗ Os colaboradores da equipe estão listados no final do relatório.

## 1 Introdução

A criação de cenas 3D de alta fidelidade e exploráveis que os usuários podem navegar de forma contínua alimenta amplas aplicações que vão desde jogos de vídeo e produção de filmes até simulação robótica [33]. No entanto, os fluxos de trabalho tradicionais para construir tais mundos 3D permanecem limitados pelo esforço manual, exigindo minucioso projeto de layout, curadoria de ativos e composição de cena. Embora métodos recentes baseados em dados [40, 49, 25, 41, 21] tenham mostrado promessa na geração de objetos ou cenas simples, sua capacidade de escalar para cenas complexas é limitada pela escassez de dados de cena 3D de alta qualidade. Essa lacuna destaca a necessidade de estruturas que possibilitem a geração escalável de mundos virtuais navegáveis pelo usuário com consistência 3D.

  Recentemente, um número crescente de trabalhos [6, 8, 37, 48, 24, 50, 27, 3] explorou o uso de síntese de visão nova (NVS) e geração de vídeo como paradigmas alternativos para modelagem de mundo. Esses métodos, embora demonstrem capacidades impressionantes na geração de conteúdo visualmente atraente e semanticamente rico, ainda enfrentam vários desafios. 1) Inconsistência Espacial de Longo Alcance. Devido à ausência de fundamentação estrutural 3D explícita, eles frequentemente lutam para manter consistência espacial e transições de ponto de vista coerentes durante o processo de geração, especialmente ao gerar vídeos com trajetórias de câmera de longo alcance. 2) Alucinação Visual. Embora vários trabalhos [27, 3] tenham tentado aproveitar condições 3D para melhorar a consistência geométrica, eles normalmente dependem de imagens RGB parciais como orientação, ou seja, imagens de visão nova renderizadas a partir de nuvens de pontos reconstruídas com visões de entrada. No entanto, tal representação pode introduzir alucinações visuais significativas em cenas complexas, como as oclusões incorretas na Figura 2, que podem introduzir supervisão imprecisa durante o treinamento. 3) Reconstrução 3D Posterior. Embora essas abordagens possam sintetizar conteúdo visualmente satisfatório, reconstruções 3D posteriores ainda são necessárias para obter conteúdo 3D utilizável. Este processo é demorado e inevitavelmente introduz artefatos geométricos [38], tornando-se inadequado para aplicações do mundo real.

  

Para abordar esses desafios, introduzimos o Voyager [13], uma estrutura projetada para sintetizar vídeos RGB-D(epth) de longo alcance e consistentes com o mundo a partir de uma única imagem e trajetórias de câmera especificadas pelo usuário. No núcleo do Voyager está uma nova difusão de vídeo consistente com o mundo que utiliza um mecanismo de cache de mundo expansível para garantir consistência espacial e evitar alucinação visual. Começando com uma imagem, construímos um cache de mundo inicial projetando-a no espaço 3D com um mapa de profundidade. Este cache 3D é então projetado nas visões da câmera alvo para obter observações RGB-D parciais, que guiam o modelo de difusão para manter coerência com o estado acumulado do mundo. Crucialmente, os quadros gerados são realimentados para atualizar e expandir o cache do mundo, criando um sistema de ciclo fechado que suporta trajetórias de câmera arbitrárias enquanto mantém coerência geométrica.

  

Ao contrário dos métodos [48, 24, 27, 3] que dependem apenas de condicionamento RGB, o Voyager aproveita explicitamente informações de profundidade como um prior espacial, possibilitando maior consistência 3D durante a geração de vídeo. Ao gerar simultaneamente sequências RGB e profundidade alinhadas, nossa estrutura suporta reconstrução direta de cena 3D sem exigir etapas adicionais de reconstrução 3D como structure-from-motion.

  

Apesar do desempenho promissor, modelos de difusão lutam para gerar vídeos longos em uma única passagem. Para possibilitar a exploração de mundo de longo alcance, propomos um esquema de cache de mundo e amostragem suave de vídeo para extensão de cena autorregressiva. Nosso cache de mundo acumula e mantém nuvens de pontos de todos os quadros gerados anteriormente, expandindo-se à medida que as sequências de vídeo crescem. Para otimizar a eficiência computacional, projetamos um método de remoção de pontos para detectar e remover pontos redundantes com renderização em tempo real, minimizando a sobrecarga de memória. Aproveitando as nuvens de pontos em cache como proxy, desenvolvemos uma estratégia de amostragem suave que estende autorregressivamente o comprimento do vídeo enquanto garante transições suaves entre clipes.

  

Treinar tal modelo requer vídeos em larga escala com poses de câmera precisas e profundidade, mas os conjuntos de dados existentes frequentemente carecem dessas anotações. Para abordar isso, introduzimos um mecanismo de dados para reconstrução de vídeo escalável que estima automaticamente poses de câmera e profundidade métrica para vídeos de cena arbitrários. Com a estimativa de profundidade métrica, nosso mecanismo de dados garante escalas de profundidade consistentes em diversas fontes, possibilitando a geração de dados de treinamento de alta qualidade. Usando este pipeline, compilamos um conjunto de dados de mais de 100.000 clipes de vídeo, combinando capturas do mundo real e renderizações sintéticas do Unreal Engine.

  

Experimentos extensos demonstram a eficácia do Voyager na geração de vídeo de cena e reconstrução de mundo 3D. Beneficiando-se da modelagem conjunta de profundidade, nossos resultados na Figura 1 exibem geometria mais coerente, que não só possibilita a reconstrução 3D direta, mas também suporta a expansão infinita do mundo enquanto preserva o layout espacial original. Além disso, exploramos aplicações como geração 3D, transferência de vídeo e estimativa de profundidade, mostrando ainda mais o potencial do Voyager no avanço da inteligência espacial.

  

Nossas contribuições podem ser resumidas como: • Introduzimos o Voyager, um modelo de difusão de vídeo consistente com o mundo para geração de cena. Até onde sabemos, o Voyager é o primeiro modelo de vídeo que gera conjuntamente sequências RGB e profundidade com trajetórias de câmera dadas. • Propomos um esquema de cache de mundo eficiente e uma abordagem de amostragem de vídeo autorregressiva, estendendo o Voyager para reconstrução de mundo e exploração infinita de mundo. • Propomos um mecanismo de dados de vídeo escalável para estimativa de câmera e profundidade métrica, com mais de 100.000 pares de treinamento preparados para o modelo de difusão de vídeo.

## 2 Detalhes Técnicos

Dada uma imagem I0 ∈ R3×H×W, nosso objetivo é criar um mundo explorável baseado em uma trajetória de câmera definida pelo usuário. No entanto, há uma lacuna entre a geração de vídeo e a modelagem de mundo 3D, que se origina principalmente de três aspectos: (1) a inconsistência da extensão de vídeo de longo alcance, (2) a alucinação de condições visuais para geração de vídeo, e (3) a incapacidade de reconstruir o mundo a partir das saídas de vídeo. Para abordar esses problemas, propomos o Voyager, uma estrutura de geração de vídeo consistente com o mundo que pode produzir diretamente quadros rgb-profundidade com parâmetros de câmera correspondentes para exploração de mundo de longo alcance. Nesta seção, primeiro introduzimos uma condição de quadro injetada com geometria para compensar a alucinação perceptual sob condições visuais. (Seç. 2.1). Com esta condição de entrada, propomos um modelo de difusão de vídeo fundido com profundidade para garantir consistência espacial e blocos baseados em contexto para aprimorar seu controle de ponto de vista (Seç. 2.2). Para reconstrução de mundo 3D e exploração de longo alcance, propomos cache de mundo com remoção de pontos e amostragem suave de vídeo na inferência autorregressiva (Seç. 2.3). Propomos ainda um mecanismo de dados de vídeo escalável para preparar câmera e profundidade métrica para o treinamento do modelo acima (Seç. 2.4).

### 2.1 Condição de Quadro Injetada com Geometria

Para o controle do ponto de vista do vídeo, o parâmetro da câmera [50, 1] é uma condição direta, mas esta condição implícita não é trivial para o treinamento de modelos de vídeo. Trabalhos recentes [24, 27, 3] tentam reconstruir a nuvem de pontos p ∈ RN×6 a partir de vídeos como um controle explícito, onde N é o número de pontos e cada ponto é representado por coordenadas 6D (x, y, z, r, g, b). A condição RGB deformada Îv para uma visão nova v pode então ser renderizada de acordo com a câmera, que é uma imagem parcial com regiões em branco.

  

No entanto, tal imagem RGB parcial é insuficiente para garantir consistência espacial, por exemplo, relações de oclusão complexas em uma cena podem levar a alucinações visuais. Para impor controle espacialmente consistente durante o treinamento, introduzimos uma condição geométrica adicional, o mapa de profundidade parcial, que está alinhado com a imagem RGB parcial. Especificamente, primeiro estimamos o mapa de profundidade Dk e os parâmetros de câmera correspondentes ck para cada quadro Ik do vídeo. Como apenas o primeiro quadro é visível na inferência de vídeo, criamos uma nuvem de pontos p0 projetando D0 com c0. Para o k-ésimo quadro, sua imagem parcial Îk e profundidade parcial D̂k são adquiridas mascarando a região invisível com a máscara de renderização Mk = render(p0, ck).

### 2.2 Difusão de Vídeo Consistente com o Mundo

Condicionado com mapas RGB e profundidade parciais, nossa intenção é gerar conteúdo plausível para as regiões invisíveis, garantindo consistência com as informações espaciais fornecidas pelas condições parciais. Para este propósito, a prática comum [18, 27] é concatenar os latentes de condição zrgb e zdepth com os latentes originais ruidosos zt ao longo do eixo do canal e projetar os latentes concatenados de volta para a dimensão do Transformer através da camada de patch-embedding femb: z′t,0 = femb(concat(zt, zrgb, zdepth)). Então, os latentes projetados z′t,0 são alimentados para blocos de fluxo duplo e fluxo único sequencialmente, o que é formulado como, z′t,i, z′y,i = f iD(z′t,i−1, z′y,i−1, t), i = 1, ..., ND, (1) z′′t,i = f iS(z′′t,i−1, t), i = 1, ..., NS , (2) onde z′y é o latente de texto. ND e NS denotam o número de blocos de cada fluxo. z′′t,0 é inicializado como a concatenação de z′t,N e z′y,N.

  

Embora o modelo de vídeo possa preservar melhor os parâmetros pré-treinados desta forma, as condições espaciais são usadas apenas no nível do canal. As partes ausentes em nossos mapas parciais podem variar de pequenas rachaduras a grandes áreas em branco, dependendo da extensão da mudança de ponto de vista. Esta solução trivial lida com situações variáveis. Portanto, como mostrado na Figura 4, propomos geração de vídeo fundida com profundidade e aprimoramento de controle baseado em contexto para melhorar o modelo de vídeo.

  

Geração de Vídeo Fundida com Profundidade. Em vez de depender apenas da profundidade parcial como condição de entrada para completar as regiões ausentes nos quadros RGB, propomos gerar simultaneamente quadros RGB e profundidade completos. Como resultado, o modelo de vídeo pode aproveitar a estrutura de atenção completa do DiT, permitindo a interação de informações visuais e geométricas no nível de pixel. Para este fim, concatenamos as imagens rgb e profundidade ao longo do eixo da altura como Ik = [Ik,Φ, Dk]h, bem como os mapas de condição Îk = [Îk,Φ, D̂k]h e máscaras Mk = [Mk,Φ,Mk]h. Aqui, adicionamos uma linha de espaço reservado Φ entre as imagens rgb e profundidade para ajudar o modelo a separar esses dois tipos de conteúdo. Os novos latentes de vídeo são apresentados como z′t,0 = femb(concat(zt, ẑi, ẑ0,m)), onde ẑi é o latente de [Îk]T−1k=0 e m é o mapa reduzido de [Mk]T−1k=0 via max-pooling. Para suportar ainda mais o condicionamento de imagem, concatenamos o latente de imagem ẑi, que codifica o primeiro quadro do vídeo verdadeiro, enquanto preenchemos os latentes dos quadros restantes com zeros. De acordo, z′t,0 é alimentado para o modelo de difusão semelhante à Eq. 1-2. O modelo de difusão é então treinado para gerar quadros de vídeo rgb-profundidade.

  

Aprimoramento de Controle Baseado em Contexto. O mecanismo de concatenação acima incorpora informações condicionais apenas na entrada do modelo DiT, levando a uma aplicação fraca das condições geométricas e resultando em desalinhamento entre os quadros gerados e as condições de entrada.

  

Para aprimorar as capacidades de seguimento geométrico, seguindo [2], injetamos ainda o modelo de difusão com módulos leves. Concretamente, replicamos o primeiro bloco dos módulos de fluxo duplo e fluxo único como os blocos de Controle f̂D e f̂S. Dado o latente de vídeo de entrada z′t,0, temos as seguintes operações para cada bloco Transformer i: zD = f̂D(z′t,0), zS = f̂S(zD), (3) z′t,i = z′t,i + lD(zD), z′′t,i = z′′t,i + lS(zS), (4) onde lD e lS são camadas lineares inicializadas com zero. Os latentes de recursos do estágio inicial preservam mais informações contextuais, de modo que a integração em cada bloco pode fortalecer a controlabilidade no nível de pixel.

### 2.3 Exploração de Mundo de Longo Alcance

Para geração de vídeo de longo alcance ou mesmo infinita, autorregressão é uma escolha natural. Este paradigma gera recursivamente quadros ou clipes futuros com base no conteúdo gerado anteriormente, mantendo continuidade temporal ao longo do tempo. No entanto, devido à capacidade de memória limitada dos modelos de difusão de vídeo, métodos autorregressivos são frequentemente restritos a condicionar apenas alguns quadros ou clipes precedentes. Este contexto limitado leva a uma perda inevitável de informações, tornando fundamentalmente inviável reter e propagar o histórico completo da cena. Em contraste com os métodos autorregressivos anteriores, o Voyager explora condições de nuvem de pontos para geração, que é uma representação escalável para armazenar todas as informações de histórico. Para possibilitar a geração infinita, propomos cache de mundo com remoção de pontos para armazenar eficientemente informações espaciais e adotamos amostragem suave de vídeo para garantir a consistência dos clipes consecutivos.

  

Cache de Mundo com Remoção de Pontos. Com parâmetros de câmera de entrada e quadros de vídeo RGB-D correspondentes, nuvens de pontos podem ser projetadas no espaço 3D como p̂ ∈ R(T×H×W)×3, onde T é o número total de quadros. À medida que o vídeo continua a se estender, o número de pontos pode facilmente crescer para milhões, apresentando desafios significativos em termos de memória e eficiência computacional. Para abordar isso, propomos manter um cache de mundo, que elimina pontos redundantes enquanto preserva informações geométricas essenciais. Especificamente, adicionamos incrementalmente novos pontos ao cache em base por quadro: dada a nuvem de pontos acumulada p̂ dos quadros anteriores, renderizamos uma máscara de visibilidade M = render(p̂, ci) a partir da visão da câmera atual ci. Pontos nas regiões invisíveis são adicionados a p̂ primeiro. Para as regiões visíveis, se o ângulo entre a normal da superfície dos pontos existentes e a direção da visão atual exceder 90 graus, o novo ponto também é atualizado no cache, porque esses pontos existentes não podem ser vistos no ponto de vista atual. Esta estratégia reduz o número de pontos armazenados em aproximadamente 40% e evita o acúmulo de ruído causado pela agregação de múltiplos quadros.

  

Amostragem Suave de Vídeo. Condicionado no cache de mundo acima, nosso modelo de vídeo pode acessar as informações espaciais completas dos quadros anteriores. No entanto, embora cada clipe de vídeo gerado independentemente seja espacialmente consistente, ainda pode haver discrepâncias de cor, tornando-os inadequados para concatenação direta. Adotamos duas estratégias para garantir transições mais suaves entre clipes adjacentes. (1) Primeiro dividimos o vídeo de entrada em segmentos sobrepostos, onde o comprimento da região sobreposta é metade de um segmento. Para cada segmento, a região sobreposta é inicializada com os resultados gerados do segmento anterior, servindo como a inicialização de ruído para a região sobreposta do segmento atual. (2) Após completar a inferência para os dois segmentos consecutivos, aplicamos média nas regiões sobrepostas e realizamos alguns passos de desruído para refinar as transições. Desta forma, garantimos a geração eficiente de múltiplos clipes enquanto mantemos consistência visual em quadros de vídeo consecutivos.

### 2.4 Mecanismo de Dados de Vídeo Escalável

Treinar tal modelo de vídeo exige quadros de vídeo em larga escala com parâmetros de câmera correspondentes e mapas de profundidade. Curamos cuidadosamente mais de 100.000 clipes de vídeo de vídeos capturados no mundo real e renderizações 3D, e propomos um mecanismo de dados de vídeo escalável para anotar automaticamente as informações 3D necessárias para vídeos de cena arbitrários.

  

Curadoria de Dados. Selecionamos dois conjuntos de dados de código aberto do mundo real, ou seja, RealEstate [51] e DL3DV [19] para o treinamento. RealEstate contém 74.766 clipes de vídeo relacionados a cenas imobiliárias, apresentando principalmente cenas domésticas internas, juntamente com alguns ambientes externos. DL3DV fornece 10K vídeos de cena real, mas a maioria deles sofre de movimentos de câmera rápidos ou instáveis. Curamos 3.000 vídeos de alta qualidade deste conjunto de dados e os segmentamos em aproximadamente 18.000 clipes de vídeo. Além disso, para aumentar a diversidade do conteúdo de geração, coletamos 1.500 modelos de cena do Unreal Engine e renderizamos mais de 10.000 amostras de vídeo para aumentar o conjunto de dados. No final, coletamos mais de 100.000 clipes de vídeo desses conjuntos de dados.

  

Anotação de Dados. Parâmetros de câmera precisos e profundidade são cruciais para o treinamento do modelo, mas RealEstate e DL3DV não fornecem tais dados de verdade terrestre. Métodos existentes [3, 27, 30] adotam modelos estéreo densos [32] para preparar pares de treinamento, lutando para produzir profundidade geometricamente consistente. Propomos um mecanismo de processamento de dados mais robusto como mostrado na Figura 5. Especificamente, primeiro usamos VGGT [35] para estimar parâmetros de câmera e profundidade para todos os quadros de vídeo. A profundidade estimada por VGGT não é precisa o suficiente, mas está alinhada com as poses da câmera. Para melhorar ainda mais a estimativa de profundidade, então empregamos MoGE [36] como um estimador de profundidade robusto e alinhamos os dois mapas de profundidade com otimização de mínimos quadrados.

  

Finalmente, como nossos dados UE fornecem valores de profundidade métrica, precisamos alinhar todas as profundidades estimadas a uma escala padrão. Estimamos o intervalo de profundidade métrica da cena usando Metric3D [12] e mapeamos as profundidades anteriores para este intervalo. Desta forma, podemos anotar automaticamente câmera e profundidade para vídeos de qualquer fonte.

## 3 Avaliação do Modelo

### 3.1 Detalhes de Implementação

Nosso treinamento segue basicamente o modelo de imagem para vídeo do HunYuan-Video [17]. Dividimos o treinamento em três estágios: o primeiro estágio treina apenas o modelo de vídeo RGB; no segundo estágio, a profundidade é introduzida no treinamento; e no terceiro estágio, os parâmetros do DiT são congelados e os blocos ControlNet são incorporados para treinamento. Usamos todos os três conjuntos de dados no primeiro estágio de treinamento. No entanto, DL3DV é removido no segundo estágio devido ao seu movimento de câmera rápido, o que o torna inadequado para treinamento de profundidade. No terceiro estágio, treinamos apenas no conjunto de dados UE com sua profundidade verdadeira. Durante o treinamento, selecionamos aleatoriamente uma razão largura-altura de [1, 1.25, 1.5, 1.75] para suportar a geração de vídeos com múltiplas proporções. Para melhorar a robustez do modelo a velocidades variadas de movimento da câmera, selecionamos aleatoriamente intervalos de quadros para amostrar vídeos de treinamento, expondo assim o modelo a trajetórias de diferentes densidades temporais. A taxa de aprendizado é definida como 1× 10−5 com uma fase de aquecimento de 100 iterações, e é programada para decair para um valor mínimo de 1× 10−6. Para inferência, a profundidade da imagem de entrada é primeiro estimada por MoGE [36]. O número de passos de amostragem é definido como 50 por padrão. O consumo de pico de memória da GPU durante a inferência de placa única é de aproximadamente 60 GB. Usando quatro GPUs em paralelo, a geração ponta a ponta de um único segmento de vídeo é concluída em aproximadamente 4 minutos. O número de quadros de geração para uma única passagem é 49. Fornecemos pseudocódigo de nosso cache de mundo e amostragem suave de vídeo no Algoritmo 1 e 2, respectivamente.

### 3.2 Geração de Vídeo

Avaliamos a qualidade de geração de vídeo do Voyager comparando quatro métodos de geração de vídeo controláveis por câmera de código aberto em geração de imagem para vídeo, incluindo SEVA [50], ViewCrafter [48], See3D [24] e FlexWorld [3]. Entre esses métodos, ViewCrafter, See3D e FlexWorld controlam os pontos de vista com condições de nuvem de pontos, que são semelhantes ao nosso método. SEVA toma diretamente parâmetros de câmera como condições de entrada.

  

Conjunto de Dados e Métricas. Selecionamos aleatoriamente 150 clipes de vídeo do conjunto de teste do RealEstate [51] como nosso conjunto de dados de teste. Para avaliar ainda mais nosso modelo com dados não vistos, amostramos 50 vídeos de Tanks and Temples [16] como um conjunto de dados fora do domínio. Como os clipes de vídeo não fornecem câmeras verdadeiras, estimamos os parâmetros da câmera e os mapas de profundidade com o mesmo pipeline em nosso mecanismo de dados. Para avaliar a qualidade visual dos vídeos gerados, adotamos PSNR, SSIM e LPIPS para medir a semelhança entre os quadros gerados e a verdade terrestre.

  

Resultados. Relatamos os resultados quantitativos na Tabela 1. Nosso método supera todas as linhas de base, demonstrando a alta qualidade de geração de nosso modelo de vídeo. A comparação qualitativa na Figura 6 também mostra nossa capacidade de gerar vídeos fotorrealistas. Especialmente no último caso da Figura 6, apenas nosso método pode preservar os detalhes dos produtos na imagem de entrada. No entanto, outros métodos são propensos a gerar artefatos, por exemplo, no primeiro exemplo da Figura 6, esses métodos falham em fornecer previsões razoáveis quando o movimento da câmera é muito grande.

### 3.3 Geração de Cena

Para avaliar a qualidade da geração de cena, comparamos ainda mais a qualidade da reconstrução de cena com vídeos gerados com base na Seç. 3.2. Como as linhas de base comparadas produzem apenas quadros RGB, primeiro exploramos VGGT [35] para estimar parâmetros de câmera e inicializar as nuvens de pontos para os vídeos gerados desses métodos. Graças à capacidade de gerar conteúdo RGB-D, nossos resultados podem ser usados diretamente na reconstrução 3DGS.

  

Na Tabela 2, nossos resultados de reconstrução com VGGT posterior superam as linhas de base comparadas, indicando que nossos vídeos gerados são mais consistentes em termos de geometria. Os resultados são ainda melhores ao inicializar nuvens de pontos com nossa própria saída de profundidade, o que demonstra a eficácia de nossa geração de profundidade para reconstrução de cena. Os resultados qualitativos na Figura 3 ilustram a mesma conclusão. Particularmente no último caso, nosso método retém a maioria dos detalhes do lustre, enquanto os métodos de linha de base até mesmo falham em reconstruir uma forma básica.

### 3.4 Geração de Mundo

Além da comparação no domínio no RealEstate, testamos o Voyager no benchmark estático WorldScore [5] na geração de mundo. WorldScore consiste em 2.000 exemplos de teste estáticos que abrangem mundos diversos, por exemplo, internos e externos, fotorrealistas e estilizados. Em cada exemplo, uma imagem de entrada e uma trajetória de câmera são fornecidas. As métricas avaliam a controlabilidade e qualidade da geração de vídeo. Especificamente, usamos "Camera Control", "Object Control" e "Content Alignment" para julgar como o modelo de vídeo adere às instruções de ponto de vista e prompts de texto. Usamos "3D Consistency", "Photometric Consistency", "Style Consistency" e "Subjective Quality" para avaliar a consistência e qualidade do conteúdo gerado. Finalmente, uma pontuação média é apresentada para mostrar o desempenho geral. Consulte WorldScore para obter detalhes dessas métricas.

  

Comparamos sete principais métodos no benchmark existente, incluindo três métodos 3D WonderJourney [47], LucidDreamer [4] e WonderWorld [46], e quatro métodos de vídeo EasyAnimate [42], Allegro [52], Gen-3 [29] e CogVideoX [43]. As pontuações são relatadas na Tabela 3. O Voyager alcança a pontuação mais alta neste benchmark. A pontuação mostra que o voyager tem desempenho competitivo no controle de câmera e consistência espacial, em comparação com métodos baseados em 3D. Comparado com métodos de deformação como LucidDreamer e WonderWorld, nosso método atinge um melhor equilíbrio entre consistência de geração e qualidade. Nossa consistência de estilo e qualidade subjetiva são as mais altas entre todos os métodos, demonstrando ainda mais a qualidade visual de nossos vídeos gerados. Notavelmente, como nossa condição de vídeo é construída com profundidade métrica, o movimento da câmera em nossos resultados é maior do que outros métodos, o que é muito mais difícil de gerar.

### 3.5 Geração de Vídeo de Longo Alcance

Como explicado na Seç. 2.3, nosso método permite a geração de vídeo de longo alcance com cache de mundo eficiente e amostragem suave de vídeo. Na Figura 8, fornecemos resultados de geração que consistem em três clipes de vídeo, com trajetórias de câmera totalmente diferentes entre os clipes.

  

Os resultados apresentam controlabilidade de câmera e consistência espacial do vídeo gerado, demonstrando que nosso método é capaz de exploração de mundo de longo alcance. Por exemplo, a montanha no clip-3 da Figura 8(a) é exatamente a mesma que a imagem de entrada, o que se beneficia das informações espaciais preservadas por nosso cache de mundo. Na Figura 8(d), a cadeira azul à extrema esquerda permanece consistente com a imagem de entrada, embora tenha se movido para fora do campo de visão durante a geração do clip-1.

### 3.6 Estudos de Ablação

Para verificar a eficácia de nossos projetos propostos, conduzimos estudos de ablação em nossa difusão de vídeo consistente com o mundo e exploração de mundo de longo alcance.

  

Difusão de Vídeo Consistente com o Mundo Avaliamos nossos modelos de vídeo treinados nos três estágios separadamente no conjunto de teste RealEstate10K e no benchmark Worldscore, ou seja, (a) modelo treinado apenas em condições RGB, (b) modelo treinado em condições RGB-D, e (c) modelo anexado com blocos de controle adicionais. Como mostrado na Tabela 4, fundir condições de profundidade no treinamento pode melhorar significativamente a qualidade de geração e o controle da câmera. Os blocos de controle podem melhorar ainda mais a consistência espacial dos resultados gerados. Também fornecemos resultados qualitativos na Figura 9. O modelo apenas RGB pode gerar conteúdo inconsistente quando a câmera se move para uma região não vista. Os resultados do modelo RGB-D são mais consistentes com a imagem de entrada, mas ainda podem produzir alguns artefatos menores. Nosso modelo final gera os resultados mais razoáveis.

  

Geração de vídeo de longo alcance. Avaliamos a qualidade da remoção de pontos e amostragem suave na Figura 10. Para remoção de pontos, armazenar todos os pontos introduz ruído, enquanto armazenar pontos na região invisível é insuficiente. Resultados com verificação normal adicional têm desempenho visual comparável com armazenar todos os pontos, mas economizam quase 40% de armazenamento. Para amostragem suave, o clipe de vídeo sem amostragem pode exibir inconsistências em comparação com o primeiro clipe. A amostragem suave garante uma transição perfeita entre dois segmentos consecutivos.

## 4 Aplicações

Beneficiando-se de nossa geração de vídeo fundida com profundidade, o Voyager suporta várias aplicações relacionadas a 3D. Além disso, fornecemos mais resultados de visualização na Figura 12 e 13.

  

Geração de Imagem para 3D. Na Figura 11(a), usamos três métodos de geração 3D de última geração Trellis [40], Rodin v1.5 [28] e Hunyuan-3D v2.5 [14] para gerar uma trajetória orbital de imagens de entrada. Comparado com o Voyager, os métodos 3D geralmente são deficientes em capturar detalhes de textura refinados e garantir a plausibilidade de visões novas. Como mostrado na geração do personagem antigo, nosso método apresenta texturas mais detalhadas, especialmente na geração de vista traseira. Além disso, modelos generativos 3D nativos dificilmente conseguem lidar com a geração de múltiplos objetos. Na combinação simples onde um carro se encosta a uma tenda, o Rodin falhou em gerar a tenda, enquanto o Trellis produziu uma tenda com partes ausentes. O Hunyuan gerou com sucesso dois objetos completos, mas a relação espacial era imprecisa, com a tenda muito distante do carro. Nosso método não apenas gera o conteúdo correto, mas também produz efeitos visuais mais realistas. A tenda é até visível através da janela do carro na vista lateral.

  

Transferência de Vídeo Consistente com Profundidade. Gerar um vídeo espacialmente consistente com um estilo diferente normalmente requer o treinamento de um modelo de vídeo estilizado. No entanto, para alcançar o efeito desejado com nosso modelo, só precisamos substituir a imagem de referência enquanto retém a condição de profundidade original. Como mostrado na Figura 11(b), podemos alterar o vídeo original para o estilo americano ou para a noite, mantendo as informações espaciais do vídeo original.

  

Estimativa de Profundidade de Vídeo. Nosso modelo de vídeo é naturalmente capaz de estimar profundidade de vídeo. Na Figura 11(c), nossa profundidade prevista pode preservar os detalhes nas arquiteturas. Projetamos ainda mais a profundidade estimada para nuvem de pontos 3D na Figura 11(d). Comparado com VGGT, a projeção do Voyager parece mais plausível. Como a profundidade verdadeira não está disponível para vídeos gerados, é inviável avaliar a estimativa de profundidade usando métricas como Erro Relativo Absoluto (AbsRel). Portanto, conduzimos um estudo de usuário em pontos projetados de dois métodos. Selecionamos aleatoriamente 10 cenas internas e 10 externas do RealEstate10k e pedimos a 10 participantes para escolher o mais plausível. Os resultados são mostrados na Tabela 5. Nossos resultados são preferidos pelos participantes, particularmente em cenas externas com maior alcance de profundidade.

## 5 Trabalhos Relacionados

### 5.1 Geração de Visão Controlável por Câmera

Os modelos de geração controláveis por câmera existentes podem ser categorizados em três tipos: síntese de visão nova [15, 26, 39, 11] produz novos pontos de vista através de reconstrução multivisão. Esses métodos dependem de pontos de vista densos e lutam para lidar com entradas de visão única. O segundo método [7, 20, 37, 8, 50, 22] incorpora implicitamente parâmetros de câmera no modelo, treinando-o para gerar imagens a partir dos pontos de vista correspondentes. Por exemplo, SEVA [50] injetou embeddings de plucker de trajetórias de câmera nas camadas de atenção, impondo seguimento de ponto de vista da geração de vídeo. No entanto, esses métodos frequentemente sofrem de inconsistência espacial, onde o conteúdo de diferentes pontos de vista está espacialmente desalinhado, levando a artefatos e desalinhamentos notáveis na saída gerada. O terceiro método [31, 24, 27, 3] aproveita nuvens de pontos obtidas pela deformação da visão de entrada como condições para geração de visão nova como uma condição explícita, reduzindo significativamente a complexidade de geração. LucidDreamer [4] propôs um modelo de inpainting para preencher as regiões ausentes de imagens deformadas. See3D [24] treinou um modelo de geração multivisão condicionado com imagens deformadas. ViewCrafter [48], Gen3C [27] e FlexWorld [3] propuseram introduzir modelos de vídeo nesta tarefa, melhorando ainda mais a consistência do conteúdo gerado. No entanto, as imagens deformadas ainda contêm artefatos que afetam negativamente o treinamento do modelo, como discutido na Figura 2. Neste trabalho, introduzimos a deformação de profundidade como uma entrada de condicionamento adicional e geramos conteúdo RGB e profundidade.

### 5.2 Geração de Vídeo de Longo Alcance

Os modelos de vídeo atuais são limitados em sua capacidade de gerar vídeos longos em uma única passagem. Para estender o comprimento do vídeo, pesquisas existentes exploram métodos sem treinamento [34, 23], estratégias hierárquicas [44, 9] e estruturas autorregressivas [45, 10]. No entanto, as duas primeiras abordagens não podem escalar para vídeos infinitamente longos, enquanto a estratégia autorregressiva depende de caches de memória que lutam para reter informações de quadros distantes no passado. Para abordar essa limitação, propomos neste trabalho um cache de mundo com remoção de pontos que preserva eficientemente informações espaciais e possibilita a geração de vídeos arbitrariamente longos com amostragem suave de vídeo em uma inferência autorregressiva.

## 6 Conclusão

Neste artigo, apresentamos o Voyager, uma estrutura de geração de vídeo consistente com o mundo para exploração de mundo de longo alcance. O modelo de difusão de vídeo RGB-D proposto pode produzir sequências de vídeo espacialmente consistentes que se alinham com as trajetórias de câmera de entrada, permitindo a reconstrução direta de cena 3D. Isso suporta a expansão de mundo autorregressiva e consistente. Experimentos demonstram alta fidelidade visual e forte coerência espacial tanto nos vídeos gerados quanto nas nuvens de pontos.

## Colaboradores

• Patrocinadores do Projeto: Jie Jiang, Linus, Yuhong Liu, Peng Chen • Líderes do Projeto: Tengfei Wang, Chunchao Guo • Colaboradores Principais: Tianyu Huang, Wangguandong Zheng, Tengfei Wang, Junta Wu, Zhenwei Wang, Yuhao Liu • Colaboradores: Xuhui Zuo, Lifu Wang, Yixuan Tang, Yonghao Tan, Chao Zhang

  
**