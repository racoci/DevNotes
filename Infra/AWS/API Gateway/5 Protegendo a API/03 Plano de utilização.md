Agora que você já tem a chave da API, crie um plano de utilização para que possamos usar essa chave na API, e mais importante, usar a chave apenas na seção de controle de API, onde subimos e deletamos imagens.

Se tiver alguma dúvida de como criar um plano de utilização, vá até a parte de "Opinião do instrutor" para um passo a passo


Criar um plano de utilização no API Gateway da AWS envolve alguns passos no Console de Gerenciamento da AWS.

1. **Abra a guia "Plans" (Planos):**
    
    - Na página da API selecionada, vá para a guia "Plans" no menu lateral esquerdo.
2. **Crie um novo plano:**
    
    - Clique no botão "Create" (Criar) para criar um novo plano.
3. **Configure o plano:**
    
    - **Name (Nome):** Escolha um nome que tenha um significado para o seu plano, preferencialmente com o nome da aplicação para ficar de fácil identificação.
    - **Description (Descrição):** Forneça uma descrição.
    - **API Stages (Estágios da API):** Selecione as APIs e os estágios associados ao plano.
4. **Configurações do plano:**
    
    - **Taxa:** Configure limites de taxa ou acessos totais por segundo a API.
    - **Pico:** Configure o limite de solicitações simultâneas de um único cliente.
    - **Cota:** Defina uma cota diária ou mensal para as chamadas da API de um único cliente.
5. **Clique em "Create" (Criar):**
    
    - Após configurar todas as opções, clique no botão "Create" (Criar) para criar o plano de utilização.

Agora, seu plano de utilização foi criado e associado à sua API no API Gateway da AWS.