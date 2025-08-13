## Exemplos Práticos de Comunicação HL7 FHIR no e-Saúde Mental

A seguir, demonstramos com exemplos concretos como o padrão HL7 FHIR será utilizado para a troca de informações entre as diferentes plataformas que compõem o projeto "e-Saúde Mental no SUS". Os exemplos seguem a jornada de um paciente hipotético, João da Silva.

### **1. Plataforma do Paciente (Aplicativo Android)**

O paciente João da Silva, utilizando o aplicativo "e-Saúde Mental" no seu smartphone Android, responde a um questionário de avaliação para ansiedade (GAD-7).

**Ação:** Após João preencher as 7 perguntas, o aplicativo precisa enviar essas respostas para o backend da plataforma.

**Como o HL7 FHIR é usado:**

O aplicativo irá construir um recurso FHIR do tipo `QuestionnaireResponse`. Este recurso contém as respostas de João e as associa ao seu cadastro de paciente e ao questionário específico que ele respondeu.

O aplicativo então envia este recurso para o servidor FHIR da plataforma através de uma requisição `POST` para o endpoint `[servidor]/QuestionnaireResponse`.

**Exemplo do Recurso `QuestionnaireResponse` em JSON (gerado pelo app Android):**

```js
{
  "resourceType": "QuestionnaireResponse",
  "status": "completed",
  "questionnaire": "Questionnaire/gad-7",
  "subject": {
    "reference": "Patient/12345",
    "display": "João da Silva"
  },
  "authored": "2025-08-13T10:30:00-03:00",
  "item": [
    {
      "linkId": "1",
      "text": "Sentir-se nervoso, ansioso ou muito tenso",
      "answer": [{
        "valueCoding": {
          "system": "http://loinc.org",
          "code": "LA6568-5",
          "display": "Vários dias"
        }
      }]
    },
    {
      "linkId": "2",
      "text": "Não ser capaz de impedir ou controlar as preocupações",
      "answer": [{
        "valueCoding": {
          "system": "http://loinc.org",
          "code": "LA6569-3",
          "display": "Mais da metade dos dias"
        }
      }]
    }
    // ... demais 5 respostas
  ]
}
```

### **2. Plataforma do Profissional (Sistema da UBS - Aplicação Web)**

A Dra. Ana, médica da família de João na UBS, abre o prontuário eletrónico para a consulta. O sistema precisa mostrar os resultados da avaliação de João e a análise da IA.

**Ação 1: Visualizar os resultados.**

O sistema da UBS, conectado à RNDS, busca as informações mais recentes de João. O backend da plataforma "e-Saúde Mental", após processar o `QuestionnaireResponse` de João, gerou dois novos recursos do tipo `Observation`: um com a pontuação total do GAD-7 e outro com a estratificação de risco da IA.

**Como o HL7 FHIR é usado:**

O sistema da UBS faz uma requisição `GET` ao servidor FHIR, pedindo todas as "Observações" para o paciente João: `GET [servidor]/Observation?patient=12345`.

**Exemplo do Recurso `Observation` para a Pontuação (retornado para o sistema da UBS):**

```js
{
  "resourceType": "Observation",
  "status": "final",
  "category": [{
    "coding": [{
      "system": "http://terminology.hl7.org/CodeSystem/observation-category",
      "code": "survey"
    }]
  }],
  "code": {
    "coding": [{
      "system": "http://loinc.org",
      "code": "70274-6",
      "display": "GAD-7 total score"
    }]
  },
  "subject": { "reference": "Patient/12345" },
  "effectiveDateTime": "2025-08-13T10:30:00-03:00",
  "valueQuantity": {
    "value": 14,
    "unit": "{score}",
    "system": "http://unitsofmeasure.org"
  },
  "interpretation": [{
    "coding": [{
      "system": "http://acme.org/obs-interpretations",
      "code": "MOD",
      "display": "Ansiedade Moderada"
    }]
  }]
}
```

**Ação 2: Confirmar o diagnóstico.**

Com base na consulta e nos dados da plataforma, a Dra. Ana confirma o diagnóstico de "Transtorno de Ansiedade Generalizada".

**Como o HL7 FHIR é usado:**

O sistema da UBS cria um recurso `DiagnosticReport` para formalizar o diagnóstico e o envia via `POST` para o servidor FHIR, que o distribui pela RNDS.

**Exemplo do Recurso `DiagnosticReport` em JSON (gerado pelo sistema da UBS):**

```
{
  "resourceType": "DiagnosticReport",
  "status": "final",
  "code": {
    "coding": [{
      "system": "http://hl7.org/fhir/sid/icd-10",
      "code": "F41.1",
      "display": "Transtorno de ansiedade generalizada"
    }]
  },
  "subject": { "reference": "Patient/12345" },
  "effectiveDateTime": "2025-08-13T11:15:00-03:00",
  "conclusion": "Paciente apresenta quadro clínico compatível com Transtorno de Ansiedade Generalizada, corroborado por avaliação GAD-7.",
  "result": [
    { "reference": "Observation/gad7-score-xyz" }
  ]
}
```

### **3. Plataforma do Gestor (Dashboard de Gestão - Aplicação Web)**

Um gestor de saúde municipal quer saber a prevalência de diagnósticos de ansiedade na sua cidade no último mês.

**Ação:** O gestor acede ao dashboard e aplica os filtros desejados.

**Como o HL7 FHIR é usado:**

Neste caso, o gestor não interage diretamente com recursos FHIR individuais por questões de privacidade e performance. A arquitetura aqui é diferente:

1. O dashboard faz uma chamada a uma **API de Analytics** específica, por exemplo: `GET /analytics/prevalence?diagnosis=F41.1&city=MinhaCidade`.
2. O **Backend** da plataforma recebe esta chamada.
3. O Backend executa uma consulta no **Data Lake Anonimizado**. Este Data Lake contém milhões de recursos `DiagnosticReport` e `Observation` sem nenhuma informação que possa identificar os pacientes.
4. A consulta agrega os dados (ex: `COUNT DiagnosticReport WHERE code='F41.1' AND patient.address.city='MinhaCidade'`).
5. O Backend **não retorna** uma lista de recursos FHIR. Em vez disso, ele retorna um objeto JSON simples com o resultado agregado, que é usado para popular os gráficos do dashboard.


**Exemplo da Resposta da API de Analytics (consumida pelo dashboard):**

```
{
  "query": {
    "diagnosis": "F41.1",
    "city": "MinhaCidade",
    "period": "2025-07-01_2025-07-31"
  },
  "result": {
    "total_cases": 874,
    "prevalence_rate": "2.1%",
    "comparison_previous_month": "+15%"
  }
}
```

Esta abordagem mostra como o HL7 FHIR serve de base para toda a coleta e troca de dados individuais, enquanto as APIs de analytics consomem esses dados de forma agregada e anónima para fornecer inteligência para a gestão, garantindo tanto a interoperabilidade quanto a privacidade.