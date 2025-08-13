

![[ER Modularizado.png]]
```plantuml
@startuml
!theme vibrant

' Definições de Estilo (Dark Theme)
skinparam linetype ortho
skinparam shadowing false
skinparam roundcorner 10
skinparam backgroundColor #111827
skinparan fontColor #E5E7EB
skinparam title {
    FontColor #FFFFFF
}
skinparam package {
    FontColor #E5E7EB
    BorderColor #00A8E8
    BackgroundColor #1F2937
}
skinparam entity {
    FontColor #E5E7EB
    BorderColor #90E0EF
    BackgroundColor #374151
}
skinparam diamond {
    FontColor #111827
    BorderColor #00A8E8
    BackgroundColor #90E0EF
}
skinparam relationship {
    LineColor #90E0EF
    LineThickness 1.5
}
skinparam note {
    backgroundColor #374151
    borderColor #90E0EF
    fontColor #E5E7EB
}

title Diagrama ER Modular do "e-Saúde Mental" (Alinhado ao Padrão HL7 FHIR)

' --- Módulo de Base e Identidade (Foundation & Identity) ---
package "Módulo de Base e Identidade (Foundation & Identity)" {
  entity "Usuario" as E_Usuario {
    + **ID_Usuario** (PK)
    --
    Nome_Completo
    CPF_Criptografado
    Email_Verificado
    ID_GovBr (UUID)
    Tipo_Usuario (Enum: Paciente, Profissional)
    Data_Cadastro
  }

  entity "Paciente" as E_Paciente {
    + **ID_Paciente** (PK, FK de Usuario)
    --
    CNS (Cartão Nacional de Saúde)
    Nome_Social
    Data_Nascimento
    Genero
  }

  entity "Profissional" as E_Profissional {
    + **ID_Profissional** (PK, FK de Usuario)
    --
    Registro_Conselho (ex: CRM, CRP)
    Especialidade
    Tipo (Enum: APS, CAPS, Gestor)
  }
  
  E_Usuario <|-- E_Paciente
  E_Usuario <|-- E_Profissional
  note on link: Herança (É um)
}

' --- Módulo de Engajamento do Paciente e Coleta de Dados (Patient Engagement & Data Collection) ---
package "Módulo de Engajamento do Paciente (Diagnostics & Care Provision)" {
  entity "RespostaQuestionario" as E_RespostaQuestionario {
    + **ID_Resposta** (PK)
    --
    # //ID_Paciente// (FK)
    # //ID_Questionario// (FK)
    Data_Hora_Submissao
    Respostas_JSON
    Pontuacao_Total_Calculada
    Nivel_Risco_Inferido (Enum: Baixo, Médio, Alto)
  }
  
  diamond "Responde" as R_Responde
  
  E_Paciente "1" -- "0..*" R_Responde
  R_Responde "0..*" -- "1" E_RespostaQuestionario
}

' --- Módulo Clínico e de Apoio à Decisão (Clinical & Decision Support) ---
package "Módulo Clínico e de Apoio à Decisão (Clinical & Decision Support)" {
  entity "Questionario" as E_Questionario {
    + **ID_Questionario** (PK)
    --
    Nome_Tecnico (ex: "GAD-7", "PHQ-9")
    Versao
    Tipo (Enum: Triagem, Monitoramento)
    Estrutura_Perguntas_JSON
  }

  entity "Observacao" as E_Observacao {
    + **ID_Observacao** (PK)
    --
    # //ID_Paciente// (FK)
    # //ID_RespostaQuestionario// (FK, Opcional)
    Codigo_LOINC
    Valor_Observado
    Interpretacao_Clinica
  }

  entity "RelatorioDiagnostico" as E_RelatorioDiagnostico {
    + **ID_Relatorio** (PK)
    --
    # //ID_Paciente// (FK)
    # //ID_Profissional_Emissor// (FK)
    Codigo_CID10
    Conclusao_Texto_Profissional
  }

  entity "PlanoCuidado" as E_PlanoCuidado {
    + **ID_Plano** (PK)
    --
    # //ID_Paciente// (FK)
    # //ID_Profissional_Criador// (FK)
    Descricao_Geral
    Objetivos_Terapeuticos
  }

  entity "Intervencao" as E_Intervencao {
    + **ID_Intervencao** (PK)
    --
    # //ID_PlanoCuidado// (FK)
    Tipo (Enum: Digital, Medicamentosa)
    Descricao_Detalhada
  }

  diamond "Emite" as R_EmiteDiagnostico
  diamond "Cria" as R_CriaPlano
  diamond "Gera" as R_GeraObservacao
  diamond "Contém" as R_Contem
  
  E_Questionario "1" -- "0..*" R_Responde
  
  E_RespostaQuestionario "1" -- "1..*" R_GeraObservacao
  R_GeraObservacao "1..*" -- "1" E_Observacao
  
  E_Profissional "1" -- "0..*" R_EmiteDiagnostico
  R_EmiteDiagnostico "0..*" -- "1" E_RelatorioDiagnostico
  E_Paciente "1" -- "0..*" E_RelatorioDiagnostico
  
  E_Profissional "1" -- "0..*" R_CriaPlano
  R_CriaPlano "0..*" -- "1" E_PlanoCuidado
  E_Paciente "1" -- "0..*" E_PlanoCuidado
  
  E_PlanoCuidado "1" -- "1..*" R_Contem
  R_Contem "1..*" -- "1" E_Intervencao
}

' --- Módulo Administrativo e de Saúde Populacional (Administration & Population Health) ---
package "Módulo Administrativo e de Saúde Populacional (Administration)" {
  entity "Alerta" as E_Alerta {
    + **ID_Alerta** (PK)
    --
    # //ID_Paciente// (FK)
    # //ID_Profissional_Responsavel// (FK)
    Tipo_Alerta (Enum: Risco Suicida)
    Nivel_Urgencia (Enum: Alto, Médio)
    Status (Enum: Aberto, Fechado)
  }
  
  diamond "É Notificado" as R_Notificado
  
  E_Profissional "1" -- "0..*" R_Notificado
  R_Notificado "0..*" -- "1" E_Alerta
  E_Paciente "1" -- "0..*" E_Alerta
  
  note as N1
    **Gestão de Saúde Pública:**
    O usuário **Gestor** (um tipo de Profissional)
    não possui entidades próprias.
    Ele consome dados agregados e anonimizados
    das entidades **RelatorioDiagnostico** e **Observacao**
    para alimentar painéis de vigilância epidemiológica.
  end note
  E_Profissional .. N1
}

@enduml
```



![[E-R Simplificado.png]]