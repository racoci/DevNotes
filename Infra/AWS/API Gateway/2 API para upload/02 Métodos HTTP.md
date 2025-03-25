Métodos HTTP (Hypertext Transfer Protocol) são comandos utilizados para indicar a ação desejada a ser executada em um recurso identificado. Eles especificam a operação que deve ser realizada no recurso quando uma solicitação é feita ao servidor web. Aqui estão alguns dos métodos HTTP mais comuns:

1. **GET:**
    
    - O método GET é usado para solicitar dados de um recurso específico.
    - Não deve ter efeitos colaterais no servidor, ou seja, não deve alterar o estado do servidor.
2. **POST:**
    
    - O método POST é utilizado para enviar dados para serem processados para um recurso especificado.
    - Pode causar efeitos colaterais no servidor, como a criação de um novo recurso ou a atualização de dados existentes.
3. **PUT:**
    
    - O método PUT é usado para atualizar um recurso existente ou criar um novo, caso não exista.
    - Geralmente, é utilizado para atualizar completamente um recurso.
4. **PATCH:**
    
    - Semelhante ao PUT, mas o método PATCH é utilizado para aplicar modificações parciais a um recurso.
    - É útil quando você quer atualizar apenas parte dos dados de um recurso.
5. **DELETE:**
    
    - O método DELETE é usado para solicitar a remoção de um recurso específico.
    - Assim como o GET, não deve ter efeitos colaterais no servidor.
6. **OPTIONS:**
    
    - O método OPTIONS é usado para descrever as opções de comunicação disponíveis para o recurso de destino.
    - Geralmente é utilizado para solicitar informações sobre os métodos permitidos ou requisitos de cabeçalho antes de fazer uma solicitação real.
7. **HEAD:**
    
    - Semelhante ao GET, mas o método HEAD é usado para obter apenas os cabeçalhos da resposta, sem o corpo da mensagem.
    - É útil para verificar metadados sem recuperar o conteúdo completo do recurso.
8. **TRACE:**
    
    - O método TRACE é usado para realizar um teste de loop-back ao longo do caminho da requisição, fornecendo uma maneira de diagnosticar problemas de comunicação.

Estes são alguns dos métodos HTTP mais comuns, cada um com um propósito específico. A escolha do método depende da operação que você deseja realizar no recurso e do comportamento desejado em termos de efeitos colaterais no servidor.

Nossa API já tem um método POST disponibilizado na API padrão e acabamos de criar um método DELETE para permitir a remoção de imagens e arquivos.