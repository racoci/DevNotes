Vimos nesse vídeo que a partir de uma instância podemos criar tanto uma imagem quanto um modelo.

Qual a diferença entre Imagem e Modelo que podemos criar a partir de uma instância existente?

- Alternativa incorreta
    
    Imagem e Modelo são sinônimos na AWS. Não há diferença.
    
    Imagem e Modelo não são sinônimos e entender sua diferença é bastante importante para gerenciarmos nossas instâncias.
    
- Alternativa incorreta
    
    Modelo é relacionado ao software enquanto Imagem é ao hardware.
    
    Na verdade é exatamente o contrário.
    
- Alternativa correta
    
    Imagem é relacionado ao software enquanto Modelo é ao hardware.
    
    Ao criarmos uma instância a partir de uma imagem, podemos selecionar todo o hardware (tipo de instância, rede, etc) e algum software já vem pré-instalado. No exemplo da aula foi o Nginx. Já com o Modelo, nós podemos selecionar qualquer imagem e o hardware já estará pré-configurado. Inclusive nós criaremos um modelo mais adiante no curso para que a AWS possa criar instâncias automaticamente para nós.