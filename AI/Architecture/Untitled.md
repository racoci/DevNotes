### 1 Diferencial de Fréchet

Considere dois espaços vetoriais normados $(E,\|\cdot\|_E)$ e $(F,\|\cdot\|_F)$ e uma aplicação

$$
F:E\;\longrightarrow\;F .
$$

| passo       | ideia                                                                                                                         |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Gateaux** | Olha apenas direções individuais: $dF(x;\,h)=\displaystyle\lim_{\varepsilon\to0}\frac{F(x+\varepsilon h)-F(x)}{\varepsilon}$. |
| **Fréchet** | Exige que *uma única aplicação linear* $DF(x)\in\mathcal L(E,F)$ **aproxime $F$ uniformemente em todas as direções**:         |

$$
\lim_{\|h\|_E\to0}\frac{\|F(x+h)-F(x)-DF(x)\,h\|_F}{\|h\|_E}=0 .
$$ 

*Se o limite existe, dizemos que $F$ é Fréchet-diferenciável em $x$ e $DF(x)$ é o seu **diferencial de Fréchet**.*  
Para $E=F=\mathbb R^n$ isto coincide com o Jacobiano usual; para $E=L^2([0,1])$ e $F=L^2([0,1])$, $DF(x)$ torna-se um **operador integral** com núcleo $K_x(t,s)=\partial F(x)/\partial x(s)$.

---

### 2 Adjunto = “Jacobiano transposto” no espaço dual  
Num espaço de Hilbert $H$ o produto interno define um **isomorfismo canônico** entre o espaço e o seu dual $(\,\cdot\,)^\ast$.  Para um operador linear e contínuo  
$$
A:H\;\longrightarrow\;H,
$$

o **adjunto** $A^\ast$ é caracterizado por

$$
\langle Ax,\,y\rangle_H = \langle x,\,A^\ast y\rangle_H \quad \forall\,x,y\in H .
$$

* Quando $H=\mathbb R^n$ com produto interno euclidiano, $A^\ast$ é simplesmente $A^\top$.
* Para $H=L^2$, $A^\ast$ é a transposta (no sentido integral) do núcleo:
  $A^\ast f(t)=\int K(s,t)f(s)\,ds$.

---

### 3 Regra da cadeia na forma adjunta (= back-prop)

Suponha um functorial “grafo” de composições

$$
E\xrightarrow{F_1}H_1\xrightarrow{F_2}H_2\xrightarrow{\dots}H_m\xrightarrow{F_m}F.
$$

* **Regra da cadeia de Fréchet**

  $$
  D(F_m\!\circ\dots\!\circ F_1)(x)
    \;=\; DF_m(F_{m-1}\!\circ\!\dots)(\,\dots)\; \dots \; DF_1(x).
  $$
* **Back-prop**: para um funcional de perda $\mathcal L\colon F\to\mathbb R$ define-se
  $a_m = D\mathcal L\bigl(F_m\circ\dots\circ F_1(x)\bigr)\in F^\ast$
  e propaga-se *para trás* resolvendo

  $$
  a_{k-1}=a_k\circ DF_k(x_{k-1}) 
          \;=\; DF_k(x_{k-1})^\ast\,a_k,
  \qquad k=m,m-1,\dots,1.
  $$

Em outras palavras, **o gradiente recua aplicando sucessivamente os adjuntos dos diferenciais** — que, no caso finito-dimensional, são as transpostas dos Jacobianos.
No **método adjoint para ODEs** faz-se exatamente isso de forma *contínua*: o “laço” de back-prop torna-se uma ODE reversa com $DF^\ast$ no lugar de $DF$.

---

### 4 Do operador ao tensor (discretização)

| objeto analítico                                                        | representação depois da malha                        | tipo de tensor                       |
| ----------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------ |
| Função $f:[0,1]\!\to\!\mathbb R$                                        | vetor $f_i=f(d_i)$                                   | rank-1 (shape $D$)                   |
| Operador linear $A:L^2\!\to\!L^2$ com núcleo $K(t,s)$                   | matriz $A_{ij}=K(d_i,d_j)$                           | rank-2 (shape $D\times D$)           |
| **Super-operador** $S:\mathcal L\!\to\!\mathcal L$ do tipo $S(A)=U A V$ | quatro-índice $S_{pq,rs}=U_{pr}V_{sq}$               | rank-4 ($D\times D\times D\times D$) |
| “Hiper” (operador de super-operadores)                                  | tensor de ordem $2^k$ se você discretizar cada nível | rank $2^k$                           |

O **produto interno** usado em cada nível dita qual **reshape** o autograd executa para calcular o adjunto:

* nível funções  → produto interno discreto $f^\top g$
* nível operadores → produto de Frobenius $\mathrm{Tr}(A^\top B)$
      $\Downarrow$
  a transposta/Frobenius-adjunta vira simplesmente `tensor.permute` e `einsum` no código.

> **Concretamente em PyTorch** todo operador linear contínuo que age numa grade de $D$ pontos vira um tensor `(..., D, D)`; se ele próprio é argumento de um outro mapa linear, este se realiza como um tensor `(..., D, D, D, D)` cuja contração por `einsum` implementa a aplicação do super-operador.  O autograd gera automaticamente o adjunto porque sabe derivar (e transpor) essas contrações.

---

### 5 Resumo em uma frase

*O **diferencial de Fréchet** dá o “Jacobiano genuíno” mesmo em espaços de funções; o **adjunto** é o seu transposto generalizado.  Propagar gradientes (back-prop) nada mais é que aplicar esses adjuntos de trás - para - frente, e, após discretizar o domínio, cada operador ou super-operador torna-se um tensor cuja adjunta é automaticamente gerida pelo mesmo mecanismo de autograd que usamos em redes convencionais.*
