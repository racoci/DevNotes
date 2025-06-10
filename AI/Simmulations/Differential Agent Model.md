# Sistema Contínuo de Equações Diferenciais para o Agente Cognitivo

A seguir, definimos em notação LaTeX as equações diferenciais que modelam dinamicamente o estado interno do agente.

## Variáveis de Estado

- $m(t)$: nível médio de memória consolidada, $0 \le m \le 1$.
- $e_i(t)$: vetor de emoções, para $i=1,\dots,8$ representando \{joy, fear, anger, sadness, surprise, disgust, curiosity, calmness\}.
- $p_j(t)$: traços de personalidade dinâmicos, $j=1,\dots,P$, cada $0 \le p_j \le 1$.
- $n(t)$: estágio narrativo contínuo, de $0$ (Chamado) até $3$ (Retorno).
- $a_k(t)$: ativação de arquétipos, $k=1,\dots,A$.
- $s_l(t)$: sensibilidade sinestésica/fusão sensorial, $l=1,\dots,S$.
- $c(t)$: carga cognitiva (atenção), $c \ge 0$.

## Parâmetros

- $\alpha_m$: taxa de consolidação de memória.
- $\beta_m$: taxa de esquecimento.
- $\mathbf{\alpha_e} \in \mathbb{R}^{8\times(E+S)}$: matriz de acoplamento emocional entre memórias e simulações.
- $\gamma_e$: taxa de decaimento emocional.
- $\alpha_p$: taxa de adaptação de personalidade.
- $\alpha_n$: ritmo de progressão narrativa.
- $\gamma_n$: taxa de regressão narrativa.
- $\alpha_a$: acoplamento arquétipo → módulo emocional/memória.
- $\alpha_s$: sensibilidade sinestésica.
- $\gamma_s$: decaimento da sinestesia.
- $\alpha_c$: aumento de carga cognitiva por estímulos.
- $\gamma_c$: recuperação de carga cognitiva.

## Equações Diferenciais

1. **Memória Consolidada**:

$$
\frac{dm}{dt}
= \alpha_m \sum_{\mathrm{evt}} \mathrm{salience}(\mathrm{evt}) \,(1 - m)
- \beta_m \; m
$$

2. **Emoções (vetor)**:

$$
\frac{d\mathbf{e}}{dt}
= \mathbf{\alpha_e} \; [\mathrm{memories},\;\mathrm{simulations}]^T
- \gamma_e \; \mathbf{e}
$$

3. **Traços de Personalidade**:

$$
\frac{dp_j}{dt}
= \alpha_p \; \Delta\mathrm{experience}_j
- \lambda_p \; p_j
$$

4. **Estágio Narrativo**:

$$
\frac{dn}{dt}
= \alpha_n \; \mathrm{triggers}(\mathrm{event})
- \gamma_n \; n
$$

5. **Ativação de Arquétipos**:

$$
\frac{da_k}{dt}
= \alpha_a \; f_k(\mathrm{archetype}, \mathrm{context})
- \lambda_a \; a_k
$$

6. **Sinestesia / Fusão Sensorial**:

$$
\frac{ds_l}{dt}
= \alpha_s \; \mathrm{sensoryFusion}_l
- \gamma_s \; s_l
$$

7. **Carga Cognitiva**:

$$
\frac{dc}{dt}
= \alpha_c \; \mathrm{stimuliLoad}
- \gamma_c \; c
$$

## Observações

- Os termos auxiliares (por exemplo, $\mathrm{triggers}(\mathrm{event})$, $\Delta\mathrm{experience}$, $f_k$, $\mathrm{sensoryFusion}$, $\mathrm{stimuliLoad}$) são funções de entrada que devem ser definidas de acordo com o design do simulador.
- A integração numérica pode ser feita via Runge–Kutta de 4ª ordem com passo $\Delta t$.
