# SmartStudyBuddy
Você quer uma **proposta de projeto completa** para o “SmartStudyBuddy” que descreva em detalhes a **arquitetura** (todas as camadas LMSI) e sugira **prompts** e **ferramentas** para **automatizar** ao máximo a construção, desde o scaffold do código até o deploy em nuvem.

**Premissas implícitas**

* Você possui conhecimento em Angular, NestJS, Kubernetes, Terraform e LLMs.
* Quer acelerar o desenvolvimento usando geração de código e pipelines automatizados.
* A solução deve ser replicável e documentada “como código”.

---

## Estratégia de Resposta e Comprovação

1. **Visão Geral Arquitetural**: Descrever cada camada LMSI, componentes e responsabilidades.
2. **Diagramas Lógicos**: Mapear fluxos de dados e integrações.
3. **Automação de Scaffold**: Sugerir prompts para ChatGPT/GitHub Copilot e usar Angular Schematics, NestJS CLI, Yeoman, etc.
4. **Infraestrutura como Código**: Propor Terraform para GCP, Dockerfiles, Kubernetes YAML, e GitHub Actions.
5. **Templates de Prompt**: Fornecer exemplos detalhados de prompts para as fases de Prompting, Orquestração e Execução.
6. **Ferramentas Extra**: Indicar serviços e bibliotecas auxiliares (CI/CD, monitoramento, testes).
7. **Pipeline End-to-End**: Mostrar como tudo se conecta num fluxo automatizado.

Cada escolha virá acompanhada de referências aos docs oficiais ou blogs de usuários experientes, para você validar a abordagem.

---

## 1. Visão Geral da Arquitetura “SmartStudyBuddy”

```plaintext
┌───────────────────────────────────────────────────────────────────┐
│                          Aplicação                              │
│        (Angular 17 + Tailwind + Socket.IO + NgRx)              │
└───────────────────────────────────────────────────────────────────┘
          ↓ HTTP / WebSocket                         ↑
┌───────────────────────────────────────────────────────────────────┐
│                         Orquestração                           │
│              (LangChain + Agents Guidance + CrewAI)            │
└───────────────────────────────────────────────────────────────────┘
          ↓ Chamada API LLM + Ferramentas                         ↑
┌───────────────────────────────────────────────────────────────────┐
│           Prompting & Execução (Guidance + CrewAI Agents)      │
└───────────────────────────────────────────────────────────────────┘
          ↓ Saída Estruturada                                     ↑
┌───────────────────────────────────────────────────────────────────┐
│                         Interpretação                          │
│ (LlamaIndex RAG + Guardrails AI + TruLens para confidência)    │
└───────────────────────────────────────────────────────────────────┘
          ↓ Embeddings / JSON                                      ↑
┌───────────────────────────────────────────────────────────────────┐
│                 Interface de Modelo                            │
│      (vLLM / FastChat local ou fallback OpenAI API)            │
└───────────────────────────────────────────────────────────────────┘
          ↓ RPC / HTTP                                            ↑
┌───────────────────────────────────────────────────────────────────┐
│                       Infraestrutura                           │
│   (Docker, Kubernetes, GCP via Terraform, Redis, Logging/Prom) │
└───────────────────────────────────────────────────────────────────┘
```

---

## 2. Automação do Scaffold de Código

### 2.1. Frontend Angular + Tailwind

* **Ferramenta**: Angular CLI + [ngx-tailwind](https://github.com/johanmont/ngx-tailwind) schematic
* **Prompt para ChatGPT**

  ```
  /system
  Gerei um monorepo Nx com Angular 17 e Tailwind integrado via ngx-tailwind.
  Quero gerar três módulos:
  - ArticleModule com UploadArticleComponent e PipelineStatusComponent.
  - ResultsModule com SummaryComponent, ConfidenceMapComponent e TaskListComponent.
  - ChatModule com ChatComponent e CitationButtonsComponent.
  Cada componente deve usar Tailwind para estilo (p-4, rounded-2xl, shadow-md) e RxJS para WebSocket.
  Me dê o comando CLI exato e o código base de cada componente.
  ```

* **Como usar**:
  1. `npx create-nx-workspace smart-study-buddy --preset=angular`
  2. `nx generate @johanmont/ngx-tailwind:setup`
  3. Colar no ChatGPT o prompt acima para gerar `nx g @schematics` scripts ou copiar/colar do retorno.

### 2.2. Backend NestJS

* **Ferramenta**: NestJS CLI + TypeORM + Socket.IO adapter
* **Prompt para ChatGPT**

  ```
  /system
  Gerei um projeto NestJS com módulos:
  - ArticlesModule (serviço para download + pre-processamento de PDF).
  - PipelineModule (orquestra Chain LangChain).
  - ChatModule (WebSocket Gateway e Controllers para chat e citações).
  Configure TypeORM com PostgreSQL e RedisCacheModule. Forneça a estrutura dos Controllers, Services e DTOs.
  ```
* **Automação**:

  1. `nest new backend`
  2. `nest g module articles && nest g service articles` etc.
  3. Usar prompt acima no Copilot/ChatGPT.

---

## 3. Infraestrutura como Código (Terraform + Docker + K8s)

### 3.1. Terraform para GCP

* **Módulos**:

  * `google_project` + `google_kubernetes_cluster`
  * `google_sql_database_instance` (PostgreSQL)
  * `google_redis_instance`
* **Prompt para ChatGPT**

  ```
  /system
  Gere um módulo Terraform em GCP que:
  - Crie um GKE autopilot cluster.
  - Provisione Cloud SQL PostgreSQL com usuário e DB.
  - Provisione Memorystore Redis.
  - Exporte as saídas para usar nos manifests Kubernetes do backend.
  ```
* **Automação**:

  1. `terraform init`
  2. `terraform apply -auto-approve`
  3. `terraform output -json > infra/outputs.json`

### 3.2. Docker & Kubernetes

* **Dockerfiles**: Um para frontend, outro para backend, config de multi-stage builds.
* **Manifests K8s**:

  * Deployment/Service para frontend, backend, vLLM/pod de modelo, Redis.
  * Ingress NGINX para roteamento HTTP/WebSocket.
* **Prompt para ChatGPT**

  ```
  /system
  Com base no outputs.json do Terraform, gere:
  - Dockerfile para backend NestJS (multi-stage, porta 3000).
  - Dockerfile para frontend Angular (serve estático).
  - K8s Deployment+Service para cada serviço e um Ingress para domínio.
  ```
* **Automação**:

  1. `docker build -t gcr.io/$PROJECT/backend:latest backend/`
  2. `kubectl apply -f k8s/`

---

## 4. Pipelines CI/CD e Monitoramento

* **GitHub Actions**

  * Workflow `ci.yml`: lint, test (Angular + Jest + e2e Cypress), build Docker images.
  * Workflow `deploy.yml`: após merge em `main`, roda Terraform, então `kubectl apply`.
* **Prompts**

  ```
  /system
  Gere um GitHub Actions workflow que:
  - Use Node.js 20.
  - Instale dependências do monorepo Nx.
  - Rode `nx affected:lint,test,build`.
  - Faça login no GCP via OIDC e rode `terraform apply`.
  - Construa e publique imagens Docker no GCR.
  - Rode `kubectl apply` usando konteks do GKE.
  ```
* **Monitoramento**: Prometheus + Grafana no cluster (Helm charts).

---

## 5. Templates de Prompt & Engenharia de Prompting

* **Sumarização (Guidance)**

  ```python
  from guidance import Prompt

  summarize = Prompt("""
  Você é um assistente acadêmico. Dado o trecho entre """ + '"""{text}"""' + """:
  1. Gere um sumário em até 5 tópicos.
  2. Para cada tópico, forneça uma “confiança” entre 0 e 1.
  Formato de saída: 
  {{
    "summary": [
      {{ "point": "...", "confidence": 0.87 }},
      ...
    ]
  }}
  """)
  ```
* **Planejamento de Tarefas**
```python
  tasks = Prompt("""
  Com base neste sumário JSON {summary}:
  1. Gere uma lista de 5 “tarefas de estudo” acionáveis.
  2. Cada tarefa deve ter “title” e “dueInDays”.
  Saída JSON:
  {{
    "tasks": [
      {{ "title": "...", "dueInDays": 3 }},
      ...
    ]
  }}
  """)
```
* **Fallback & Retries com Guardrails**

  * Em cada chamada, incorpore validação de JSON Schema usando Guardrails para retry automático.

---

## 6. Orquestração (LangChain + CrewAI)

* **Prompt de Setup de Agent**

```python
  from langchain.agents import Agent, Tool

  summarizer_tool = Tool(
    name="summarizer",
    func=lambda text: summarize(text=text).strip(),
    description="Gera sumário estruturado de texto acadêmico."
  )
  planner_tool = Tool(
    name="task_planner",
    func=lambda summary: tasks(summary=summary).strip(),
    description="Cria tarefas de estudo a partir de sumário JSON."
  )

  agent = Agent(
    tools=[summarizer_tool, planner_tool],
    llm=OpenAI(...),
    verbose=True
  )
```
* **Fluxo**
  1. Agent recebe URL → chama service de download.
  2. Extrai texto → chama `summarizer_tool`.
  3. Passa resultado para `planner_tool`.
  4. Aplica Guardrails e retorna ao frontend via WebSocket.

---

## 7. Execução & Modelos

* **Servir Modelo**:

  * **vLLM** rodando LLaMA/Vicuna em pod GPU.
  * **Fallback**: OpenAI API via `OpenAI()` no Agent.
* **Prompting Dinâmico**: gerar embeddings via LlamaIndex para “context windows”.

---

### Conclusão

Com esta proposta, cada etapa — do scaffold do monorepo e componentes, passando pelos prompts detalhados, até a infraestrutura automatizada e pipelines CI/CD — está descrita e acompanhada de **prompts** para ChatGPT/GitHub Copilot e **ferramentas como código**. Assim você terá um **projeto totalmente replicável**, onde cada camada LMSI é demonstrada e orquestrada, e a maior parte do trabalho manual é delegada a **engenharia de prompts** e **Infraestrutura como Código**.
