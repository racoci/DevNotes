### 1 Do CPT discreto ao “CPT” em log-função característica

Num nó discreto **$C\mid A,B$**, a representação clássica é um **CPT**, isto é, uma função

$$
P_{C\mid A,B}:\;D_A\times D_B \;\longrightarrow\;\Delta(D_C),
$$

onde para cada par $(a,b)$ temos a lista $\{P(C=c\mid A=a,B=b)\}_{c\in D_C}$.

Em vez disso, definimos para cada $(a,b)$ a **função característica condicional**

$$
\varphi_{C\mid A,B}(t\mid a,b)
\;=\;
\E\bigl[e^{\,i\,t\,C}\mid A=a,B=b\bigr]
\;=\;\sum_{c\in D_C} e^{\,i\,t\,c}\;P(C=c\mid a,b).
$$

E trabalhamos com o seu **logaritmo**:

$$
\Psi_{C\mid A,B}(t\mid a,b)
=\ln\bigl(\varphi_{C\mid A,B}(t\mid a,b)\bigr).
$$

**Assinatura**:

$$
\Psi_{C\mid A,B}:\;
\underbrace{\R}_{t}\;\times\;
\underbrace{D_A}_{a}\;\times\;\underbrace{D_B}_{b}
\;\longrightarrow\;
\C.
$$

Em vez de guardar uma tabela $\lvert D_A\rvert\times\lvert D_B\rvert$ de vetores em $\Delta(D_C)$, guardamos uma **função** $\Psi(t\mid a,b)$.

---

### 2 Mudança de domínios via bijeção $(A,B)\!\leftrightarrow\!(X,Y)$

Suponha que exista uma bijeção

$$
p:\;D_A\times D_B \;\longrightarrow\;D_X\times D_Y,
\quad
q = p^{-1}.
$$

Definimos a característica condicionada a $(X,Y)$ por

$$
\varphi_{C\mid X,Y}(t\mid x,y)
\;=\;
\E\bigl[e^{\,i\,t\,C}\mid X=x,Y=y\bigr]
\;=\;
\E\bigl[e^{\,i\,t\,C}\mid A=a,B=b\bigr]
\quad\text{com }(a,b)=q(x,y).
$$

Tomando logaritmo:

$$
\boxed{
\Psi_{C\mid X,Y}(t\mid x,y)
=\Psi_{C\mid A,B}\bigl(t\mid q(x,y)\bigr).
}
$$

**Assinatura**:

$$
\Psi_{C\mid X,Y}:\;
\R\times D_X\times D_Y\;\longrightarrow\;\C.
$$

---

### 3 Inferência usando somas e log-sum-exp

Num BN clássico, a factorização
$\;P(A,B,C)=P(A)\,P(B)\,P(C\mid A,B)$
leva a multiplicações de tabelas. Em log-função característica, a **característica conjunta** de $(A,B,C)$ satisfaz:

$$
\varphi_{A,B,C}(t_A,t_B,t_C)
=\varphi_A(t_A)\;\varphi_B(t_B)\;
\varphi_{C\mid A,B}(t_C\mid A,B)\;\text{avaliada em média sobre }A,B.
$$

Em log-espaço:

$$
\Psi_{A,B,C}(t_A,t_B,t_C)
=\Psi_A(t_A)+\Psi_B(t_B)
\;+\;\ln\E_{A,B}\!\bigl[e^{\Psi_{C\mid A,B}(t_C\mid A,B)}\bigr],
$$

onde o último termo é um **log-sum-exp** sobre $(a,b)$.

---

### 4 Resumo

* **Tabela $P(C\mid A,B)$** ↔ **função** $\Psi_{C\mid A,B}(t\mid a,b)$.
* **Multiplicação de prob.** ↔ **adição** de $\Psi$.
* **Marginalização em $A,B$** ↔ **log-sum-exp** de $\Psi_{C\mid A,B}$.
* **Mudança de variáveis** $(A,B)\!\to\!(X,Y)$ ↔ **substituir** $\Psi(t\mid a,b)$ por $\Psi\bigl(t\mid q(x,y)\bigr)$.

Dessa forma eliminamos completamente as tabelas tradicionais, substituindo-as por operações de **adição** e **log-sum-exp** sobre as **log-funções características**.
