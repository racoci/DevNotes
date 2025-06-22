A arquitetura descrita no artigo apresenta dois modelos principais para dotar agentes sociais de reações emocionais fundamentadas em teorias psicológicas:

1. **DETT** (Disposição → Gatilho → Emoção → Tendência), que estende o ciclo crença-intenção-ação com módulos que moldam a avaliação de eventos segundo traços individuais (disposição) e definem como a emoção resultante altera intenções futuras .
2. **Funções Moderadoras de Desempenho** (o PMFServ), que reúne diversos módulos — percepção, estado biológico, avaliação emocional, relações sociais e decisão cognitiva — articulados por “tanques” que representam componentes fisiológicos e psicológicos, e por “árvores de metas, padrões e preferências” que implementam o modelo de avaliação cognitiva de emoções .

## 1. Arquitetura DETT (Disposição – Gatilho – Emoção – Tendência)

### 1.1 Módulo de Disposição

Define **como** cada crença deve ser convertida em emoção, segundo o perfil do agente (por exemplo, um soldado com “tendência à covardia” reage à mesma percepção com medo, enquanto outro com “tendência à irritabilidade” reage com raiva) .

### 1.2 Módulo de Gatilho

Identifica **qual percepção** (visão de um inimigo, ruído súbito etc.) deu origem à emoção, servindo de link entre o mundo externo e a avaliação afetiva .

### 1.3 Módulo de Emoção

Aplica a **teoria de avaliação cognitiva** (OCC) sobre cada crença modificada pela disposição e pelo gatilho, gerando um vetor de intensidades emocionais (alegria, medo, raiva etc.) .

### 1.4 Módulo de Tendência

Traduz a emoção em **consequências cognitivas**: define como a emoção altera as intenções do agente (p. ex., medo gerar intenção de fugir; raiva gerar intenção de confrontar).

---

## 2. Funções Moderadoras de Desempenho (PMFServ)

A proposta do PMFServ é agrupar em um ciclo todas as etapas que, em humanos, regulam comportamento sob estresse, da percepção inicial até a ação explícita.

### 2.1 Percepção

* Captura **estímulos** do ambiente simulado (cenário, outros agentes) e processa **possibilidades de ação** (afordâncias) .
* Encaminha observações de outros agentes para o módulo de expressão, permitindo respostas sociais.

### 2.2 Estado Biológico e de Estresse (os “Tanques”)

No diagrama aparecem dois “tanques” principais, que armazenam variáveis fisiológicas e energéticas do agente:

* **Tanque de Fisiologia**: registra níveis de sono, nutrição, ferimentos, representando a condição corporal geral.
* **Tanque de Energia**: mede vitalidade e fadiga, influenciando rapidez e capacidade de resposta.
  Eles recebem atualizações de acordo com o tempo e eventos do mundo, e produzem sinais de **pressão temporal** (“tempo pressionando”) e **emoções negativas brutas** que alimentam diretamente a avaliação cognitiva .

### 2.3 Árvores de Metas, Padrões e Preferências

Implementam os três ramos do modelo de avaliação cognitiva de emoções:

1. **Árvore de Metas** – avalia consequências de eventos (alegria, decepção).
2. **Árvore de Padrões** – avalia ações de agentes (admiração, reprovação).
3. **Árvore de Preferências** – avalia aspectos de objetos (atração, repulsa).
   Cada ramo e sub-ramo possui pesos bayesianos que determinam sua importância; a avaliação informa, para cada nó, se houve sucesso ou fracasso, gerando intensidade para cada um dos onze pares emocionais do modelo original .

### 2.4 Agregação em Utilidade Subjetiva

As onze intensidades emocionais são **combinadas** em um único valor de utilidade subjetiva, simplificando para o sistema cognitivo a “carga afetiva total” de uma situação .

### 2.5 Módulo Social

Mantém **parâmetros de relacionamento** (confiança, alinhamento, credibilidade) e **propriedades de identidade** (demografia, grupos, papéis). Emissões de emoções negativas e decisões alteram esses tanques, que depois impactam a tomada de decisão .

### 2.6 Tomada de Decisão e Expressão

* **Teoria da Decisão Aumentada** usa a utilidade subjetiva e os parâmetros sociais para gerar um conjunto de ações candidatas.
* **Gestão de Intenções** prioriza essas ações, formando as intenções finais.
* **Módulo de Expressão** converte intenções em atos físicos e fala, e também em emissões de pares emocionais observáveis pelos demais .

---

## 3. Fluxo Integrado e Memória

Todos os subsistemas gravam e recuperam estados de **memória compartilhada**, garantindo consistência e permitindo que o agente lembre de seu nível de energia, sua última emoção e suas relações sociais durante toda a simulação .

---

**Referências do próprio artigo**:

* Van Dyke Parunak et al. (2006) descrevem o DETT como extensão de arquiteturas baseadas em crença-intenção-ação .
* Silverman et al. (2006b) apresentam o PMFServ reunindo percepções, tanques fisiológicos, avaliação cognitiva de emoções, relações sociais e decisão cognitiva em um ciclo único .

## Os onze pares de emoções no modelo OCC

Segundo Ortony, Clore e Collins, as vinte e duas emoções do modelo são organizadas em onze pares de valência oposta, facilitando a avaliação cognitiva de situações ([jasss.org][1]). Cada par consiste em uma emoção positiva e seu contraponto negativo, estruturadas em três ramos de foco: consequências de eventos, ações de agentes e aspectos de objetos. A seguir, apresentamos cada par em termos gerais.

1. **Alegria vs. Sofrimento**

   * **Alegria**: reação positiva a um evento visto como desejável em relação aos objetivos do agente.
   * **Sofrimento** (distress): reação negativa a um evento percebido como indesejável. ([w3.org][2])

2. **Esperança vs. Medo**

   * **Esperança**: sentimento positivo sobre a possibilidade futura de um evento desejável.
   * **Medo**: sentimento negativo sobre a possibilidade futura de um evento indesejável. ([w3.org][2])

3. **Satisfação vs. Decepção**

   * **Satisfação**: contentamento resultante da concretização de uma expectativa desejável.
   * **Decepção**: desagrado decorrente da frustração de uma expectativa desejável. ([w3.org][2])

4. **Alívio vs. Remorso**

   * **Alívio**: sensação positiva quando uma ameaça futura não se concretiza.
   * **Remorso**: sentimento negativo ligado a ter realizado uma ação imprópria que trouxe consequências indesejáveis. ([w3.org][2])

5. **Orgulho vs. Vergonha**

   * **Orgulho**: sentimento de valor próprio derivado de uma ação elogiável realizada pelo próprio agente.
   * **Vergonha**: sentimento de baixa autoestima associado a uma ação própria condenável. ([w3.org][2])

6. **Admiração vs. Reprovação**

   * **Admiração**: respeito positivo por uma ação louvável de outro agente.
   * **Reprovação**: julgamento negativo de uma ação de outro agente que viola padrões. ([w3.org][2])

7. **Gratidão vs. Ira**

   * **Gratidão**: respeito e reconhecimento por um benefício recebido de outro agente.
   * **Ira**: hostilidade ou raiva resultante de uma ação prejudicial de outro agente. ([w3.org][2])

8. **Felicidade pelo Bem de Outro vs. Ressentimento**

   * **Felicidade pelo bem‐estar de outro** (happy-for): alegria ao ver outra pessoa obter sucesso.
   * **Ressentimento**: desagrado ou inveja diante do êxito alheio. ([w3.org][2])

9. **Compaixão vs. Júbilo Maligno**

   * **Compaixão** (pity): tristeza pela desgraça alheia, acompanhada de desejo de ajudar.
   * **Júbilo Maligno** (gloating): prazer maligno ao testemunhar a queda de outro. ([w3.org][2])

10. **Amor vs. Ódio**

    * **Amor**: forte atração ou carinho por um objeto ou agente.
    * **Ódio**: forte repulsa ou antipatía por um objeto ou agente. ([w3.org][2])

11. **Afeição vs. Repulsa**

    * **Afeição** (liking): sentimento positivo de atração ou preferência por um objeto.
    * **Repulsa** (disliking): sentimento negativo de aversão ou desprezo por um objeto. ([w3.org][2])

> **Referências principais**
> – Ortony, A., Clore, G. L., & Collins, A. (1988). *The Cognitive Structure of Emotions*. ([jasss.org][1])
> – “The 22 OCC categories” (W3C). ([w3.org][2])
> – Daviet et al. (2005), uso de “11 pares de emoções” em agentes emocionais. ([researchgate.net][3])

[1]: https://www.jasss.org/21/2/5.html?utm_source=chatgpt.com "Emotion Modeling in Social Simulation: A Survey"
[2]: https://www.w3.org/TR/emotion-voc/?utm_source=chatgpt.com "Vocabularies for EmotionML - W3C"
[3]: https://www.researchgate.net/figure/The-eleven-pairs-of-the-OCC-model_tbl1_4207577?utm_source=chatgpt.com "The eleven pairs of the OCC model. | Download Table - ResearchGate"
