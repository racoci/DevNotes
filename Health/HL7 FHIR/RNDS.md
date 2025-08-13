## Guia Passo a Passo: Conectando-se ao Ambiente de Homologação da RNDS

Este guia descreve o processo técnico e administrativo para que uma organização ou equipe de desenvolvimento possa se conectar e realizar testes no ambiente de homologação (também conhecido como sandbox) da Rede Nacional de Dados em Saúde (RNDS). Este ambiente é crucial para validar a conformidade de um sistema com os padrões do SUS Digital antes de solicitar o acesso ao ambiente de produção.

### **Fase 1: Pré-requisitos e Preparação**

Antes de iniciar o processo de solicitação, é fundamental garantir que sua organização e seu software atendam a certos requisitos básicos.

- **Requisitos Organizacionais:**
    - **CNPJ Válido:** A solicitação de acesso é institucional. É necessário ter um CNPJ válido, seja de uma empresa de software, uma instituição de saúde ou uma entidade governamental.
    - **Responsável Técnico:** Designar um responsável técnico que será o ponto de contato com a equipe do DataSUS.
        
- **Requisitos Técnicos do Software:**
    - **Capacidade de Gerar Recursos HL7 FHIR:** Seu sistema deve ser capaz de criar, ler e manipular dados no padrão HL7 FHIR (versão R4), que é a "língua franca" da RNDS.
    - **Cliente HTTP Seguro:** O software deve ser capaz de realizar chamadas de API RESTful seguras, utilizando o protocolo HTTPS com TLS 1.2 ou superior.
    - **Certificado Digital:** A organização precisará de um certificado digital do tipo e-CNPJ (padrão ICP-Brasil) para assinar as requisições, garantindo a autenticidade e a não repudiação das transações.
        

### **Fase 2: Solicitação Formal de Acesso**

O acesso ao ambiente de homologação não é público e requer uma solicitação formal junto ao Ministério da Saúde.

**Passo 2.1: Acessar o Portal de Serviços do DataSUS** A porta de entrada para os serviços da RNDS é o Portal de Serviços do DataSUS. É neste portal que se encontram os formulários e a documentação oficial.

**Passo 2.2: Preencher o Formulário de Solicitação** Procure pelo "Formulário de Solicitação de Acesso ao Barramento de Serviços da RNDS". Este formulário solicitará informações como:

- Dados da instituição (Razão Social, CNPJ).
- Dados do responsável técnico (Nome, CPF, e-mail, telefone).
- Descrição do sistema que será integrado.
- Finalidade da integração (ex: "Integração de Prontuário Eletrônico do Paciente para o projeto e-Saúde Mental").
  - Declaração de conformidade com a Lei Geral de Proteção de Dados (LGPD).
    

**Passo 2.3: Aguardar Análise e Recebimento das Credenciais** Após o envio, a equipe do DataSUS analisará a solicitação. Se aprovada, sua organização receberá por e-mail as credenciais de acesso exclusivas para o ambiente de homologação. Estas credenciais geralmente incluem:

- `client_id`
- `client_secret`
    

### **Fase 3: Configuração Técnica do Ambiente**

Com as credenciais em mãos, a equipe de desenvolvimento pode iniciar a configuração técnica para a primeira conexão.

**Passo 3.1: Obtenção do Token de Acesso (OAuth 2.0)** A RNDS utiliza o padrão OAuth 2.0 para autenticação. Antes de enviar qualquer dado de saúde, seu sistema precisa obter um token de acesso.

Isso é feito através de uma chamada `POST` para o endpoint de autenticação do ambiente de homologação da RNDS, enviando o `client_id` e o `client_secret` recebidos.

**Exemplo de Requisição de Token (usando `curl`):**

```
curl -X POST 'https://auth-hmg.rnds.saude.gov.br/token' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'grant_type=client_credentials&client_id=SEU_CLIENT_ID&client_secret=SEU_CLIENT_SECRET'
```

A resposta será um JSON contendo o `access_token`. Este token é temporário e deve ser incluído em todas as chamadas subsequentes para a API da RNDS.

**Passo 3.2: Configuração dos Endpoints da API** As URLs para o ambiente de homologação são diferentes das de produção. O endpoint base para as operações FHIR no ambiente de homologação é tipicamente:

`https://fhir-hmg.rnds.saude.gov.br/v1/`

Portanto, para enviar um recurso `Patient`, o endpoint completo seria `https://fhir-hmg.rnds.saude.gov.br/v1/Patient`.

### **Fase 4: Testando a Conexão - Primeira Chamada**

O teste mais comum para validar a conexão é o envio de um recurso `Patient` (paciente fictício).

**Passo 4.1: Construir um Recurso `Patient` em FHIR JSON** Crie um objeto JSON representando um paciente, seguindo o perfil FHIR definido pela RNDS. Utilize um CPF fictício válido (gerado por ferramentas online para desenvolvedores).

**Exemplo de Recurso `Patient`:**

```
{
  "resourceType": "Patient",
  "identifier": [
    {
      "system": "urn:ietf:rfc:3986",
      "value": "urn:cpf:12345678901" 
    }
  ],
  "name": [
    {
      "use": "official",
      "text": "Maria da Silva Teste"
    }
  ],
  "gender": "female",
  "birthDate": "1985-07-20"
}
```

**Passo 4.2: Realizar a Chamada `POST`** Envie o recurso `Patient` para o endpoint correspondente, incluindo o token de acesso no cabeçalho `Authorization`.

**Exemplo de Envio do Paciente (usando `curl`):**

```
curl -X POST 'https://fhir-hmg.rnds.saude.gov.br/v1/Patient' \
-H 'Authorization: Bearer SEU_ACCESS_TOKEN' \
-H 'Content-Type: application/fhir+json' \
-d '{ "resourceType": "Patient", ... }'
```

**Passo 4.3: Verificar a Resposta**

- **Sucesso:** Uma resposta `201 Created` indica que o recurso foi criado com sucesso no servidor da RNDS. O corpo da resposta geralmente contém o recurso criado com um ID atribuído pelo servidor.
    
- **Erro:** Respostas como `400 Bad Request` indicam um erro no formato do seu recurso FHIR. Respostas `401 Unauthorized` indicam um problema com seu token de acesso. Analise o corpo da resposta de erro para obter detalhes sobre o problema.
    

### **Fase 5: Próximos Passos**

Após conectar e enviar com sucesso o primeiro paciente, os próximos passos incluem:

- **Testar outros Recursos:** Continue testando o envio de outros recursos FHIR relevantes para o seu sistema, como `Observation`, `QuestionnaireResponse` e `DiagnosticReport`, sempre utilizando os perfis especificados na documentação da RNDS.
- **Consultar a Documentação Oficial:** A documentação da RNDS é a fonte primária de verdade. Consulte-a frequentemente para entender os perfis de recursos (regras de preenchimento) e os guias de implementação (`Implementation Guides - IGs`).
- **Solicitar Acesso à Produção:** Uma vez que todos os testes no ambiente de homologação sejam concluídos com sucesso, sua organização poderá seguir um processo semelhante para solicitar o acesso ao ambiente de produção.