Com base nas descrições detalhadas dos fluxos de cada papel no sistema "e-Saúde Mental no SUS" da nossa conversa anterior e das fontes fornecidas, apresento os diagramas em PlantUML para cada sub-seção. Estes diagramas ilustram a interação entre os atores e os componentes do sistema, conforme a arquitetura funcional tripartite.

### 1. O Paciente (Usuário Final)

O módulo do paciente visa transformá-lo em um **agente ativo na sua própria saúde mental**.

#### 1.1 Início da Jornada e Cadastro

Este fluxo detalha como o paciente acessa a plataforma e realiza seu cadastro inicial, marcando o começo de sua jornada no sistema.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

actor Paciente
participant "Aplicativo Móvel (e-Saúde Mental)" as App
database "Sistema e-Saúde Mental (Backend)" as Backend

Paciente -> App : **Acessa a plataforma** através de aplicativo móvel (Android/iOS)
activate App
App -> App : Exibe "Check-in Digital"
Paciente -> App : **Realiza Cadastro / Check-in Digital** (para acesso inicial ao protocolo de tratamento)
App -> Backend : Envia Dados de Cadastro
activate Backend
Backend -> Backend : Registra Paciente
Backend --> App : Confirma Cadastro / Acesso
deactivate Backend
App --> Paciente : **Acesso Concedido** ao Protocolo de Tratamento
deactivate App
@enduml
```

#### 1.2 Engajamento e Autoaplicação

Aqui, o diagrama mostra como o paciente interage com os recursos de autoajuda e psicoeducação oferecidos pelo aplicativo para o manejo diário de seus sintomas.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

actor Paciente
participant "Aplicativo Móvel (e-Saúde Mental)" as App
database "Sistema e-Saúde Mental (Conteúdo)" as ContentDB

Paciente -> App : Acessa conteúdo e ferramentas de autoajuda
activate App
App -> ContentDB : Solicita Conteúdo de Psicoeducação
ContentDB --> App : Envia Conteúdo (informações sobre transtornos, bem-estar)
App --> Paciente : **Exibe Conteúdo de Psicoeducação**
Paciente -> App : Seleciona Técnicas Autoaplicáveis
App --> Paciente : Orienta sobre **Técnicas de Regulação Emocional e Ativação Comportamental**
Paciente -> Paciente : Aplica Técnicas no dia a dia para manejar sintomas
deactivate App
@enduml
```

#### 1.3 Fluxo de Autoavaliação e Dados

Este diagrama ilustra o processo pelo qual o paciente utiliza questionários digitais para autoavaliar seus sintomas, e como esses dados são integrados ao sistema de saúde.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

actor Paciente
participant "Aplicativo Móvel (e-Saúde Mental)" as App
participant "Sistema e-Saúde Mental (Backend/IA)" as Backend
participant "Rede Nacional de Dados em Saúde (RNDS)" as RNDS
database "Prontuário Eletrônico (Local UBS)" as ProntuarioUBS

Paciente -> App : Acessa **Questionários Digitais Cientificamente Validados**
activate App
App --> Paciente : Apresenta Questionários (ex: para insônia, ansiedade, depressão)
Paciente -> App : **Preenche e Submete Questionários**
App -> Backend : Envia Respostas dos Questionários
activate Backend
Backend -> Backend : Processa Respostas e Gera Resultados
Backend -> RNDS : **Envia Dados da Autoavaliação** (Resultados, Escalas)
activate RNDS
RNDS -> ProntuarioUBS : **Integra Dados ao Prontuário Eletrônico** do paciente (registro longitudinal)
deactivate RNDS
deactivate Backend
App --> Paciente : (Opcional) Exibe Resumo da Autoavaliação
deactivate App
@enduml
```

#### 1.4 Fluxo de Comunicação e Conexão

Demonstra como a plataforma facilita a comunicação segura entre o paciente e sua equipe de saúde da Atenção Primária.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #FFFFFF
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #FFFFFF
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #FFFFFF
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #FFFFFF
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #FFFFFF
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
    LoopBorderColor #00A8E8
    LoopBackgroundColor #1F2937
    LoopFontColor #FFFFFF
    GroupBorderColor #00A8E8
    GroupBackgroundColor #1F2937
    GroupFontColor #FFFFFF
}

actor Paciente
participant "Aplicativo Móvel (e-Saúde Mental)" as App
participant "Profissional da APS (Sistema)" as APS_System

Paciente -> App : Inicia comunicação (via **chat ou teleconsulta**)
activate App
App -> APS_System : Estabelece canal de comunicação segura
activate APS_System
APS_System --> Paciente : Permite conexão com a equipe de referência na APS
loop Enquanto a comunicação for ativa
    Paciente <-> APS_System : Troca de mensagens / Realiza Teleconsulta
end
deactivate APS_System
deactivate App
@enduml
```

### 2. O Profissional da Atenção Primária (APS)

Para os profissionais da APS, a plataforma funciona como um **"copiloto" inteligente**, visando aumentar sua confiança e capacidade no manejo de casos de saúde mental.

#### 2.1 Recebimento de Dados e Apoio à Decisão Clínica

Este diagrama ilustra como o profissional da APS recebe os dados do paciente via RNDS e como a IA do sistema oferece suporte à decisão clínica.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #FFFFFF
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #FFFFFF
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #FFFFFF
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #FFFFFF
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #FFFFFF
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

actor "Profissional da APS" as ProfissionalAPS
participant "Rede Nacional de Dados em Saúde (RNDS)" as RNDS
participant "Prontuário Eletrônico (Local UBS)" as ProntuarioUBS
participant "Sistema e-Saúde Mental (Backend/IA)" as BackendIA

RNDS -> ProntuarioUBS : Envia dados do paciente (autoavaliação, histórico)
activate ProntuarioUBS
ProfissionalAPS -> ProntuarioUBS : Acessa prontuário do paciente
activate ProfissionalAPS
ProntuarioUBS -> BackendIA : Solicita **Apoio à Decisão Clínica** (com base nos dados)
activate BackendIA
BackendIA -> BackendIA : **IA analisa dados do paciente** (respostas a questionários, histórico de sintomas)
BackendIA --> BackendIA : **Sugere Diagnósticos Prováveis**
BackendIA --> BackendIA : **Recomenda Condutas Clínicas** (terapia medicamentosa, intervenções digitais, encaminhamento)
BackendIA --> ProntuarioUBS : Envia Sugestões da IA
deactivate BackendIA
ProntuarioUBS --> ProfissionalAPS : Exibe sugestões da IA no prontuário
ProfissionalAPS -> ProfissionalAPS : Avalia sugestões e combina com seu julgamento clínico
deactivate ProfissionalAPS
deactivate ProntuarioUBS
@enduml
```

#### 2.2 Alerta de Risco e Ação Proativa

O fluxo demonstra como o sistema detecta situações de gravidade e emite alertas, permitindo uma intervenção rápida e proativa por parte da equipe de saúde.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #FFFFFF
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #FFFFFF
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #FFFFFF
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #FFFFFF
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #FFFFFF
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
    LoopBorderColor #00A8E8
    LoopBackgroundColor #1F2937
    LoopFontColor #FFFFFF
    GroupBorderColor #00A8E8
    GroupBackgroundColor #1F2937
    GroupFontColor #FFFFFF
}

participant "Sistema e-Saúde Mental (Backend/IA)" as BackendIA
participant "Profissional da APS (Sistema)" as APS_System
actor "Profissional da APS" as ProfissionalAPS
participant "CAPS (Sistema de Agendamento)" as CAPS_System

BackendIA -> BackendIA : **Detecta automaticamente situações de gravidade** (ex: ideação suicida, sintomas psicóticos agudos)
BackendIA -> APS_System : **Emite Alerta Imediato** para a equipe de saúde
activate APS_System
APS_System --> ProfissionalAPS : Recebe Alerta de Risco Grave
activate ProfissionalAPS

alt Risco Alto / Necessidade Urgente
    ProfissionalAPS -> APS_System : Aciona Protocolo de Intervenção Urgente
    APS_System -> CAPS_System : Solicita Agendamento Urgente / Encaminhamento Direto para CAPS
    CAPS_System --> APS_System : Confirma Agendamento / Encaminhamento
    APS_System --> ProfissionalAPS : Notifica Confirmação
else Risco Moderado / Necessidade de Avaliação
    ProfissionalAPS -> APS_System : Agenda Consulta Presencial
    APS_System --> ProfissionalAPS : Confirma Agendamento
end

deactivate ProfissionalAPS
deactivate APS_System
@enduml
```

#### 2.3 Monitoramento e Gestão da Carteira

Este diagrama ilustra como os profissionais da APS utilizam o painel de monitoramento para acompanhar a evolução dos pacientes e gerenciar suas respectivas carteiras.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

actor "Profissional da APS" as ProfissionalAPS
participant "Sistema e-Saúde Mental (Painel de Monitoramento)" as DashboardAPS
database "Sistema e-Saúde Mental (Dados do Paciente)" as PatientData

ProfissionalAPS -> DashboardAPS : Acessa **Painel de Monitoramento Individual para cada paciente**
activate DashboardAPS
DashboardAPS -> PatientData : Solicita dados da carteira de pacientes
PatientData --> DashboardAPS : Envia dados (evolução, adesão, status)
DashboardAPS --> ProfissionalAPS : Exibe Visão Geral da Carteira de Pacientes
ProfissionalAPS -> DashboardAPS : Seleciona Paciente para Monitoramento Detalhado
DashboardAPS -> PatientData : Solicita dados específicos do paciente
PatientData --> DashboardAPS : Fornece dados (evolução dos sintomas ao longo do tempo, adesão às atividades propostas)
DashboardAPS --> ProfissionalAPS : **Visualiza Evolução de Sintomas e Adesão**
ProfissionalAPS -> ProfissionalAPS : **Gerencia sua carteira de pacientes** de forma organizada
deactivate DashboardAPS
@enduml
```

#### 2.4 Registro e Feedback para o Sistema

O diagrama mostra como os registros clínicos feitos pelo profissional são enviados de volta para a RNDS, atualizando o histórico de saúde do paciente.

```plantuml
@startuml
actor "Profissional da APS" as ProfissionalAPS
participant "Prontuário Eletrônico (Local UBS)" as ProntuarioUBS
cloud "Rede Nacional de Dados em Saúde (RNDS)" as RNDS
database "Sistema e-Saúde Mental (Backend)" as Backend

ProfissionalAPS -> ProntuarioUBS : Realiza Consulta (Presencial ou Remota)
activate ProntuarioUBS
ProfissionalAPS -> ProntuarioUBS : <b>Confirma Diagnóstico e Define Plano Terapêutico</b>
ProntuarioUBS -> RNDS : <b>Envia Novo Registro Clínico</b> (Diagnóstico, Plano)
activate RNDS
RNDS -> RNDS : <b>Atualiza Histórico de Saúde do Paciente</b> (Prontuário Eletrônico Unificado)
RNDS --> ProntuarioUBS : Confirma Recebimento
deactivate RNDS
ProntuarioUBS --> Backend : Notifica Backend sobre atualização (para potencial feedback à IA)
deactivate ProntuarioUBS
@enduml
```

#### 2.5 Matriciamento e Teleinterconsulta

Este fluxo ilustra como o profissional da APS pode solicitar apoio de um especialista do CAPS via teleinterconsulta, utilizando os dados pré-coletados pelo aplicativo para qualificar o matriciamento.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

actor "Profissional da APS" as ProfissionalAPS
participant "Prontuário Eletrônico (Local UBS)" as ProntuarioUBS
participant "Sistema e-Saúde Mental (Backend)" as Backend
actor "Especialista do CAPS" as EspecialistaCAPS
participant "Sistema de Teleinterconsulta (CAPS)" as TeleconsultaCAPS

ProfissionalAPS -> ProntuarioUBS : Identifica caso complexo (via alerta ou monitoramento)
activate ProntuarioUBS
ProntuarioUBS -> Backend : Solicita Dados Detalhados do Paciente (coletados via aplicativo)
activate Backend
Backend --> ProntuarioUBS : Fornece Dados Detalhados do Paciente
deactivate Backend
ProfissionalAPS -> ProntuarioUBS : **Inicia solicitação de Teleinterconsulta**
ProntuarioUBS -> TeleconsultaCAPS : Envia Solicitação de Teleinterconsulta e **Dados do Paciente Pré-Compartilhados**
activate TeleconsultaCAPS
TeleconsultaCAPS --> EspecialistaCAPS : Notifica sobre solicitação e disponibiliza dados para **apoio matricial qualificado**
activate EspecialistaCAPS
EspecialistaCAPS -> TeleconsultaCAPS : Agenda / Aceita Teleinterconsulta
TeleconsultaCAPS --> ProntuarioUBS : Confirma Agendamento
deactivate TeleconsultaCAPS
ProntuarioUBS --> ProfissionalAPS : Notifica Agendamento
ProfissionalAPS <-> EspecialistaCAPS : **Realiza Teleinterconsulta (Matriciamento)**
deactivate EspecialistaCAPS
deactivate ProntuarioUBS
@enduml
```

### 3. O Gestor de Saúde Pública

O módulo de gestão visa transformar os dados clínicos gerados em **inteligência acionável para a formulação de políticas públicas**.

#### 3.1 Coleta e Agregação de Dados Anonimizados

Este diagrama mostra como os dados coletados de pacientes e profissionais são agregados e anonimizados para a vigilância epidemiológica e análise de tendências.

```plantuml
@startuml
participant "Sistema e-Saúde Mental (Backend)" as Backend
cloud "Rede Nacional de Dados em Saúde (RNDS)" as RNDS
database "Data Lake/Data Warehouse (Gestão)" as DataLake

Backend -> Backend : **Agrega dados de pacientes e profissionais** (anonimizados)
Backend -> RNDS : **Envia Lotes de Dados Anonimizados** (ex: prevalência de sintomas, uso de funcionalidades)
activate RNDS
RNDS -> DataLake : Armazena e consolida dados anonimizados
deactivate RNDS
@enduml
```

#### 3.2 Visualização e Análise de Indicadores

Ilustra como os gestores acessam painéis interativos para visualizar indicadores-chave de saúde mental e obter insights para a tomada de decisões.

```plantuml
@startuml

!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

actor "Gestor de Saúde Pública" as Gestor
participant "Módulo de Gestão (Dashboards)" as Dashboard
database "Data Lake/Data Warehouse (Gestão)" as DataLake

Gestor -> Dashboard : Acessa **Painéis Interativos (Dashboards)**
activate Dashboard
Dashboard -> DataLake : Solicita Indicadores-Chave de Saúde Mental
DataLake --> Dashboard : Fornece dados agregados (ex: prevalência de transtornos, eficácia das intervenções, tempo de espera, taxas de recuperação)
Dashboard --> Gestor : **Exibe Dashboards com Indicadores-Chave de Saúde Mental**
Gestor -> Gestor : Analisa Tendências e Padrões de Adoecimento
deactivate Dashboard
@enduml
```

#### 3.3 Apoio à Formulação de Políticas e Otimização de Recursos

Este diagrama detalha como as informações e análises da plataforma são utilizadas para otimizar a alocação de recursos e planejar serviços de saúde mental.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}


actor "Gestor de Saúde Pública" as Gestor
participant "Módulo de Gestão (Dashboards)" as Dashboard
participant "Sistema e-Saúde Mental (Backend/IA de Gestão)" as BackendIA_Gestao

Gestor -> Dashboard : Interpreta Indicadores e Tendências dos Dashboards
activate Dashboard
Dashboard -> BackendIA_Gestao : (Opcional) Solicita Análises Preditivas / Cenários
activate BackendIA_Gestao
BackendIA_Gestao -> BackendIA_Gestao : **Estima as necessidades de saúde mental** de estados e municípios
BackendIA_Gestao -> BackendIA_Gestao : **Preve respostas a tratamentos** em diferentes perfis populacionais
BackendIA_Gestao --> Dashboard : Envia Análises e Projeções
deactivate BackendIA_Gestao
Dashboard --> Gestor : Apresenta Insights para Decisões
deactivate Dashboard
Gestor -> Gestor : **Otimiza Alocação de Recursos e Planejamento de Serviços**
Gestor -> Gestor : **Formula Políticas Públicas Mais Eficazes** (baseadas em evidências)
@enduml
```

#### 3.4 Vigilância Epidemiológica


O fluxo final mostra como a agregação de dados anonimizados permite uma vigilância epidemiológica abrangente, identificando padrões e particularidades regionais na saúde mental.

```plantuml
@startuml
!theme vibrant
' Definições de Estilo (Dark Theme)
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparam defaultFontColor #FFFFFF
skinparam title {
    FontColor #FFFFFF
}
skinparam actor {
    BorderColor #90E0EF
    BackgroundColor #374151
    FontColor #E5E7EB
}
skinparam usecase {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam rectangle {
    BorderColor #00A8E8
    BackgroundColor #1F2937
    FontColor #E5E7EB
}
skinparam arrow {
    Color #90E0EF
}
skinparam sequence {
    ParticipantBorderColor #90E0EF
    ParticipantBackgroundColor #374151
    ParticipantFontColor #E5E7EB
    DatabaseBorderColor #00A8E8
    DatabaseBackgroundColor #1F2937
    DatabaseFontColor #E5E7EB
    LifeLineBackgroundColor #111827
    LifeLineBorderColor #374151
}

participant "Sistema e-Saúde Mental (Backend)" as Backend
cloud "Rede Nacional de Dados em Saúde (RNDS)" as RNDS
database "Data Lake/Data Warehouse (Gestão)" as DataLake
actor "Gestor de Saúde Pública" as Gestor
participant "Módulo de Gestão (Ferramentas de Vigilância)" as VigilanceTools

Backend -> RNDS : Envia Dados Anonimizados para Agregação Nacional
activate RNDS
RNDS -> DataLake : **Consolida Dados Epidemiológicos** de todas as interações
deactivate RNDS
Gestor -> VigilanceTools : Acessa Ferramentas de Vigilância Epidemiológica
activate VigilanceTools
VigilanceTools -> DataLake : Consulta Dados Consolidados
DataLake --> VigilanceTools : Fornece Dados Agregados e Geospatializados
VigilanceTools --> Gestor : **Exibe Padrões de Transtornos Mentais, Tendências de Adoecimento e Particularidades Regionais**
deactivate VigilanceTools
Gestor -> Gestor : **Realiza Vigilância Epidemiológica sem precedentes** para Saúde Mental
@enduml
```