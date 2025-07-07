A seguir reescrevo o argumento de que a **perda de *flow-matching* marginal**
$\mathcal{L}_{\mathrm{FM}}$ difere da condicional $\mathcal{L}_{\mathrm{CFM}}$ apenas por uma constante, desta vez

* explicitando **todas as distribuições** (com notação $\mathcal{N},\mathcal{U}$);
* mostrando os **limites das integrais** e definindo previamente os conjuntos envolvidos;
* usando $\displaystyle\mathcal{L}$ para a perda e **fontes distintas** ($\mathcal{·}$ para distribuições, $\mathbf{·}$ para vetores, $\mathrm{·}$ para objetos determinísticos);
* empregando $\underset{\text{···}}{\mathbb{E}}$ vertical para que cada variável apareça em linha separada;
* realçando **de azul** o termo que será modificado no passo seguinte e **de verde** o que acabou de ser modificado no passo atual.

---

## 1. Definições preliminares

* Espaço dos dados: $\mathsf{X}\subseteq\mathbb{R}^d$.
* Espaço latente: $\mathsf{Z}\subseteq\mathbb{R}^d$.
* Intervalo temporal: $\mathcal{T}:=[0,1]$.

$$
\begin{aligned}
&T\;\sim\;\mathcal{U}(0,1), 
&&Z\;\sim\;\mathcal{P}_{\mathrm{data}}\,,\\[4pt]
&X\;\big|\;(T=t,\;Z=z)\;\sim\;p_t(\cdot\mid z),
&&X\;\big|\;T=t\;\sim\;p_t \;=\int_{\mathsf{Z}}\!p_t(\cdot\mid z)\;\mathcal{P}_{\mathrm{data}}(\mathrm{d}z).
\end{aligned}
$$

---

## 2. Perdas marginal e condicional

$$
\boxed{
\mathcal{L}_{\mathrm{FM}}(\theta)
:=\underset{
  \begin{array}{c}
    T\sim\mathcal{U}(0,1)\\[2pt]
    X\sim p_T
  \end{array}
}{\mathbb{E}}
  \Bigl\lVert
    \mathbf{u}^{\theta}_{T}(\mathbf{X})
    -\mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X})
  \Bigr\rVert_2^{2}
}\qquad\qquad
\boxed{
\mathcal{L}_{\mathrm{CFM}}(\theta)
:=\underset{
  \begin{array}{c}
    T\sim\mathcal{U}(0,1)\\
    Z\sim\mathcal{P}_{\mathrm{data}}\\
    X\sim p_T(\cdot\mid Z)
  \end{array}
}{\mathbb{E}}
  \Bigl\lVert
    \mathbf{u}^{\theta}_{T}(\mathbf{X})
    -\mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X}\mid Z)
  \Bigr\rVert_2^{2}
}
$$

---

## 3. Passo a passo da prova

### Passo A – Expandir o quadrado

$$
\mathcal{L}_{\mathrm{FM}}(\theta)=
\underset{\substack{T,X}}{\mathbb{E}}
\Bigl[\,
\underbrace{\lVert\mathbf{u}^{\theta}_{T}(\mathbf{X})\rVert^2}_{\text{(i)}}\!
-\;
\color{blue}{2\,\mathbf{u}^{\theta}_{T}(\mathbf{X})^{\!\top}
             \mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X})}\;
+\;
\lVert\mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X})\rVert^2
\Bigr]
\tag{A}
$$

### Passo B – Isolar o termo constante

(somente $\mathbf{u}^{\mathrm{target}}$; marcado **verde** porque foi alterado deste passo para o anterior)

$$
\mathcal{L}_{\mathrm{FM}}(\theta)=
\underset{\substack{T,X}}{\mathbb{E}}
\bigl[\lVert\mathbf{u}^{\theta}_{T}(\mathbf{X})\rVert^2\bigr]
-\;
\color{green}{2\,\underset{\substack{T,X}}{\mathbb{E}}
  \bigl[\mathbf{u}^{\theta}_{T}(\mathbf{X})^{\!\top}
        \mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X})\bigr]}
+\;
\cancelto{C_1}{\underset{\substack{T,X}}{\mathbb{E}}
   \lVert\mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X})\rVert^2}
\tag{B}
$$

> $C_1$ é **constante em $\theta$**. (cf. notas, linha (iii) do Teorema 18)&#x20;

### Passo C – Reescrever o **termo cruzado** via truque da marginalização

(substitui-se $\mathbf{u}^{\mathrm{target}}_{T}$ pela média condicional; o que muda agora está **azul**)

$$
\begin{aligned}
&\underset{\substack{T,X}}{\mathbb{E}}
  \bigl[\mathbf{u}^{\theta}_{T}(\mathbf{X})^{\!\top}
        \mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X})\bigr]
\\[4pt]
&\quad=\;
\int_{\mathcal{T}}\!\int_{\mathsf{X}}
  \mathbf{u}^{\theta}_{t}(\mathbf{x})^{\!\top}
  \Bigl[
    \int_{\mathsf{Z}}
      \mathbf{u}^{\mathrm{target}}_{t}(\mathbf{x}\mid z)
      \frac{p_t(\mathbf{x}\mid z)\,\mathcal{P}_{\mathrm{data}}(\mathrm{d}z)}
           {p_t(\mathbf{x})}
  \Bigr]\,
  p_t(\mathbf{x})\,
  \mathrm{d}\mathbf{x}\,\mathrm{d}t
\\[4pt]
&\quad=\;
\underset{
  \begin{array}{c}
    T\sim\mathcal{U}(0,1)\\
    Z\sim\mathcal{P}_{\mathrm{data}}\\
    X\sim p_T(\cdot\mid Z)
  \end{array}
}{\mathbb{E}}
  \bigl[\mathbf{u}^{\theta}_{T}(\mathbf{X})^{\!\top}
        \mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X}\mid Z)\bigr]
\end{aligned}
\tag{C}
$$

*(ver linhas (ii)–(iv) da prova nas notas) *

### Passo D – Substituir (C) em (B)

(o termo azul de (B) vira verde aqui)

$$
\mathcal{L}_{\mathrm{FM}}(\theta)=
\underset{\substack{T,Z,X}}{\mathbb{E}}\!
  \bigl[
    \lVert\mathbf{u}^{\theta}_{T}(\mathbf{X})\rVert^2
    -\;
    \color{green}{2\,\mathbf{u}^{\theta}_{T}(\mathbf{X})^{\!\top}
                  \mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X}\mid Z)}
  \bigr]
+\;C_1
\tag{D}
$$

### Passo E – Completar o quadrado e identificar a perda condicional

(o termo que será eliminado no próximo passo está **azul**)

$$
\begin{aligned}
\mathcal{L}_{\mathrm{FM}}(\theta)
&=\underset{\substack{T,Z,X}}{\mathbb{E}}
   \Bigl[
     \lVert\mathbf{u}^{\theta}_{T}(\mathbf{X})
          -\mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X}\mid Z)\rVert^2
     \;\color{blue}{-\lVert\mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X}\mid Z)\rVert^2}
   \Bigr]
\;+\;C_1 \\[6pt]
&=\underbrace{\mathcal{L}_{\mathrm{CFM}}(\theta)}_{\text{def. acima}}
   \;+\;
   \cancelto{C_2}{
     -\underset{\substack{T,Z,X}}{\mathbb{E}}
      \lVert\mathbf{u}^{\mathrm{target}}_{T}(\mathbf{X}\mid Z)\rVert^2}
   \;+\;C_1
\end{aligned}
\tag{E}
$$

### Passo F – Conclusão

$$
\boxed{
\mathcal{L}_{\mathrm{FM}}(\theta)=
\mathcal{L}_{\mathrm{CFM}}(\theta)
+\underbrace{(C_1+C_2)}_{=:C}
}
\qquad\Longrightarrow\qquad
\nabla_{\theta}\mathcal{L}_{\mathrm{FM}}
=
\nabla_{\theta}\mathcal{L}_{\mathrm{CFM}}
$$

que é exatamente o enunciado do **Teorema 18** .

---

## 4. Comentários finais

* Os termos $C_1$ e $C_2$ dependem apenas de $\mathbf{u}^{\mathrm{target}}$, logo **são constantes** em relação a $\theta$; minimizando $\mathcal{L}_{\mathrm{CFM}}$ já minimizamos $\mathcal{L}_{\mathrm{FM}}$.
* O “peso” de Bayes
  $\displaystyle w_t(z\mid x)=\frac{p_t(x\mid z)\,\mathcal{P}_{\mathrm{data}}(z)}{p_t(x)}$
  reaparece naturalmente no passo C como consequência do **truque da marginalização**.
* A distinção de fontes ($\mathcal{·}$, $\mathbf{·}$, $\mathrm{·}$) ajuda a lembrar:
  $\mathcal{·}$ → distribuições/conjuntos; $\mathbf{·}$ → vetores/campos; $\mathrm{·}$ → funções, constantes ou operadores.

Com isso, fica claro — passo a passo e com toda a notação explícita — por que a perda marginal difere da condicional apenas por uma constante.


### Onde surge o peso $w_t(z\mid x)=\dfrac{p_t(x\mid z)\,p_{\text{data}}(z)}{p_t(x)}$ ?

1. **Queremos a média condicional do campo**
   O campo marginal é definido por

   $$
     u_t(x)=\mathbb{E}\!\bigl[u^{\text{cond}}_t(x\mid Z)\,\big\vert\,X_t=x\bigr]
           =\int u^{\text{cond}}_t(x\mid z)\,
             \underbrace{\frac{p_t(x\mid z)\,p_{\text{data}}(z)}{p_t(x)}}_{w_t(z\mid x)}
           dz, 
   \tag{1}
   $$

   exatamente a equação (19) das notas .
   O fator em destaque é simplesmente a **\[posterior weighting]** $p(Z=z\mid X_t=x)$.

2. **Relação direta com a inversão bayesiana**
   Compare (1) com a forma geral da \[Bayes’ rule] para densidades

   $$
     p_{Y\mid X}(y\mid x)=\frac{p_{X\mid Y}(x\mid y)\,p_Y(y)}{p_X(x)}:contentReference[oaicite:1]{index=1}.
   $$

   Basta identificar $Y\mapsto Z$ e $X\mapsto X_t$ para ver que

   $$
     w_t(z\mid x)=p(Z=z\mid X_t=x).
   $$

   Assim, o “truque da marginalização” não é nada além de **usar Bayes para inverter o condicionamento** e obter a distribuição de $Z$ *dado* o ponto atual $x$.

3. **Por que ele aparece também no *score* marginal?**
   O score marginal é

   $$
     \nabla_x\log p_t(x)=\mathbb{E}\!\left[\nabla_x\log p_t(x\mid Z)\,\middle\vert\,X_t=x\right],
   $$

   de novo a mesma média condicional — portanto com o mesmo peso.
   Nas notas, essa decomposição é usada, por exemplo, na eq. (67) para derivar guidance .

---

### Passando para \[logits] (log-odds)

Suponha $Z$ **discreto** com categorias $k=1,\dots,K$.
Defina o *logit* relativo a uma classe de referência $k_0$:

$$
\text{logit}_{k,k_0}(x,t)
   =\log\frac{p(Z=k\mid X_t=x)}{p(Z=k_0\mid X_t=x)}
   =\underbrace{\log\frac{p_{\text{data}}(k)}{p_{\text{data}}(k_0)}}_{\text{prior log-odds}}
    \;+\;
    \underbrace{\log\frac{p_t(x\mid k)}{p_t(x\mid k_0)}}_{\text{likelihood ratio}}.
\tag{2}
$$

* O termo $\log p_t(x)$ **cancela** — ele não depende de $k$.
* Logo (2) separa a contribuição do **\[prior]** da de evidência vinda de $x$, exatamente como na regressão logística.

Em notação de “energia” (útil no caso contínuo):

$$
w_t(z\mid x)=\frac{\exp\bigl[-E_t(x,z)\bigr]}{Z_t(x)},\qquad
E_t(x,z)\equiv -\log p_t(x\mid z)-\log p_{\text{data}}(z),
$$

onde $Z_t(x)=p_t(x)$ é a \[log-partition function] (evidence).
O *logit* entre dois valores $z,z'$ é então $\log\frac{w_t(z\mid x)}{w_t(z'\mid x)}=E_t(x,z')-E_t(x,z)$.

---

### Intuição resumida

* **Marginalizar** é “esquecer” $z$; para isso ponderamos tudo pela **posterior** $p(z\mid x)$.
* Esse peso é obtido **invertendo o condicional** via Bayes – o mesmo truque que usamos na estatística para trocar $p(x\mid z)$ por $p(z\mid x)$.
* Escrever em termos de **logits** deixa explícita a soma *prior + evidência* e mostra o paralelismo com modelos lineares de classificação.

Com isso, o fator que converte campos ou scores condicionais para marginais deixa de ser um “truque” misterioso e vira apenas “Bayes aplicado na veia” – agora também pronto para quem prefere raciocinar em escala log-odds.
